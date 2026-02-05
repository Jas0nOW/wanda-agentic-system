"""Structured logging configuration for WANDA Voice Core.

Replaces print statements with proper logging for production use.
"""

from __future__ import annotations
import logging
import sys
from pathlib import Path
from typing import Optional

# Default log format
DEFAULT_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Module-specific log levels
MODULE_LEVELS = {
    "wanda_voice_core.engine": logging.INFO,
    "wanda_voice_core.providers.gemini_cli": logging.INFO,
    "wanda_voice_core.refiner": logging.WARNING,
    "wanda_voice_core.safety": logging.INFO,
    "wanda_voice_core.router": logging.INFO,
    "wanda_voice_core.event_bus": logging.WARNING,
}


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    format_string: str = DEFAULT_FORMAT,
    module_levels: Optional[dict[str, int]] = None,
) -> logging.Logger:
    """Configure structured logging for WANDA.

    Args:
        level: Default logging level
        log_file: Optional file path for logging
        format_string: Log format string
        module_levels: Module-specific log levels

    Returns:
        Root logger instance
    """
    # Get root logger for wanda_voice_core
    logger = logging.getLogger("wanda_voice_core")
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(format_string, datefmt=DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)  # Always log debug to file
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt=DATE_FORMAT,
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Set module-specific levels
    levels = module_levels or MODULE_LEVELS
    for module, module_level in levels.items():
        logging.getLogger(module).setLevel(module_level)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LogContext:
    """Context manager for temporary log level changes."""

    def __init__(self, logger_name: str, level: int):
        self.logger = logging.getLogger(logger_name)
        self.original_level = self.logger.level
        self.temporary_level = level

    def __enter__(self):
        self.logger.setLevel(self.temporary_level)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(self.original_level)
        return False
