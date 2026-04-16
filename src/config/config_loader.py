"""
Copyright (c) Wuerfelhusten
"""

import logging
import sys
from pathlib import Path

import json5

from .config import Config


class ConfigLoader:
    """
    Loads and validates the application configuration
    from a JSON5 file.
    """

    log: logging.Logger = logging.getLogger(
        "ConfigLoader"
    )

    @staticmethod
    def load(config_path: Path) -> Config:
        """
        Loads configuration from the given path.

        Args:
            config_path (Path): Path to the JSON5 config
                file.

        Returns:
            Config: Parsed and validated configuration.

        Raises:
            SystemExit: If the config file is missing or
                contains invalid data.
        """

        if not config_path.exists():
            ConfigLoader.log.error(
                "config.json not found!"
            )
            sys.exit(1)

        with open(config_path, encoding="utf-8") as f:
            raw: dict[str, object] = json5.load(f)

        normalized: dict[str, object] = {
            k.lower(): v for k, v in raw.items()
        }

        if "startdiscordminimized" in normalized:
            normalized["start_discord_minimized"] = (
                normalized.pop("startdiscordminimized")
            )

        if "branch" not in normalized:
            ConfigLoader.log.error(
                "'branch' missing in config.json!"
            )
            sys.exit(1)

        if "openasar" not in normalized:
            ConfigLoader.log.error(
                "'OpenAsar' missing in config.json!"
            )
            sys.exit(1)

        if "autostart" not in normalized:
            ConfigLoader.log.warning(
                "'Autostart' not set in config.json!"
                " Default: False"
            )

        if "start_discord_minimized" not in normalized:
            ConfigLoader.log.warning(
                "'StartDiscordMinimized' not set in"
                " config.json! Default: True"
            )

        config = Config(**normalized)

        ConfigLoader.log.info(
            f"Loaded config."
            f" branch: '{config.branch}' |"
            f" OpenAsar: '{config.openasar}' |"
            f" Autostart: '{config.autostart}' |"
            f" StartDiscordMinimized:"
            f" '{config.start_discord_minimized}'"
        )

        return config
