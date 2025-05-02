import asyncio
from pynput import keyboard
from transcriber import WhisperAPITranscriber
from table_interface import ConsoleTable
from key_listener import create_keylistener
from dotenv import load_dotenv
import os
from utils import manual_type

def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    transcriber = WhisperAPITranscriber.create()
    hotkey = create_keylistener(transcriber)
    console_table = ConsoleTable()

    async def transcription_loop():
        with console_table:
            async for transcription, audio_duration_ms in transcriber.get_transcriptions():
                manual_type(transcription.strip())
                console_table.insert(
                    transcription,
                    round(0.0006 * audio_duration_ms / 1000, 6),
                )

    loop = asyncio.get_event_loop()
    loop.create_task(transcription_loop())

    with keyboard.Listener() as listener:
        def for_canonical(f):
            return lambda k, injected=None: f(listener.canonical(k))

        listener.on_press = for_canonical(hotkey.press)
        listener.on_release = for_canonical(hotkey.release)
        print("[DEBUG] Hotkey listener started. Press your hotkey...")
        loop.run_forever()

if __name__ == "__main__":
    main()
