"""
Copyright (c) Wuerfelhusten
"""

import logging
from typing import override

OWN_LOGGERS: set[str] = {
    "VencordLauncher",
    "ConfigLoader",
    "AutostartManager",
    "DiscordFinder",
    "DiscordLauncher",
    "VencordChecker",
    "VencordInstaller",
    "ProcessRunner",
}
"""Set of logger names owned by this application."""


class ConsoleFormatter(logging.Formatter):
    """
    Formatter for console output without timestamps.
    Marks external library logs with their logger name
    as prefix.
    """

    @override
    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record for console output.

        Args:
            record (logging.LogRecord): The log record
                to format.

        Returns:
            str: Formatted log line.
        """

        msg: str = record.getMessage()

        if record.name not in OWN_LOGGERS:
            msg = f"[{record.name}] {msg}"

        return f"{record.levelname} | {msg}"


class FileFormatter(logging.Formatter):
    """
    Formatter for file output with full timestamps.
    Marks external library logs with their logger name
    as prefix.
    """

    @override
    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record for file output.

        Args:
            record (logging.LogRecord): The log record
                to format.

        Returns:
            str: Formatted log line with timestamp.
        """

        msg: str = record.getMessage()
        timestamp: str = self.formatTime(
            record, "%Y-%m-%d %H:%M:%S"
        )

        if record.name not in OWN_LOGGERS:
            msg = f"[{record.name}] {msg}"

        return f"[{timestamp}] {record.levelname} | {msg}"
