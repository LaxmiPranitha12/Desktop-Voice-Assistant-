"""Text-to-Speech (TTS) placeholder interface.

Responsible for vocalizing system responses to the user.
Implementation will be added during the speech synthesis module phase.
"""

from src.utils.logger import setup_logger

logger = setup_logger("TextToSpeech")


class TextToSpeech:
    """Manages text synthesis and audio output."""

    def __init__(self) -> None:
        logger.info("TextToSpeech initialized (placeholder mode).")

    def speak(self, text: str) -> None:
        """Converts text to spoken audio.
        
        Args:
            text: The text message to speak aloud.
        """
        # Placeholder implementation - logs output until audio engine is wired up
        logger.info(f"[TTS Output]: {text}")
