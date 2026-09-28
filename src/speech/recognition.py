"""Speech Recognition module for converting spoken English to text.

Handles microphone capture, ambient noise calibration, and speech-to-text processing.
"""

from typing import Optional
import speech_recognition as sr
from src.config.settings import settings
from src.speech.microphone import MicrophoneManager
from src.utils.logger import setup_logger

logger = setup_logger("SpeechRecognizer")


class SpeechRecognizer:
    """Manages audio capture and speech recognition pipeline."""

    def __init__(self, mic_manager: Optional[MicrophoneManager] = None) -> None:
        self.mic_manager = mic_manager or MicrophoneManager(
            device_index=settings.audio_device_index
        )
        self.recognizer = sr.Recognizer()
        
        # Audio listening parameters to prevent premature cutoff
        self.recognizer.pause_threshold = 1.0
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
        self.recognizer.dynamic_energy_threshold = True

        self._calibrated = False

    def calibrate(self, duration: float = 1.0) -> bool:
        """Calibrates microphone energy threshold for ambient room noise."""
        if not self.mic_manager.is_available:
            logger.warning("Calibration skipped: Microphone is unavailable.")
            return False

        mic = self.mic_manager.get_microphone()
        if mic is None:
            return False

        try:
            logger.info("Calibrating microphone for ambient room noise...")
            with mic as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=duration)
            self._calibrated = True
            logger.info(f"Ambient noise calibration complete (Energy threshold: {self.recognizer.energy_threshold:.1f}).")
            return True
        except Exception as exc:
            logger.warning(f"Ambient noise calibration encountered an issue: {exc}")
            return False

    def listen(self, timeout: Optional[int] = None, phrase_time_limit: int = 10) -> Optional[str]:
        """Listens to the microphone and converts spoken English into text.

        Args:
            timeout: Seconds to wait for speech to start before timing out.
                     Defaults to settings.speech_timeout.
            phrase_time_limit: Maximum allowed phrase duration in seconds.

        Returns:
            Transcribed text in lower-case, or None if no speech / error occurred.
        """
        if not self.mic_manager.is_available:
            logger.error("Microphone is unavailable. Cannot capture audio.")
            return None

        mic = self.mic_manager.get_microphone()
        if mic is None:
            return None

        # Ensure at least one calibration has run
        if not self._calibrated:
            self.calibrate(duration=0.6)

        listen_timeout = timeout if timeout is not None else settings.speech_timeout

        try:
            logger.debug(f"Listening for speech (timeout={listen_timeout}s, limit={phrase_time_limit}s)...")
            with mic as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=listen_timeout,
                    phrase_time_limit=phrase_time_limit
                )

            logger.debug("Audio captured. Sending to speech recognizer...")
            text = self.recognizer.recognize_google(audio, language="en-US")
            cleaned_text = text.strip()
            logger.info(f"Recognized speech: \"{cleaned_text}\"")
            return cleaned_text

        except sr.WaitTimeoutError:
            # Expected when user doesn't say anything within timeout window
            logger.debug("No speech detected within the timeout window.")
            return None

        except sr.UnknownValueError:
            logger.info("Speech was detected but could not be understood.")
            return ""

        except sr.RequestError as exc:
            logger.error(f"Speech recognition service request error: {exc}")
            return None

        except OSError as exc:
            logger.error(f"Microphone audio capture error (OS/Hardware): {exc}")
            return None

        except Exception as exc:
            logger.error(f"Unexpected error during speech recognition: {exc}")
            return None
