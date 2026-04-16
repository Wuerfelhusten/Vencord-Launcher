"""
Copyright (c) Wuerfelhusten
"""

import logging
import sys
import time
from pathlib import Path

import json5

from config.config import Config
from config.config_loader import ConfigLoader
from discord.discord_finder import DiscordFinder
from discord.discord_launcher import DiscordLauncher
from utilities.autostart_manager import AutostartManager
from utilities.exe_info import (
    get_base_dir,
    get_exe_path,
    is_compiled,
)
from utilities.log_formatters import (
    ConsoleFormatter,
    FileFormatter,
)
from vencord.vencord_checker import VencordChecker
from vencord.vencord_installer import VencordInstaller


class VencordLauncher:
    """
    Main application class that orchestrates the Vencord
    installation and Discord launch process.
    """

    log: logging.Logger = logging.getLogger(
        "VencordLauncher"
    )

    __base_dir: Path
    __exe_path: Path
    __config_path: Path

    def __init__(self) -> None:
        """
        Initializes the launcher with base directory and
        executable path detection.
        """

        self.__base_dir = get_base_dir()
        self.__exe_path = get_exe_path()

        if is_compiled():
            self.__config_path = (
                self.__base_dir / "config.json"
            )
        else:
            self.__config_path = (
                self.__base_dir / "data"
                / "config.json"
            )

    def run(self) -> None:
        """
        Executes the full launcher workflow.
        """

        self.__setup_logging(
            self.__read_debug_flag()
        )
        self.log.info("VencordLauncher started.")

        config: Config = ConfigLoader.load(
            self.__config_path
        )

        AutostartManager.apply(
            config.autostart, self.__exe_path
        )

        app_dir: Path = DiscordFinder.find_app_dir()

        if VencordChecker.is_installed(app_dir):
            self.log.info(
                "Vencord already present."
                " Launching Discord..."
            )
            DiscordLauncher.launch(
                app_dir,
                config.start_discord_minimized,
            )
            sys.exit(0)

        self.log.info(
            "Vencord not found."
            " Proceeding with installation..."
        )

        cli_path: Path = (
            self.__base_dir
            / "VencordInstallerCli.exe"
        )

        VencordInstaller.ensure_cli(cli_path)
        VencordInstaller.update_cli(cli_path)

        if config.openasar:
            VencordInstaller.install_openasar(
                cli_path, config.branch
            )

        VencordInstaller.install_vencord(
            cli_path, config.branch
        )

        time.sleep(1)

        self.log.info(
            "Launching Discord after Vencord"
            " installation..."
        )
        DiscordLauncher.launch(
            app_dir,
            config.start_discord_minimized,
        )
        sys.exit(0)

    def __read_debug_flag(self) -> bool:
        """
        Reads the debug flag directly from the config
        file before full config parsing. Returns True
        if the file is missing or unreadable.

        Returns:
            bool: Whether debug logging is enabled.
        """

        if not self.__config_path.exists():
            return True

        try:
            with open(
                self.__config_path, encoding="utf-8"
            ) as f:
                raw: dict[str, object] = json5.load(f)

            normalized: dict[str, object] = {
                k.lower(): v for k, v in raw.items()
            }
            return bool(normalized.get("debug", False))
        except Exception:
            return True

    def __setup_logging(
        self, debug: bool
    ) -> None:
        """
        Configures the logging system with console and
        file handlers. Rotates existing latest.log to a
        timestamped name and keeps at most 10 log files.

        Args:
            debug (bool): Whether to enable DEBUG level
                logging. If False, uses INFO level.
        """

        logs_dir: Path = self.__base_dir / "logs"
        logs_dir.mkdir(exist_ok=True)

        latest: Path = logs_dir / "latest.log"

        if latest.exists():
            from datetime import datetime

            timestamp: str = datetime.fromtimestamp(
                latest.stat().st_mtime
            ).strftime("%Y-%m-%d_%H-%M-%S")
            latest.rename(
                logs_dir / f"{timestamp}.log"
            )

        self.__cleanup_logs(logs_dir)

        log_level: int = (
            logging.DEBUG if debug else logging.INFO
        )

        root_logger: logging.Logger = logging.getLogger()
        root_logger.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(
            ConsoleFormatter()
        )

        file_handler = logging.FileHandler(
            latest, encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(FileFormatter())

        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

    @staticmethod
    def __cleanup_logs(
        logs_dir: Path, max_count: int = 10
    ) -> None:
        """
        Deletes the oldest log files if more than
        max_count exist (excluding latest.log).

        Args:
            logs_dir (Path): Path to the logs directory.
            max_count (int): Maximum number of log files
                to keep (including latest.log).
        """

        log_files: list[Path] = sorted(
            [
                f
                for f in logs_dir.glob("*.log")
                if f.name != "latest.log"
            ]
        )

        while len(log_files) >= max_count:
            oldest: Path = log_files.pop(0)
            oldest.unlink()
