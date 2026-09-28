"""Core Voice Assistant orchestrator.

Coordinates microphone capture, speech recognition, intent routing, and TTS playback.
"""

from typing import Optional
from src.config.settings import settings
from src.intents.parser import CommandParser, IntentResult
from src.speech.microphone import MicrophoneManager
from src.speech.recognition import SpeechRecognizer
from src.speech.tts import TextToSpeech
from src.utils.logger import setup_logger

logger = setup_logger("VoiceAssistant")


class VoiceAssistant:
    """Main orchestrator for the PBL Desktop Voice Assistant."""

    def __init__(
        self,
        recognizer: Optional[SpeechRecognizer] = None,
        tts: Optional[TextToSpeech] = None,
        parser: Optional[CommandParser] = None,
    ) -> None:
        self.name = settings.assistant_name
        logger.info(f"Initializing {self.name} Voice Assistant...")

        # Subsystems
        self.mic_manager = MicrophoneManager(device_index=settings.audio_device_index)
        self.recognizer = recognizer or SpeechRecognizer(mic_manager=self.mic_manager)
        self.tts = tts or TextToSpeech()
        self.parser = parser or CommandParser()
        self.is_running = False

    def start(self) -> None:
        """Starts the assistant and indicates readiness."""
        self.is_running = True
        logger.info(f"{self.name} is now online and ready.")

        # Announce readiness
        ready_message = f"Hello! I am {self.name}. I am ready and listening."
        self.tts.speak(ready_message)

    def process_command(self, query: Optional[str]) -> IntentResult:
        """Processes a single command query string and vocalizes the result.

        Args:
            query: The recognized user speech text (or None/empty).

        Returns:
            IntentResult with execution details and exit flags.
        """
        result = self.parser.parse(query)

        # Only vocalize if a response text exists (silence results in empty response)
        if result.response_text:
            self.tts.speak(result.response_text)

        if result.should_exit:
            self.is_running = False

        return result

    def listen_and_respond(self) -> bool:
        """Performs one single listen -> process -> respond cycle.

        Returns:
            True if the assistant should continue running, False to shut down.
        """
        try:
            # 1. Listen for user voice input
            query = self.recognizer.listen()

            # 2. Process query and respond
            result = self.process_command(query)

            # Check if shutdown was requested
            if result.should_exit:
                return False

            return True

        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received during listen cycle.")
            return False
        except Exception as exc:
            logger.error(f"Error during assistant processing cycle: {exc}", exc_info=True)
            # Do not crash - inform user and continue running
            self.tts.speak("I encountered an internal error, but I am still listening.")
            return True

    def run(self) -> None:
        """Runs the continuous assistant conversation loop."""
        self.start()

        if not self.mic_manager.is_available:
            logger.warning("Microphone is not available. Voice loop cannot proceed with audio input.")
            self.tts.speak("Microphone is not available. Please check your audio settings.")
            self.stop()
            return

        logger.info("Entering active listening loop. Say 'exit' or 'goodbye' to stop.")

        try:
            while self.is_running:
                continue_running = self.listen_and_respond()
                if not continue_running:
                    break
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt caught in main loop.")
        finally:
            self.stop()

    def stop(self) -> None:
        """Stops the assistant gracefully."""
        if self.is_running:
            self.is_running = False
        logger.info(f"{self.name} has shut down cleanly.")
