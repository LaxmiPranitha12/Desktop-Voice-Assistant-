"""Voice Input / Speech Recognition placeholder interface.

Responsible for capturing audio from the microphone and converting it to text.
Implementation will be added during the speech recognition module phase.
"""

from typing import Optional
from src.utils.logger import setup_logger

logger = setup_logger("SpeechRecognizer")


class SpeechRecognizer:
    """Manages audio capture and speech-to-text conversion."""

    def __init__(self) -> None:
        logger.info("SpeechRecognizer initialized (placeholder mode).")

    def listen(self) -> Optional[str]:
        """Captures microphone input and converts speech to text.
        
        Returns:
            Recognized text as a string, or None if no speech detected.
        """
        # Placeholder implementation
        logger.debug("Listening for audio input...")
        return None
