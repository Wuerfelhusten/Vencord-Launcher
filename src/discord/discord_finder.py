"""
Copyright (c) Wuerfelhusten
"""

import logging
import os
import sys
from pathlib import Path


class DiscordFinder:
    """
    Locates the Discord installation directory on Windows.
    """

    log: logging.Logger = logging.getLogger(
        "DiscordFinder"
    )

    @staticmethod
    def find_app_dir() -> Path:
        """
        Finds the latest Discord app-* directory.

        Returns:
            Path: Path to the latest Discord app
                directory.

        Raises:
            SystemExit: If no Discord installation is
                found.
        """

        localappdata = Path(
            os.environ.get("LOCALAPPDATA", "")
        )
        discord_dir: Path = localappdata / "Discord"

        app_dirs: list[Path] = sorted(
            discord_dir.glob("app-*"), reverse=True
        )

        if not app_dirs:
            DiscordFinder.log.error(
                "No Discord app-* folder found."
            )
            sys.exit(1)

        app_dir: Path = app_dirs[0]
        DiscordFinder.log.info(
            f"Found Discord installation: '{app_dir}'"
        )

        return app_dir
