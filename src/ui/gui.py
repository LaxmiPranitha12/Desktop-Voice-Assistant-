"""Desktop GUI placeholder module.

Provides a skeleton for future desktop graphic interfaces (e.g., PyQt, CustomTkinter, or Tkinter).
"""

from src.utils.logger import setup_logger

logger = setup_logger("AssistantGUI")


class AssistantGUI:
    """Desktop Graphical User Interface manager."""

    def __init__(self) -> None:
        logger.info("AssistantGUI initialized (placeholder mode).")

    def run(self) -> None:
        """Launches the graphical user interface."""
        logger.info("Starting GUI event loop (placeholder)...")
