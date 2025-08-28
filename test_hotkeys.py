#!/usr/bin/env python3
"""
Test script for UtterType AI hotkeys
This sc    # Load environment variables if .env exists
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        logger.info("Loaded configuration from .env file")
    else:
        logger.warning("No .env file found, using default hotkeys")
    
    logger.info("UtterType AI Hotkey Test")
    logger.info("=" * 40)
    
    test_hotkeys()st the hotkey detection without requiring the full transcription setup.
"""

import os
import time
from dotenv import load_dotenv
from pynput import keyboard
from logging_config import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

class MockTranscriber:
    """Mock transcriber for testing purposes."""
    def start_recording(self):
        logger.info("🎤 Mock recording started!")
    
    def stop_recording(self):
        logger.info("⏹️ Mock recording stopped!")

def mock_email_handler():
    """Mock email handler for testing purposes."""
    logger.info("📧 Mock email formatting triggered!")

def test_hotkeys():
    """Test individual hotkeys using GlobalHotKeys directly."""
    
    # Get hotkey configuration
    normal_hotkey = os.getenv('UTTERTYPE_RECORD_HOTKEYS', '<ctrl>+<alt>+q')
    ai_hotkey = os.getenv('UTTERTYPE_AI_HOTKEYS', '<ctrl>+<alt>+a')
    email_hotkey = os.getenv('UTTERTYPE_EMAIL_HOTKEY', '<ctrl>+<alt>+<shift>+e')
    
    logger.info(f"Testing hotkeys:")
    logger.info(f"  Normal recording: {normal_hotkey}")
    logger.info(f"  AI recording: {ai_hotkey}")
    logger.info(f"  Email formatting: {email_hotkey}")
    
    # Create test functions
    def test_normal():
        logger.info("✅ Normal recording hotkey triggered!")
    
    def test_ai():
        logger.info("✅ AI recording hotkey triggered!")
    
    def test_email():
        logger.info("✅ Email formatting hotkey triggered!")
    
    # Create hotkey listeners
    hotkeys = [
        keyboard.GlobalHotKeys({normal_hotkey: test_normal}),
        keyboard.GlobalHotKeys({ai_hotkey: test_ai}),
        keyboard.GlobalHotKeys({email_hotkey: test_email})
    ]
    
    # Start all listeners
    for hotkey in hotkeys:
        hotkey.start()
    
    logger.info("Hotkey listeners started! Press the hotkeys to test them.")
    logger.info("Press Ctrl+C to exit.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping hotkey listeners...")
        for hotkey in hotkeys:
            hotkey.stop()
        logger.info("Test completed!")

def main():
    # Load environment variables if .env exists
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print("Loaded configuration from .env file")
    else:
        print("No .env file found, using default hotkeys")
    
    print("UtterType AI Hotkey Test")
    print("=" * 40)
    
    test_hotkeys()

if __name__ == "__main__":
    main()
