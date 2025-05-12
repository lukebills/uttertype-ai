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

def determine_context(text: str) -> str:
    """Determine the context of the text using sentiment analysis."""
    client = OpenAI(base_url=os.getenv('OPENAI_BASE_URL'))
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "Analyze this text and determine if it's most likely a text message, email, or Teams message. Consider the tone, formality, and content. Respond with exactly one word: 'message', 'email', or 'teams'."},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"Error determining context: {e}")
        return "message"  # Default to message if there's an error

def format_with_context(text: str) -> str:
    """Format text based on its determined context."""
    # Create OpenAI client
    client = OpenAI(base_url=os.getenv('OPENAI_BASE_URL'))
    
    # Create context-specific prompt
    prompts = {
        "default": (
            "You will receive a transcribed message where the first part may describe the context "
            "(e.g. 'this is an email to a supplier', 'this is a Teams message to my colleague', or 'this is a technical explanation'). "
            "Use the context to determine the appropriate formatting style. "
            "Format the actual message content that follows the context. "
            "Apply minimal edits: fix basic grammar, punctuation, and remove filler words. "
            "Structure emails with clear paragraphs, Teams messages with clear sentences, and technical content for clarity. "
            "Return only the formatted message without any explanation or added text:"
        )
    }
    
    try:
        # Determine the context of the text
        context = determine_context(text)
        
        # Get formatted response
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": prompts[context]},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
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
                    else:
                        formatted_text = transcription.strip()
                    
                    clipboard_type(formatted_text)
                    console_table.insert(
                        formatted_text,
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
