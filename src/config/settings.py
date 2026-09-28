"""Application configuration management.

Loads settings from environment variables and provides structured access across modules.
"""

from dataclasses import dataclass
import os
from pathlib import Path

# Attempt to load dotenv if available, otherwise continue with environment defaults
try:
    from dotenv import load_dotenv
    # Root directory is two levels up from src/config
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    env_path = ROOT_DIR / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except ImportError:
    pass


@dataclass(frozen=True)
class Settings:
    """Central configuration class."""
    assistant_name: str = os.getenv("ASSISTANT_NAME", "Nova")
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Audio & Speech defaults
    audio_device_index: int | None = (
        int(os.getenv("AUDIO_INPUT_DEVICE_INDEX"))
        if os.getenv("AUDIO_INPUT_DEVICE_INDEX") and os.getenv("AUDIO_INPUT_DEVICE_INDEX").strip().isdigit()
        else None
    )
    speech_timeout: int = int(os.getenv("SPEECH_RECOGNITION_TIMEOUT", "5"))
    tts_voice_rate: int = int(os.getenv("TTS_VOICE_RATE", "175"))
    tts_volume: float = float(os.getenv("TTS_VOLUME", "1.0"))


# Global singleton instance for easy import across modules
settings = Settings()
