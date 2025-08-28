import asyncio
import sys
from pynput import keyboard
from transcriber import WhisperAPITranscriber
from table_interface import ConsoleTable
from key_listener import create_keylistener
from dotenv import load_dotenv
from utils import manual_type
from config import get_config, ConfigurationError, validate_environment
from logging_config import get_logger

logger = get_logger(__name__)


async def main():
    """Main application entry point with proper configuration management."""
    # Load environment variables first
    load_dotenv()
    
    try:
        # Load and validate configuration
        config = get_config()
        logger.info("UtterType AI starting up")
        logger.info(f"Using OpenAI model: {config.openai_chat_model}")
        logger.debug(f"Configuration summary: {config.get_summary()}")
        
        # Log any configuration warnings
        if config._validation_warnings:
            logger.warning(f"Configuration has {len(config._validation_warnings)} warnings")
            for warning in config._validation_warnings:
                logger.warning(f"Config warning: {warning}")
        
        # Create transcriber with configuration
        transcriber = WhisperAPITranscriber.create(config)
        hotkey = create_keylistener(transcriber, config)

        keyboard.Listener(on_press=hotkey.press, on_release=hotkey.release).start()
        logger.info("Hotkey listener started")
        logger.info(f"Record hotkey: {config.record_hotkeys}")
        logger.info(f"AI hotkey: {config.ai_hotkeys}")
        logger.info(f"Email hotkey: {config.email_hotkey}")
        
        console_table = ConsoleTable(config)
        with console_table:
            logger.info("Console interface started. Ready for transcriptions.")
            async for transcription, audio_duration_ms in transcriber.get_transcriptions():
                manual_type(transcription.strip())
                console_table.insert(
                    transcription,
                    round(0.0001 * audio_duration_ms / 1000, 6),
                )
                
    except ConfigurationError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease check your .env file or environment variables.")
        print("Run 'python -c \"from config import UtterTypeConfig; print(UtterTypeConfig().to_env_file())\"' for a template.")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error during startup: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}")
        print("Check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
