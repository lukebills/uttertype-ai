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
            temperature=0.5
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
            "Use the context to determine the appropriate formatting style:\n"
            "- For emails: Include appropriate greetings (e.g., 'Hi John,' or 'Dear Team,'), structure with clear paragraphs using line breaks, "
            "and maintain a professional tone. Fix grammar and punctuation.\n"
            "- For Teams messages: Include appropriate greetings (e.g., 'Hi John,' or 'Hey team,'), format as a single flowing message "
            "without unnecessary line breaks, and maintain a conversational tone. Fix grammar and remove filler words.\n"
            "- For other messages: Format with minimal changes, fixing basic grammar and removing obvious filler words.\n"
            "Ignore any spoken context at the beginning and format only the actual message content. "
            "Return only the formatted message without any explanation or added text:"
        ),
        # Commented out specific prompts for future reference
        # "message": (
        #     "Format this text message with minimal changes. "
        #     "Only fix basic grammar and remove obvious filler words. "
        #     "If the message includes initial context before the actual message, ignore it and only format the main message content. "
        #     "Return only the formatted text, no explanations:"
        # ),
        # "email": (
        #     "Format this email with minimal changes. Fix basic grammar and punctuation. "
        #     "Structure the content into clear paragraphs with proper line breaks. "
        #     "Ignore any spoken context at the beginning and format only the actual email body. "
        #     "Do not add greetings, closings, or signatures. Return only the formatted email body, no explanations:"
        # ),
        # "teams": (
        #     "Format this Teams message with minimal changes. Only fix basic grammar and remove obvious filler words. "
        #     "Ignore any contextual preamble if present and format only the message itself. "
        #     "Return only the formatted text, no explanations:"
        # )
    }
    
    try:
        # Determine the context of the text
        # context = determine_context(text)
        
        # Always use the default prompt regardless of context
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": prompts["default"]},
                {"role": "user", "content": text}
            ],
            temperature=0.5
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
