"""
Copyright (c) Wuerfelhusten
"""

import logging
import subprocess
import sys
import urllib.request
from pathlib import Path

from utilities.process_runner import ProcessRunner


class VencordInstaller:
    """
    Handles downloading and running the Vencord CLI
    installer.
    """

    log: logging.Logger = logging.getLogger(
        "VencordInstaller"
    )

    DOWNLOAD_URL: str = (
        "https://github.com/Vencord/Installer"
        "/releases/latest/download"
        "/VencordInstallerCli.exe"
    )
    """URL for the latest Vencord CLI installer."""

    @staticmethod
    def ensure_cli(cli_path: Path) -> None:
        """
        Downloads the Vencord CLI installer if it does
        not exist locally.

        Args:
            cli_path (Path): Expected path of the CLI
                executable.

        Raises:
            SystemExit: If the download fails.
        """

        if cli_path.exists():
            return

        VencordInstaller.log.warning(
            "VencordInstallerCli.exe not found."
            " Downloading latest version..."
        )

        try:
            urllib.request.urlretrieve(
                VencordInstaller.DOWNLOAD_URL,
                str(cli_path),
            )
            VencordInstaller.log.info(
                "Downloaded VencordInstallerCli.exe"
                " successfully."
            )
        except Exception as exc:
            VencordInstaller.log.error(
                "Failed to download"
                f" VencordInstallerCli.exe: '{exc}'"
            )
            sys.exit(1)

    @staticmethod
    def update_cli(cli_path: Path) -> None:
        """
        Runs the CLI self-update command.

        Args:
            cli_path (Path): Path to the CLI executable.
        """

        VencordInstaller.log.info(
            "Checking for VencordInstallerCli"
            " updates..."
        )

        try:
            ProcessRunner.run(
                [str(cli_path), "-update-self"],
            )
        except subprocess.CalledProcessError:
            VencordInstaller.log.warning(
                "VencordInstallerCli self-update failed"
                " or no update available."
            )

    @staticmethod
    def install_openasar(
        cli_path: Path, branch: str
    ) -> None:
        """
        Installs OpenAsar for the specified Discord
        branch.

        Args:
            cli_path (Path): Path to the CLI executable.
            branch (str): Discord branch to target.

        Raises:
            SystemExit: If the installation fails.
        """

        VencordInstaller.log.info(
            f"Installing OpenAsar for branch"
            f" '{branch}'..."
        )

        try:
            ProcessRunner.run(
                [
                    str(cli_path),
                    "-install-openasar",
                    "-branch",
                    branch,
                ],
            )
        except subprocess.CalledProcessError as exc:
            VencordInstaller.log.error(
                f"Error installing OpenAsar: '{exc}'"
            )
            sys.exit(1)

    @staticmethod
    def install_vencord(
        cli_path: Path, branch: str
    ) -> None:
        """
        Patches Discord with Vencord for the specified
        branch.

        Args:
            cli_path (Path): Path to the CLI executable.
            branch (str): Discord branch to target.

        Raises:
            SystemExit: If the installation fails.
        """

        VencordInstaller.log.info(
            f"Patching Discord ('{branch}')..."
        )

        try:
            ProcessRunner.run(
                [
                    str(cli_path),
                    "-install",
                    "-branch",
                    branch,
                ],
            )
        except subprocess.CalledProcessError as exc:
            VencordInstaller.log.error(
                f"Error installing Vencord: '{exc}'"
            )
            sys.exit(1)
