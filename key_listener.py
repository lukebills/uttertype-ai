import os
import sys
from pynput.keyboard import HotKey
from pynput import keyboard
from transcriber import WhisperAPITranscriber


class HoldHotKey(HotKey):
    def __init__(self, keys, on_activate, on_deactivate):
        self.active = False

        def _mod_on_activate():
            self.active = True
            on_activate()

        def _mod_on_deactivate():
            self.active = False
            on_deactivate()

        super().__init__(keys, _mod_on_activate)
        self._on_deactivate = _mod_on_deactivate

    def release(self, key):
        super().release(key)
        if self.active and self._state != self._keys:
            self._on_deactivate()


class HoldGlobeKey:
    """
    For macOS only, globe key requires special handling
    """

    def __init__(self, on_activate, on_deactivate):
        self.held = False
        self._on_activate = on_activate
        self._on_deactivate = on_deactivate

    def press(self, key):
        if hasattr(key, "vk") and key.vk == 63:
            if self.held:  # hold ended
                self._on_deactivate()
            else:  # hold started
                self._on_activate()
            self.held = not self.held

    def release(self, key):
        """Press and release signals are mixed for globe key"""
        self.press(key)


class KeyListener:
    def __init__(self, transcriber: WhisperAPITranscriber):
        self.transcriber = transcriber
        self.recording = False
        self.ai_formatting_requested = False
        self.pressed_keys = set()
        self.current_hotkey = None  # Track which hotkey is active
        
        # Get hotkey combinations from .env
        normal_hotkey = os.getenv('UTTERTYPE_NORMAL_HOTKEY', '<ctrl>+<alt>+v')
        ai_hotkey = os.getenv('UTTERTYPE_AI_HOTKEY', '<ctrl>+<alt>+b')
        
        # Parse hotkey combinations
        self.normal_keys = self._parse_hotkey(normal_hotkey)
        self.ai_keys = self._parse_hotkey(ai_hotkey)

    def _parse_hotkey(self, hotkey_str: str) -> set:
        """Parse hotkey string from .env into a set of key names."""
        keys = set()
        for key in hotkey_str.split('+'):
            key = key.strip().lower()
            if key == '<ctrl>':
                keys.add('ctrl')
            elif key == '<shift>':
                keys.add('shift')
            elif key == '<alt>':
                keys.add('alt')
            elif key == '<space>':
                keys.add('space')
            elif key == 'v':
                keys.add('v')
            elif key == 'b':
                keys.add('b')
            # Add more key mappings as needed
        return keys

    def _check_hotkey(self, pressed_keys: set, target_keys: set) -> bool:
        """Check if the currently pressed keys match the target hotkey combination."""
        return pressed_keys == target_keys

    def press(self, key):
        try:
            # Add the pressed key to our set
            if hasattr(key, 'char'):
                self.pressed_keys.add(key.char)
            elif hasattr(key, 'name'):
                self.pressed_keys.add(key.name)
            
            # Only check for hotkeys if we have exactly the right number of keys pressed
            # and we're not already recording
            if not self.recording:
                if len(self.pressed_keys) == len(self.normal_keys):  # Check exact match for normal hotkey
                    if self._check_hotkey(self.pressed_keys, self.normal_keys):
                        self.recording = True
                        self.ai_formatting_requested = False
                        self.current_hotkey = 'normal'
                        self.transcriber.start_recording()
                elif len(self.pressed_keys) == len(self.ai_keys):  # Check exact match for AI hotkey
                    if self._check_hotkey(self.pressed_keys, self.ai_keys):
                        self.recording = True
                        self.ai_formatting_requested = True
                        self.current_hotkey = 'ai'
                        self.transcriber.start_recording()
        except AttributeError:
            pass

    def release(self, key):
        try:
            # Remove the released key from our set
            if hasattr(key, 'char'):
                self.pressed_keys.discard(key.char)
            elif hasattr(key, 'name'):
                self.pressed_keys.discard(key.name)
            
            # If we were recording and any of the hotkey keys were released, stop recording
            if self.recording:
                if self.current_hotkey == 'normal' and not self._check_hotkey(self.pressed_keys, self.normal_keys):
                    self.recording = False
                    self.transcriber.stop_recording()
                elif self.current_hotkey == 'ai' and not self._check_hotkey(self.pressed_keys, self.ai_keys):
                    self.recording = False
                    self.transcriber.stop_recording()
        except AttributeError:
            pass

    def reset_formatting_flag(self):
        """Reset the formatting flag after transcription is complete."""
        self.ai_formatting_requested = False
        self.current_hotkey = None


def create_keylistener(transcriber: WhisperAPITranscriber) -> KeyListener:
    # Check if we're on macOS and using the globe key
    if (sys.platform == "darwin") and (os.getenv('UTTERTYPE_NORMAL_HOTKEY') == "<globe>"):
        return HoldGlobeKey(
            on_activate=transcriber.start_recording,
            on_deactivate=transcriber.stop_recording,
        )
    
    # Create the KeyListener with both normal and AI hotkey support
    return KeyListener(transcriber)
