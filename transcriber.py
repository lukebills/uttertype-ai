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
from logging_config import get_logger
import tempfile
import time

# Initialize logger for this module
logger = get_logger(__name__)

FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 16000  # Sample rate
CHUNK_DURATION_MS = 30  # Frame duration in milliseconds
CHUNK = int(RATE * CHUNK_DURATION_MS / 1000)
MIN_TRANSCRIPTION_SIZE_MS = int(
    os.getenv('UTTERTYPE_MIN_TRANSCRIPTION_SIZE_MS', 1500) # Minimum duration of speech to send to API in case of silence
)


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
            self.audio_duration = 0
            start_time = None
            while not self.recording_finished.is_set():  # Keep recording until interrupted
                data = stream.read(CHUNK)
                if start_time is None:
                    start_time = time.time()
                self.audio_duration += CHUNK_DURATION_MS
                # Store all frames for the complete recording
                self.all_frames.append(data)
                # Also store in frames for VAD processing if enabled
                if self.use_vad:
                    self.frames.append(data)
                else:
                    self.frames = self.all_frames  # If VAD is disabled, use all frames

        Thread(target=_record).start()

    def _finish_transcription(self):
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
            
            # Put the final transcription in the queue
            if transcription:
                self.event_loop.call_soon_threadsafe(
                    self.transcriptions.put_nowait,
                    (transcription.strip(), self.audio_duration),
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
            logger.error(f"Whisper API transcription failed: {e}", exc_info=True)
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
            logger.error(f"Local MLX transcription failed: {e}", exc_info=True)
            return "" 
"""
