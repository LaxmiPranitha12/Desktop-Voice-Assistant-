"""Speech processing package (Voice input and Text-to-Speech output).
"""

from .microphone import MicrophoneManager
from .recognition import SpeechRecognizer
from .tts import TextToSpeech

__all__ = ["MicrophoneManager", "SpeechRecognizer", "TextToSpeech"]
