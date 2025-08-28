import os
import sys
from pynput.keyboard import HotKey
from logging_config import get_logger

logger = get_logger(__name__)


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


def create_keylistener(transcriber, config):
    """Create a key listener using the provided configuration."""
    key_code = config.record_hotkeys

    logger.debug(f"Creating key listener with hotkey: {key_code}")
    
    if (sys.platform == "darwin") and (key_code in ["<globe>", ""]):
        logger.info("Using globe key for macOS")
        return HoldGlobeKey(
            on_activate=transcriber.start_recording,
            on_deactivate=transcriber.stop_recording,
        )

    key_code = key_code if key_code else "<ctrl>+<alt>+v"
    logger.info(f"Using hotkey: {key_code}")

    return HoldHotKey(
          HoldHotKey.parse(key_code),
          on_activate=transcriber.start_recording,
          on_deactivate=transcriber.stop_recording,
      )
