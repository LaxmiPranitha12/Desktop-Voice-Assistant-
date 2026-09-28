"""Text-to-Speech (TTS) module.

Responsible for vocalizing responses using pyttsx3.
The implementation is isolated behind a clear interface to allow future engine replacements.
"""

from typing import Optional
import pyttsx3
from src.config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger("TextToSpeech")


class TextToSpeech:
    """Manages voice synthesis and audio playback."""

    def __init__(self) -> None:
        self._engine: Optional[pyttsx3.Engine] = None
        self._is_ready = False
        self._initialize_engine()

    def _initialize_engine(self) -> None:
        """Initializes the pyttsx3 TTS engine and configures voice parameters."""
        try:
            self._engine = pyttsx3.init()
            if self._engine:
                # Configure rate and volume from application settings
                self._engine.setProperty("rate", settings.tts_voice_rate)
                self._engine.setProperty("volume", settings.tts_volume)

                # Prefer female voice (e.g., Microsoft Zira) for Nova if available
                voices = self._engine.getProperty("voices")
                selected_voice = None
                for voice in voices:
                    if "zira" in voice.name.lower() or "female" in voice.name.lower():
                        selected_voice = voice.id
                        break

                if selected_voice:
                    self._engine.setProperty("voice", selected_voice)

                self._is_ready = True
                logger.info(f"TTS engine initialized successfully (Rate: {settings.tts_voice_rate}, Volume: {settings.tts_volume}).")
        except Exception as exc:
            logger.error(f"Failed to initialize pyttsx3 TTS engine: {exc}")
            self._engine = None
            self._is_ready = False

    @property
    def is_ready(self) -> bool:
        """Indicates whether the TTS engine is operational."""
        return self._is_ready

    def speak(self, text: str) -> None:
        """Vocalizes the provided text aloud.

        Args:
            text: The text to be spoken.
        """
        if not text or not text.strip():
            return

        cleaned_text = text.strip()
        logger.info(f"[{settings.assistant_name} Speaking]: {cleaned_text}")

        if not self._is_ready or self._engine is None:
            logger.warning("TTS engine not ready; speaking skipped (fallback to log output).")
            return

        try:
            self._engine.say(cleaned_text)
            self._engine.runAndWait()
        except Exception as exc:
            logger.error(f"Error occurred during speech synthesis: {exc}")
            # Attempt to re-initialize the engine for subsequent calls
            self._initialize_engine()
