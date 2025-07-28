import pyaudio

def list_audio_devices():
    p = pyaudio.PyAudio()
    print("\nAvailable Audio Devices:")
    print("-----------------------")
    
    for i in range(p.get_device_count()):
        dev_info = p.get_device_info_by_index(i)
        print(f"\nDevice {i}:")
        print(f"  Name: {dev_info.get('name', 'Unknown')}")
        print(f"  Input Channels: {dev_info.get('maxInputChannels', 0)}")
        print(f"  Output Channels: {dev_info.get('maxOutputChannels', 0)}")
        print(f"  Default Input: {dev_info.get('defaultInputDevice', False)}")
        print(f"  Default Output: {dev_info.get('defaultOutputDevice', False)}")
    
    p.terminate()

if __name__ == "__main__":
    list_audio_devices() 