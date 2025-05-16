import os
import io
from typing import List, Tuple
import pyaudio
import wave
from openai import OpenAI
import asyncio
from threading import Thread, Event
import webrtcvad
from utils import transcription_concat
import tempfile
import time

FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 16000  # Sample rate
CHUNK_DURATION_MS = 30  # Frame duration in milliseconds
CHUNK = int(RATE * CHUNK_DURATION_MS / 1000)
MIN_TRANSCRIPTION_SIZE_MS = int(
    os.getenv('UTTERTYPE_MIN_TRANSCRIPTION_SIZE_MS', 1500) # Minimum duration of speech to send to API in case of silence
)
CHUNK_PROCESSING_INTERVAL_MS = 2000  # Process chunks every 2 seconds
CONTEXT_WINDOW_SIZE = 3  # Number of previous chunks to use for context


class AudioTranscriber:
    def __init__(self, use_vad=True):
        self.audio = pyaudio.PyAudio()
        self.recording_finished = Event()  # Threading event to end recording
        self.recording_finished.set()  # Initialize as finished
        self.frames = []
        self.initial_buffer = []  # Buffer for the first 1 second of audio
        self.audio_duration = 0
        self.rolling_transcriptions: List[Tuple[int, str]] = []  # (idx, transcription)
        self.rolling_requests: List[Thread] = []  # list of pending requests
        self.event_loop = asyncio.get_event_loop()
        self.use_vad = use_vad
        if use_vad:
            self.vad = webrtcvad.Vad(1)  # Voice Activity Detector, mode can be 0 to 3
        self.transcriptions = asyncio.Queue()
        self.is_processing = False  # Flag to prevent multiple transcriptions
        self.all_frames = []  # Store all frames for the complete recording
        self.last_chunk_time = 0  # Track when we last processed a chunk
        self.current_chunk_frames = []  # Store frames for current chunk
        self.previous_chunks = []  # Store previous chunk transcriptions for context
        self.client = OpenAI(base_url=os.getenv('OPENAI_BASE_URL'))

    def _get_context_prompt(self) -> str:
        """Generate a prompt that includes context from previous chunks."""
        if not self.previous_chunks:
            return "The following is normal speech."
        
        context = " ".join(self.previous_chunks[-CONTEXT_WINDOW_SIZE:])
        return f"Previous context: {context}\nContinue the transcription with proper grammar and punctuation:"

    def _post_process_text(self, text: str) -> str:
        """Post-process the text to improve grammar and formatting."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "Fix any grammar, punctuation, and formatting issues in the following text. Maintain the original meaning but ensure proper sentence structure and flow. Return only the corrected text:"},
                    {"role": "user", "content": text}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in post-processing: {e}")
            return text

    def start_recording(self):
        """Start recording audio from the microphone."""
        self.is_processing = False  # Reset processing flag when starting new recording
        def _record():
            self.recording_finished = Event()
            stream = self.audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
            )
            self.frames = []
            self.initial_buffer = []
            self.all_frames = []  # Reset all frames
            self.current_chunk_frames = []  # Reset current chunk frames
            self.previous_chunks = []  # Reset previous chunks
            self.audio_duration = 0
            self.last_chunk_time = time.time() * 1000  # Convert to milliseconds
            start_time = None
            
            while not self.recording_finished.is_set():  # Keep recording until interrupted
                data = stream.read(CHUNK)
                if start_time is None:
                    start_time = time.time()
                self.audio_duration += CHUNK_DURATION_MS
                
                # Store all frames for the complete recording
                self.all_frames.append(data)
                self.current_chunk_frames.append(data)
                
                # Check if it's time to process the current chunk
                current_time = time.time() * 1000
                if current_time - self.last_chunk_time >= CHUNK_PROCESSING_INTERVAL_MS:
                    if len(self.current_chunk_frames) > 0:
                        # Process the current chunk
                        self._process_chunk(self.current_chunk_frames)
                        self.current_chunk_frames = []  # Reset for next chunk
                        self.last_chunk_time = current_time

        Thread(target=_record).start()

    def _process_chunk(self, chunk_frames):
        """Process a chunk of audio frames for transcription."""
        if not chunk_frames:
            return

        # Create a buffer with the chunk frames
        buffer = io.BytesIO()
        buffer.name = "tmp.wav"
        wf = wave.open(buffer, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(chunk_frames))
        wf.close()
        
        # Get the transcription for this chunk with context
        transcription = self.transcribe_audio(buffer)
        
        if transcription:
            # Add to previous chunks for context
            self.previous_chunks.append(transcription.strip())
            # Keep only the last N chunks for context
            if len(self.previous_chunks) > CONTEXT_WINDOW_SIZE:
                self.previous_chunks = self.previous_chunks[-CONTEXT_WINDOW_SIZE:]
            
            # Post-process the transcription
            processed_text = self._post_process_text(transcription.strip())
            
            # Put the processed transcription in the queue
            self.event_loop.call_soon_threadsafe(
                self.transcriptions.put_nowait,
                (processed_text, len(chunk_frames) * CHUNK_DURATION_MS),
            )

    def _finish_transcription(self):
        # Process any remaining frames in the current chunk
        if self.current_chunk_frames:
            self._process_chunk(self.current_chunk_frames)
            self.current_chunk_frames = []

        # Clear any pending transcriptions
        while not self.transcriptions.empty():
            try:
                self.transcriptions.get_nowait()
                self.transcriptions.task_done()
            except asyncio.QueueEmpty:
                break

        # Process the complete audio recording
        if self.all_frames:
            # Create a buffer with all the audio frames
            buffer = io.BytesIO()
            buffer.name = "tmp.wav"
            wf = wave.open(buffer, "wb")
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b"".join(self.all_frames))
            wf.close()
            
            # Get the complete transcription
            transcription = self.transcribe_audio(buffer)
            
            if transcription:
                # Post-process the final transcription
                processed_text = self._post_process_text(transcription.strip())
                
                # Put the final processed transcription in the queue
                self.event_loop.call_soon_threadsafe(
                    self.transcriptions.put_nowait,
                    (processed_text, self.audio_duration),
                )

    def stop_recording(self):
        """Stop the recording and reset variables"""
        if not self.is_processing:  # Only process if not already processing
            self.is_processing = True
            self.recording_finished.set()
            self._finish_transcription()
            self.frames = []
            self.initial_buffer = []
            self.all_frames = []
            self.current_chunk_frames = []
            self.previous_chunks = []
            self.audio_duration = 0
            self.rolling_requests = []
            self.rolling_transcriptions = []
            self.is_processing = False

    def _frames_to_wav(self):
        buffer = io.BytesIO()
        buffer.name = "tmp.wav"
        wf = wave.open(buffer, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        # Combine initial_buffer and frames for the final audio
        wf.writeframes(b"".join(self.initial_buffer + self.frames))
        wf.close()
        return buffer

    def transcribe_audio(self, audio: io.BytesIO) -> str:
        raise NotImplementedError("Please use a subclass of AudioTranscriber")

    async def get_transcriptions(self):
        """
        Asynchronously get transcriptions from the queue.
        Returns (transcription string, audio duration in ms).
        """
        while True:
            transcription = await self.transcriptions.get()
            yield transcription
            self.transcriptions.task_done()


class WhisperAPITranscriber(AudioTranscriber):
    def __init__(self, base_url, model_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model_name = model_name
        self.client = OpenAI(base_url=base_url)

    @staticmethod
    def create(*args, **kwargs):
        base_url = os.getenv('OPENAI_BASE_URL')
        model_name = os.getenv('OPENAI_MODEL_NAME')

        return WhisperAPITranscriber(base_url, model_name)

    def transcribe_audio(self, audio: io.BytesIO) -> str:
        prompt = "The following is normal speech."
        try:
            transcription = self.client.audio.transcriptions.create(
                model=self.model_name,
                file=audio,
                response_format="text",
                language="en",
                prompt=prompt,
            )
            # Remove the prompt from the transcription if it appears
            if isinstance(transcription, str):
                return transcription.replace(prompt, "").strip()
            return transcription
        except Exception as e:
            #print(f"Encountered Error: {e}")
            return ""


"""class WhisperLocalMLXTranscriber(AudioTranscriber):
    def __init__(self, model_type="distil-medium.en", *args, **kwargs):
        super().__init__(*args, **kwargs)
        from lightning_whisper_mlx import LightningWhisperMLX

        self.model = LightningWhisperMLX(model_type)

    def transcribe_audio(self, audio: io.BytesIO) -> str:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                tmpfile.write(audio.getvalue())
                transcription = self.model.transcribe(tmpfile.name)["text"]
                os.unlink(tmpfile.name)
            return transcription
        except Exception as e:
            #print(f"Encountered Error: {e}")
            return "" 
"""
