"""PBL Project - Desktop Voice Assistant.

Main entry point for starting the voice assistant application.
"""

import sys
from src.config.settings import settings
from src.core.assistant import VoiceAssistant
from src.utils.logger import setup_logger


def print_banner() -> None:
    """Displays a clean ASCII startup banner."""
    banner = f"""
======================================================
  PBL PROJECT - DESKTOP VOICE ASSISTANT ({settings.assistant_name.upper()})
  Environment: {settings.environment.upper()} | Python: {sys.version.split()[0]}
======================================================
"""
    print(banner)


def main() -> int:
    """Application main execution function."""
    logger = setup_logger("Main", level=settings.log_level)
    print_banner()

    logger.info("Bootstrapping PBL Project foundation...")
    assistant = VoiceAssistant()

    try:
        assistant.start()
        logger.info("Project foundation verified successfully.")
    except KeyboardInterrupt:
        logger.info("Interruption received. Shutting down...")
    finally:
        assistant.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
