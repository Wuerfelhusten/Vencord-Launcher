"""
Copyright (c) Wuerfelhusten
"""

import logging
import re
import subprocess
from pathlib import Path


EMOJI_PATTERN: re.Pattern[str] = re.compile(
    "["
    "\U0001f600-\U0001f64f"
    "\U0001f300-\U0001f5ff"
    "\U0001f680-\U0001f6ff"
    "\U0001f1e0-\U0001f1ff"
    "\U00002702-\U000027b0"
    "\U000024c2-\U0001f251"
    "\U00002600-\U000026ff"
    "\U00002700-\U000027bf"
    "\U0000fe00-\U0000fe0f"
    "\U0001f900-\U0001f9ff"
    "\U0001fa00-\U0001fa6f"
    "\U0001fa70-\U0001faff"
    "\u200d\u2640\u2642\u2b50"
    "\u2714\u274c\u2728"
    "]+",
    re.UNICODE,
)
"""Regex pattern to match common emoji characters."""


class ProcessRunner:
    """
    Runs subprocesses and routes their output through
    the logging system with emoji stripping.
    """

    log: logging.Logger = logging.getLogger(
        "ProcessRunner"
    )

    @staticmethod
    def run(
        args: list[str],
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        """
        Runs a subprocess, captures its output, logs
        each line through the logging system after
        stripping emojis.

        Args:
            args (list[str]): Command and arguments to
                execute.
            check (bool): Whether to raise on non-zero
                exit code.

        Returns:
            subprocess.CompletedProcess[str]: The
                completed process result.

        Raises:
            subprocess.CalledProcessError: If check is
                True and the process returns non-zero.
        """

        result: subprocess.CompletedProcess[str] = (
            subprocess.run(
                args,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        )

        ProcessRunner.__log_output(result.stdout)
        ProcessRunner.__log_output(result.stderr)

        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode, args
            )

        return result

    @staticmethod
    def __log_output(
        output: str | None,
    ) -> None:
        """
        Logs each non-empty line of subprocess output
        after cleaning emojis and whitespace.

        Args:
            output (str | None): Raw subprocess output.
        """

        if not output:
            return

        for line in output.splitlines():
            cleaned: str = EMOJI_PATTERN.sub(
                "", line
            ).strip()

            if cleaned:
                ProcessRunner.log.info(cleaned)
