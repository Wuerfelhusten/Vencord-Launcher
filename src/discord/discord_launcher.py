"""
Copyright (c) Wuerfelhusten
"""

import logging
import subprocess
import sys
from pathlib import Path


class DiscordLauncher:
    """
    Launches the Discord application.
    """

    log: logging.Logger = logging.getLogger(
        "DiscordLauncher"
    )

    @staticmethod
    def launch(
        app_dir: Path, minimized: bool
    ) -> None:
        """
        Starts Discord from the given app directory.

        Args:
            app_dir (Path): Path to the Discord app
                directory.
            minimized (bool): Whether to start Discord
                minimized.

        Raises:
            SystemExit: If Discord.exe is not found.
        """

        exe_path: Path = app_dir / "Discord.exe"

        if not exe_path.exists():
            DiscordLauncher.log.error(
                "Discord.exe not found in latest"
                " app-* folder."
            )
            sys.exit(1)

        DETACHED: int = (
            subprocess.CREATE_NEW_PROCESS_GROUP
            | subprocess.DETACHED_PROCESS
        )

        if minimized:
            DiscordLauncher.log.info(
                "Starting Discord minimized..."
            )
            proc: subprocess.Popen[bytes] = (
                subprocess.Popen(
                    [
                        str(exe_path),
                        "--start-minimized",
                    ],
                    creationflags=DETACHED,
                    close_fds=True,
                )
            )
        else:
            DiscordLauncher.log.info(
                "Starting Discord..."
            )
            proc = subprocess.Popen(
                [str(exe_path)],
                creationflags=DETACHED,
                close_fds=True,
            )

        DiscordLauncher.log.info(
            f"Discord started (PID: '{proc.pid}')."
        )
