"""Structured logging configuration."""

import logging
import sys
from rich.logging import RichHandler


def setup_logging(debug: bool = False) -> None:
    handler = RichHandler(
        show_time=True,
        show_path=True,
        markup=True,
        rich_tracebacks=True,
    )
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(message)s",
        handlers=[handler],
        force=True,
    )
