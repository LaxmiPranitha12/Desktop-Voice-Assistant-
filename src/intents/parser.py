"""Command and Intent Processing module.

Identifies user intent from recognized text and coordinates with the response system.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional
from src.intents.basic_responses import BasicResponseSystem, ResponseResult
from src.utils.logger import setup_logger

logger = setup_logger("CommandParser")


@dataclass
class IntentResult:
    """Structure representing a parsed intent and its execution metadata."""
    intent_name: str
    confidence: float
    parameters: Dict[str, Any]
    response_text: str
    should_exit: bool = False


class CommandParser:
    """Parses text commands and resolves them into structured intents."""

    def __init__(self) -> None:
        self.response_system = BasicResponseSystem()
        logger.info("CommandParser initialized with BasicResponseSystem.")

    def parse(self, text: Optional[str]) -> IntentResult:
        """Parses input text to determine the intent and corresponding response.

        Args:
            text: The user command string (or None/empty).

        Returns:
            IntentResult containing intent name, response text, and flow control.
        """
        response: ResponseResult = self.response_system.get_response(text)
        
        confidence = 1.0 if response.intent not in ("unknown", "unintelligible", "silence") else 0.0

        return IntentResult(
            intent_name=response.intent,
            confidence=confidence,
            parameters={"raw_text": text or ""},
            response_text=response.text,
            should_exit=response.should_exit,
        )
