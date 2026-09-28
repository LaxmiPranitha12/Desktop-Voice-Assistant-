"""PBL Project - Desktop Voice Assistant.

Main entry point for starting the voice assistant application.
"""

import argparse
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
    parser = argparse.ArgumentParser(description="PBL Project - Desktop Voice Assistant")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single listen-and-respond cycle instead of continuous loop.",
    )
    args = parser.parse_args()

    logger = setup_logger("Main", level=settings.log_level)
    print_banner()

    logger.info("Initializing voice assistant...")
    assistant = VoiceAssistant()

    try:
        if args.once:
            assistant.start()
            logger.info("Running single test cycle...")
            assistant.listen_and_respond()
            assistant.stop()
        else:
            assistant.run()
    except KeyboardInterrupt:
        logger.info("Shutdown requested via KeyboardInterrupt.")
    finally:
        assistant.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
