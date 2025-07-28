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

def format_with_context(text: str) -> str:
    """Format text based on its determined context."""
    # Create OpenAI client
    client = OpenAI(base_url=os.getenv('OPENAI_BASE_URL'))
    
    # Default prompt for all message types
    default_prompt = (
        "You will receive a transcribed message. The opening lines may:\n"
        "  (a) describe context (e.g. 'this is an email to a supplier'), and/or\n"
        "  (b) include explicit formatting instructions.\n"
        "Follow any explicit formatting instructions first. If none are given, infer the correct style from the context.\n\n"
        "Formatting rules:\n"
        "- Emails:\n"
        "  • ALWAYS start with an appropriate greeting (e.g., 'Hi [Name],' or 'Dear [Name],').\n"
        "  • Use clear paragraphs separated by literal double newlines (\\n\\n).\n"
        "  • Each paragraph should be a complete thought or topic.\n"
        "  • Maintain a professional tone; correct grammar, punctuation, and spelling.\n"
        "  • If the input mentions 'email' or 'email to', format as an email with greeting and paragraphs.\n"
        "- Teams/Chat messages:\n"
        "  • Start with a brief greeting if appropriate (e.g., 'Hi [Name],').\n"
        "  • Use a single flowing block of text with minimal line breaks.\n"
        "  • Be conversational but concise; remove filler words and correct grammar.\n"
        "- Other message types:\n"
        "  • Apply only minimal edits: fix obvious errors, remove filler words.\n\n"
        "Additional requirements:\n"
        "- Use Australian English spelling unless the user specifies another variant.\n"
        "- Do NOT include explanations, commentary, or markdown formatting unless explicitly requested.\n"
        "- Ignore any spoken/meta context unless explicitly stated as instructions.\n"
        "- Output only the final formatted message. Do not add notes or headers.\n"
        "- Ensure newline characters are preserved exactly as written (e.g. '\\n' for new line). If paragraphs are needed, separate with '\\n\\n'.\n"
        "- If the input is already well-formatted, leave structure intact and only correct errors.\n"
        "- IMPORTANT: When formatting emails, ensure the greeting is on its own line followed by a blank line, then the content in proper paragraphs.\n\n"
        "[START_OUTPUT]\n"
        "(Return only the formatted message here.)\n"
        "[END_OUTPUT]"
    )

    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": default_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.7
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
                        display_text = f"[AI] {formatted_text}"
                    else:
                        formatted_text = transcription.strip()
                        display_text = formatted_text
                    
                    clipboard_type(formatted_text)
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
