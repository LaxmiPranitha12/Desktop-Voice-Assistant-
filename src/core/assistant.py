"""Core Voice Assistant orchestrator.

Coordinates input, intent routing, skills execution, and speech response.
"""

from src.config.settings import settings
from src.intents.parser import CommandParser
from src.skills.browser_actions import BrowserActions
from src.skills.system_actions import SystemActions
from src.speech.recognition import SpeechRecognizer
from src.speech.tts import TextToSpeech
from src.utils.logger import setup_logger

logger = setup_logger("VoiceAssistant")


class VoiceAssistant:
    """Main orchestrator for the PBL Voice Assistant."""

    def __init__(self) -> None:
        self.name = settings.assistant_name
        logger.info(f"Initializing {self.name} Core Engine...")
        
        # Subsystem placeholders
        self.recognizer = SpeechRecognizer()
        self.tts = TextToSpeech()
        self.parser = CommandParser()
        self.system_actions = SystemActions()
        self.browser_actions = BrowserActions()
        self.is_running = False

    def start(self) -> None:
        """Starts the assistant lifecycle."""
        self.is_running = True
        logger.info(f"{self.name} is now online and ready (Foundation Mode).")
        self.tts.speak(f"Hello! {self.name} foundation is initialized.")

    def stop(self) -> None:
        """Stops the assistant gracefully."""
        self.is_running = False
        logger.info(f"{self.name} has shut down.")
