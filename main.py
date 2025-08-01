import asyncio
from pynput import keyboard
from transcriber import WhisperAPITranscriber
from table_interface import ConsoleTable
from key_listener import create_keylistener
from dotenv import load_dotenv
import os
from utils import clipboard_type
import tkinter as tk
from tkinter import messagebox
from openai import OpenAI
import sys

# main.py - Make model configurable
def format_with_context(text: str) -> str:
    """Format text based on its determined context."""
    client = OpenAI(base_url=os.getenv('OPENAI_BASE_URL'))
    
    # Use configurable model instead of hard-coded
    model = os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o-mini-2024-07-18')
    
    # Simplified, more effective prompt
    prompt = (
        "Format the transcribed text based on context clues in the message. "
        "Apply appropriate formatting for emails (greeting + paragraphs), "
        "chat messages (casual tone), or minimal editing for other types. "
        "Use Australian English spelling. Output only the formatted text without explanations."
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3  # Lower temperature for more consistent formatting
        )
        # Handle case where content might be None
        content = response.choices[0].message.content
        return content.strip() if content else text.strip()
    except Exception as e:
        print(f"Error formatting text: {e}")
        return text.strip()

def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Create a tkinter dialog to ask the user if they want to use VAD
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    use_vad = messagebox.askyesno("VAD Option", "Would you like to use Voice Activity Detection (VAD)?\n\nYes: Only record when speech is detected.\nNo: Record continuously.")
    root.destroy()

    transcriber = WhisperAPITranscriber.create(use_vad=use_vad)
    hotkey = create_keylistener(transcriber)
    console_table = ConsoleTable()

    async def transcription_loop():
        with console_table:
            async for transcription, audio_duration_ms in transcriber.get_transcriptions():
                # Add a small delay to prevent rapid processing
                await asyncio.sleep(0.1)
                # Only process if we have a non-empty transcription
                if transcription.strip():
                    # Check if AI formatting was requested via hotkey
                    if hotkey.ai_formatting_requested:
                        formatted_text = format_with_context(transcription)
                        display_text = f"[AI] {formatted_text}"
                    else:
                        formatted_text = transcription.strip()
                        display_text = formatted_text
                    
                    # Copy the formatted text to clipboard
                    import pyperclip
                    pyperclip.copy(formatted_text)
                    
                    # Paste the text
                    import pyautogui
                    pyautogui.hotkey("command" if sys.platform == "darwin" else "ctrl", "v")
                    
                    console_table.insert(
                        display_text,
                        round(0.0003 * audio_duration_ms / 1000, 6),
                    )
                    # Reset the formatting flag after processing
                    hotkey.reset_formatting_flag()

    loop = asyncio.get_event_loop()
    loop.create_task(transcription_loop())

    with keyboard.Listener() as listener:
        def for_canonical(f):
            return lambda k, injected=None: f(listener.canonical(k))

        listener.on_press = for_canonical(hotkey.press)
        listener.on_release = for_canonical(hotkey.release)
        loop.run_forever()

if __name__ == "__main__":
    main()
