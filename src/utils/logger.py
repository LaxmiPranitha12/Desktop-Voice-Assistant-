"""Centralized logging setup.
"""

import logging
import sys


def setup_logger(name: str = "PBL_Assistant", level: str = "INFO") -> logging.Logger:
    """Configures and returns a standardized logger instance."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(numeric_level)

        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
