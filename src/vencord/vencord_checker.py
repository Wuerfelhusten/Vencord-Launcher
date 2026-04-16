"""
Copyright (c) Wuerfelhusten
"""

import logging
from pathlib import Path


class VencordChecker:
    """
    Checks whether Vencord is currently installed in a
    Discord installation.
    """

    log: logging.Logger = logging.getLogger(
        "VencordChecker"
    )

    @staticmethod
    def is_installed(app_dir: Path) -> bool:
        """
        Checks if Vencord is present in the given Discord
        app directory.

        Args:
            app_dir (Path): Path to the Discord app
                directory.

        Returns:
            bool: True if Vencord is installed.
        """

        asar_file: Path = (
            app_dir / "resources" / "_app.asar"
        )
        installed: bool = asar_file.exists()

        status: str = (
            "Installed" if installed else "Not installed"
        )
        VencordChecker.log.info(
            f"Vencord status: '{status}'"
        )

        return installed
