import os
import sys
import time
import threading
from pynput.keyboard import HotKey
from pynput import keyboard
from transcriber import WhisperAPITranscriber
from logging_config import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


class HoldHotKey(HotKey):
    def __init__(self, keys, on_activate, on_deactivate):
        self.active = False
        self._keys_pressed = set()

        def _mod_on_activate():
            self.active = True
            on_activate()

        def _mod_on_deactivate():
            self.active = False
            on_deactivate()

        super().__init__(keys, _mod_on_activate)
        self._on_deactivate = _mod_on_deactivate

    def press(self, key):
        self._keys_pressed.add(key)
        super().press(key)

    def release(self, key):
        self._keys_pressed.discard(key)
        super().release(key)
        # If we were active and no more keys are pressed, deactivate
        if self.active and not self._keys_pressed:
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


# key_listener.py - Consolidated hotkey management
class KeyListener:
    def __init__(self, transcriber: WhisperAPITranscriber, email_handler_callback=None):
        self.transcriber = transcriber
        self.recording = False
        self.ai_formatting_requested = False
        self.email_handler_callback = email_handler_callback
        
        # Get hotkeys from environment variables
        normal_hotkey = os.getenv('UTTERTYPE_RECORD_HOTKEYS', '<ctrl>+<alt>+q')
        ai_hotkey = os.getenv('UTTERTYPE_AI_HOTKEYS', '<ctrl>+<alt>+a')
        email_hotkey = os.getenv('UTTERTYPE_EMAIL_HOTKEY', '<ctrl>+<alt>+<shift>+e')
        
        # Email hotkey debouncing
        self.last_email_trigger = 0
        
        # Create global hotkeys for all functionality
        self.hotkeys = {}
        
        # Voice transcription hotkeys using hold-to-record
        self.hotkeys['normal'] = keyboard.GlobalHotKeys({
            normal_hotkey: self._start_normal_recording
        })
        
        self.hotkeys['ai'] = keyboard.GlobalHotKeys({
            ai_hotkey: self._start_ai_recording
        })
        
        # Email formatting hotkey
        if email_handler_callback:
            self.hotkeys['email'] = keyboard.GlobalHotKeys({
                email_hotkey: self._handle_email_hotkey
            })
        
        # Track which keys are currently held down for voice recording
        self.normal_hotkey_held = False
        self.ai_hotkey_held = False
        
        # Create additional listeners for key release detection
        self.key_release_listener = None
    
    def _start_normal_recording(self):
        """Start recording with normal formatting."""
        if not self.recording and not self.normal_hotkey_held:
            logger.info("Normal recording started")
            self.recording = True
            self.ai_formatting_requested = False
            self.normal_hotkey_held = True
            self.transcriber.start_recording()
            self._start_release_listener()
    
    def _start_ai_recording(self):
        """Start recording with AI formatting."""
        if not self.recording and not self.ai_hotkey_held:
            logger.info("AI recording started")
            self.recording = True
            self.ai_formatting_requested = True
            self.ai_hotkey_held = True
            self.transcriber.start_recording()
            self._start_release_listener()
    
    def _start_release_listener(self):
        """Start a listener to detect when hotkeys are released."""
        if self.key_release_listener is None:
            self.key_release_listener = keyboard.Listener(
                on_release=self._on_key_release
            )
            self.key_release_listener.start()
    
    def _on_key_release(self, key):
        """Handle key release events to stop recording."""
        try:
            # Check if any of the hotkey components were released
            key_name = None
            if hasattr(key, 'char'):
                key_name = key.char
            elif hasattr(key, 'name'):
                key_name = key.name
            
            # If any modifier or hotkey letter is released, stop recording
            if key_name in ['ctrl_l', 'ctrl_r', 'alt_l', 'alt_r', 'q', 'a'] and self.recording:
                self._stop_recording()
        except AttributeError:
            pass
    
    def _stop_recording(self):
        """Stop recording."""
        if self.recording:
            logger.info("Recording stopped")
            self.recording = False
            self.normal_hotkey_held = False
            self.ai_hotkey_held = False
            self.transcriber.stop_recording()
            
            # Stop the release listener
            if self.key_release_listener:
                self.key_release_listener.stop()
                self.key_release_listener = None
    
    def _handle_email_hotkey(self):
        """Handle email formatting hotkey with debouncing."""
        current_time = time.time()
        
        # Debounce: ignore if triggered within 2 seconds
        if current_time - self.last_email_trigger < 2.0:
            logger.debug("Email hotkey debounced - ignoring rapid trigger")
            return
            
        self.last_email_trigger = current_time
        logger.info("Email hotkey triggered")
        
        if self.email_handler_callback:
            # Run in separate thread to avoid blocking
            threading.Thread(target=self.email_handler_callback, daemon=True).start()
    
    def start_listeners(self):
        """Start all hotkey listeners."""
        for name, hotkey in self.hotkeys.items():
            hotkey.start()
            logger.debug(f"Started {name} hotkey listener")
    
    def stop_listeners(self):
        """Stop all hotkey listeners."""
        for name, hotkey in self.hotkeys.items():
            hotkey.stop()
            logger.debug(f"Stopped {name} hotkey listener")
        
        # Stop release listener if active
        if self.key_release_listener:
            self.key_release_listener.stop()
            self.key_release_listener = None
    
    def stop_recording(self):
        """Stop recording (called externally when key is released)."""
        self._stop_recording()

    def reset_formatting_flag(self):
        """Reset the formatting flag after transcription is complete."""
        self.ai_formatting_requested = False


class ManualKeyListener:
    """Legacy key listener for systems that need manual key tracking."""
    def __init__(self, transcriber: WhisperAPITranscriber):
        self.transcriber = transcriber
        self.recording = False
        self.ai_formatting_requested = False
        self.pressed_keys = set()
        
        # Get hotkeys from environment variables
        normal_hotkey = os.getenv('UTTERTYPE_RECORD_HOTKEYS', '<ctrl>+<alt>+q')
        ai_hotkey = os.getenv('UTTERTYPE_AI_HOTKEYS', '<ctrl>+<alt>+a')
        
        self.normal_keys = self._parse_hotkey(normal_hotkey)
        self.ai_keys = self._parse_hotkey(ai_hotkey)

    def _parse_hotkey(self, hotkey_str: str) -> set:
        """Parse hotkey string into a set of key names."""
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
            elif key == 'q':
                keys.add('q')
            elif key == 'a':
                keys.add('a')
            elif key == 'e':
                keys.add('e')
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
                # Handle modifier keys correctly
                if key.name == 'ctrl_l' or key.name == 'ctrl_r':
                    self.pressed_keys.add('ctrl')
                elif key.name == 'alt_l' or key.name == 'alt_r':
                    self.pressed_keys.add('alt')
                elif key.name == 'shift_l' or key.name == 'shift_r':
                    self.pressed_keys.add('shift')
                else:
                    self.pressed_keys.add(key.name)
            
            # Only check for hotkeys if we're not already recording
            if not self.recording:
                # Check for exact matches with either hotkey combination
                if self._check_hotkey(self.pressed_keys, self.normal_keys):
                    logger.debug("Normal hotkey detected")
                    self.recording = True
                    self.ai_formatting_requested = False
                    self.transcriber.start_recording()
                elif self._check_hotkey(self.pressed_keys, self.ai_keys):
                    logger.debug("AI hotkey detected")
                    self.recording = True
                    self.ai_formatting_requested = True
                    self.transcriber.start_recording()
        except AttributeError:
            pass

    def release(self, key):
        try:
            # Remove the released key from our set
            if hasattr(key, 'char'):
                self.pressed_keys.discard(key.char)
            elif hasattr(key, 'name'):
                # Handle modifier keys correctly
                if key.name == 'ctrl_l' or key.name == 'ctrl_r':
                    self.pressed_keys.discard('ctrl')
                elif key.name == 'alt_l' or key.name == 'alt_r':
                    self.pressed_keys.discard('alt')
                elif key.name == 'shift_l' or key.name == 'shift_r':
                    self.pressed_keys.discard('shift')
                else:
                    self.pressed_keys.discard(key.name)
            
            # If we were recording, stop recording
            if self.recording:
                self.recording = False
                self.transcriber.stop_recording()
                # Clear all pressed keys to prevent any delayed triggers
                self.pressed_keys.clear()
        except AttributeError:
            pass

    def reset_formatting_flag(self):
        """Reset the formatting flag after transcription is complete."""
        self.ai_formatting_requested = False


def create_keylistener(transcriber: WhisperAPITranscriber, email_handler_callback=None):
    # Check if we're on macOS and using the globe key
    if (sys.platform == "darwin") and (os.getenv('UTTERTYPE_NORMAL_HOTKEY') == "<globe>"):
        return HoldGlobeKey(
            on_activate=transcriber.start_recording,
            on_deactivate=transcriber.stop_recording,
        )
    
    # Always use the new KeyListener with GlobalHotKeys for better reliability
    # The ManualKeyListener is kept as a fallback but not used by default
    return KeyListener(transcriber, email_handler_callback)
