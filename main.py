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
import pyautogui
import pyperclip
import time

# main.py - Make model configurable
def format_with_context(text: str) -> str:
    """Format text based on its determined context."""
    client = OpenAI(base_url=os.getenv('OPENAI_BASE_URL'))
    
    # Use configurable model instead of hard-coded
    model = os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o')
    
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

def format_for_email(text: str) -> str:
    """Format and grammar check text specifically for email communication."""
    client = OpenAI(base_url=os.getenv('OPENAI_BASE_URL'))
    
    model = os.getenv('OPENAI_CHAT_MODEL', 'gpt-4o')
    
    prompt = (
        "Review and rewrite the following text for professional email communication. "
        "Fix grammar, spelling, and punctuation errors. "
        "Format appropriately with proper paragraphs and professional tone. "
        "Use Australian English spelling and conventions. "
        "Maintain the original meaning while improving clarity and professionalism. "
        "Output only the corrected text without explanations or comments."
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.2  # Very low temperature for consistent grammar correction
        )
        content = response.choices[0].message.content
        return content.strip() if content else text.strip()
    except Exception as e:
        print(f"Error formatting email text: {e}")
        return text.strip()

def handle_email_formatting():
    """Handle the Ctrl+Alt+Shift+E shortcut for email formatting."""
    try:
        print("Starting email formatting...")
        
        # Store original clipboard content
        original_clipboard = pyperclip.paste()
        
        # Platform-specific copy shortcut
        copy_key = "cmd" if sys.platform == "darwin" else "ctrl"
        
        # Copy current selection to clipboard
        pyautogui.hotkey(copy_key, "c")
        time.sleep(0.5)  # Longer delay to ensure clipboard is updated
        
        # Get the selected text from clipboard
        selected_text = pyperclip.paste()
        
        print(f"Original clipboard length: {len(original_clipboard)}")
        print(f"Selected text length: {len(selected_text)}")
        
        # Check if we actually got new text (different from original clipboard)
        if selected_text.strip() and selected_text != original_clipboard:
            print(f"Processing selected text: {selected_text[:50]}...")
            
            # Format the text for email
            formatted_text = format_for_email(selected_text)
            
            # Copy formatted text to clipboard
            pyperclip.copy(formatted_text)
            
            # Paste the formatted text (replacing the selection)
            pyautogui.hotkey(copy_key, "v")
            
            print(f"Email formatting completed successfully!")
            
        elif selected_text.strip():
            # Text might be the same as clipboard, still process it
            print(f"Processing existing clipboard text: {selected_text[:50]}...")
            formatted_text = format_for_email(selected_text)
            pyperclip.copy(formatted_text)
            pyautogui.hotkey(copy_key, "v")
            print(f"Email formatting completed!")
        else:
            print("No text available for email formatting")
            # Restore original clipboard if nothing was selected
            pyperclip.copy(original_clipboard)
            
    except Exception as e:
        print(f"Error in email formatting: {e}")
        import traceback
        traceback.print_exc()

def format_transcription(transcription, hotkey):
    """Format the transcription based on AI model or return as-is."""
    if hotkey.ai_formatting_requested:
        formatted_text = format_with_context(transcription)
        display_text = f"[AI] {formatted_text}"
    else:
        formatted_text = transcription.strip()
        display_text = formatted_text
    
    return formatted_text, display_text

def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # Create a tkinter dialog to ask the user if they want to use VAD
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    use_vad = messagebox.askyesno("VAD Option", "Would you like to use Voice Activity Detection (VAD)?\n\nYes: Only record when speech is detected.\nNo: Record continuously.")
    root.destroy()

    transcriber = WhisperAPITranscriber.create(use_vad=use_vad)
    
    # Create hotkey listener with email handler callback
    hotkey = create_keylistener(transcriber, handle_email_formatting)
    console_table = ConsoleTable()

    async def transcription_loop():
        with console_table:
            async for transcription, audio_duration_ms in transcriber.get_transcriptions():
                # Add a small delay to prevent rapid processing
                await asyncio.sleep(0.1)
                # Only process if we have a non-empty transcription
                if transcription.strip():
                    formatted_text, display_text = format_transcription(transcription, hotkey)
                    
                    # Copy the formatted text to clipboard
                    pyperclip.copy(formatted_text)
                    
                    # Paste the text
                    pyautogui.hotkey("command" if sys.platform == "darwin" else "ctrl", "v")
                    
                    console_table.insert(
                        display_text,
                        round(0.0003 * audio_duration_ms / 1000, 6),
                    )
                    # Reset the formatting flag after processing
                    hotkey.reset_formatting_flag()

    loop = asyncio.get_event_loop()
    loop.create_task(transcription_loop())

    # Start all hotkey listeners
    hotkey.start_listeners()
    
    print("UtterType AI started...")
    print("Voice transcription: Ctrl+Alt+Q (basic) | Ctrl+Alt+A (AI formatting)")
    print("Email formatting: Ctrl+Alt+Shift+E (select text first)")
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        hotkey.stop_listeners()
        print("\nShutting down...")

if __name__ == "__main__":
    main()
