"""General helper functions for PBL Project.
"""

from datetime import datetime


def get_current_time_str() -> str:
    """Returns the current formatted timestamp string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
