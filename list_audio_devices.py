import pyaudio
from logging_config import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

def list_audio_devices():
    p = pyaudio.PyAudio()
    logger.info("Available Audio Devices:")
    logger.info("-" * 23)
    
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        logger.info(f"Device {i}:")
        logger.info(f"  Name: {dev_info.get('name', 'Unknown')}")
        logger.info(f"  Input Channels: {dev_info.get('maxInputChannels', 0)}")
        logger.info(f"  Output Channels: {dev_info.get('maxOutputChannels', 0)}")
        logger.info(f"  Default Input: {dev_info.get('defaultInputDevice', False)}")
        logger.info(f"  Default Output: {dev_info.get('defaultOutputDevice', False)}")
    
    p.terminate()

if __name__ == "__main__":
    list_audio_devices() 