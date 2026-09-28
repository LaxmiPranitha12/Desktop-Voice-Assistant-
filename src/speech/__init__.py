"""Speech processing package (Voice input and Text-to-Speech output).
"""

from .recognition import SpeechRecognizer
from .tts import TextToSpeech

__all__ = ["SpeechRecognizer", "TextToSpeech"]
