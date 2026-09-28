"""Dedicated microphone and audio input device management.

Handles detection, validation, and access to audio input devices.
"""

from typing import List, Optional
import speech_recognition as sr
from src.config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger("MicrophoneManager")


class MicrophoneManager:
    """Manages audio input hardware and microphone configuration."""

    def __init__(self, device_index: Optional[int] = None) -> None:
        self.device_index = device_index
        self._is_available = False
        self._mic_name = "Unknown"
        self._initialize()

    def _initialize(self) -> None:
        """Checks for available microphone devices and verifies access."""
        try:
            available_mics = sr.Microphone.list_microphone_names()
            if not available_mics:
                logger.warning("No microphone input devices detected on this system.")
                self._is_available = False
                return

            if self.device_index is not None:
                if 0 <= self.device_index < len(available_mics):
                    self._mic_name = available_mics[self.device_index]
                    self._is_available = True
                    logger.info(f"Using configured microphone [{self.device_index}]: {self._mic_name}")
                else:
                    logger.warning(
                        f"Configured device index {self.device_index} out of range (0-{len(available_mics)-1}). "
                        "Falling back to system default."
                    )
                    self.device_index = None

            if self.device_index is None:
                # Test default microphone access
                self._mic_name = available_mics[0] if available_mics else "Default Microphone"
                self._is_available = True
                logger.info(f"Default microphone detected: {self._mic_name}")

        except Exception as exc:
            logger.error(f"Failed to initialize microphone subsystem: {exc}")
            self._is_available = False

    @property
    def is_available(self) -> bool:
        """Returns True if a working microphone was detected."""
        return self._is_available

    @property
    def device_name(self) -> str:
        """Returns the name of the active microphone."""
        return self._mic_name

    def get_microphone(self) -> Optional[sr.Microphone]:
        """Creates and returns a speech_recognition Microphone instance.
        
        Returns:
            sr.Microphone instance, or None if initialization failed.
        """
        if not self._is_available:
            logger.error("Cannot create Microphone instance: No valid input device available.")
            return None

        try:
            return sr.Microphone(device_index=self.device_index)
        except Exception as exc:
            logger.error(f"Error opening microphone device: {exc}")
            return None

    @staticmethod
    def list_devices() -> List[str]:
        """Returns a list of all detected microphone device names."""
        try:
            return sr.Microphone.list_microphone_names()
        except Exception as exc:
            logger.error(f"Error querying microphone devices: {exc}")
            return []
