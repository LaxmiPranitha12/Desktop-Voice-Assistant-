"""Predefined response mappings and generator for Phase 2.

Handles direct conversational queries with simple, deterministic responses.
No external AI or LLM is involved.
"""

from dataclasses import dataclass
from typing import Optional
from src.config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger("ResponseSystem")


@dataclass
class ResponseResult:
    """Encapsulates the response text and state flags."""
    text: str
    intent: str
    should_exit: bool = False


class BasicResponseSystem:
    """Generates predefined conversational responses based on normalized input commands."""

    def __init__(self) -> None:
        self.assistant_name = settings.assistant_name

    def get_response(self, query: Optional[str]) -> ResponseResult:
        """Determines the appropriate predefined response for a query.

        Args:
            query: The recognized text string, or None/empty.

        Returns:
            ResponseResult containing the text to vocalize and flow-control flags.
        """
        if query is None:
            # Silence / timeout case: no response needed to avoid unsolicited speaking
            return ResponseResult(text="", intent="silence", should_exit=False)

        normalized = query.strip().lower()

        # Handle speech detected but not understood
        if not normalized:
            return ResponseResult(
                text="I didn't catch that. Could you please repeat?",
                intent="unintelligible",
                should_exit=False,
            )

        # Check for shutdown commands
        if any(cmd in normalized for cmd in ["exit", "quit", "goodbye", "bye nova", "shut down", "stop"]):
            logger.info("Shutdown command detected.")
            return ResponseResult(
                text="Goodbye! Have a great day.",
                intent="shutdown",
                should_exit=True,
            )

        # Greetings
        if any(cmd in normalized for cmd in ["hello nova", "hi nova", "hey nova", "hello", "hi", "hey"]):
            return ResponseResult(
                text="Hello! How can I help you?",
                intent="greeting",
                should_exit=False,
            )

        # Status inquiry
        if any(cmd in normalized for cmd in ["how are you", "how are you doing", "how's it going"]):
            return ResponseResult(
                text="I'm doing well. What can I do for you?",
                intent="status",
                should_exit=False,
            )

        # Identity inquiry
        if any(cmd in normalized for cmd in ["who are you", "what is your name", "what's your name"]):
            return ResponseResult(
                text=f"I'm {self.assistant_name}, your voice assistant.",
                intent="identity",
                should_exit=False,
            )

        # Capabilities inquiry
        if any(cmd in normalized for cmd in ["what can you do", "help", "what are your features"]):
            return ResponseResult(
                text=f"I'm {self.assistant_name}. I can listen to your voice and respond to basic queries.",
                intent="capabilities",
                should_exit=False,
            )

        # Unrecognized sentence
        logger.info(f"Unrecognized query: '{query}'")
        return ResponseResult(
            text="I'm sorry, I didn't quite catch that. Could you please repeat?",
            intent="unknown",
            should_exit=False,
        )
