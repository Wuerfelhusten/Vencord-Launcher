"""
Copyright (c) Wuerfelhusten
"""

import logging
import winreg
from pathlib import Path


class AutostartManager:
    """
    Manages Windows autostart registry entries for
    the Vencord Launcher.
    """

    log: logging.Logger = logging.getLogger(
        "AutostartManager"
    )

    REG_NAME: str = "VencordLauncher"
    """Registry value name for the autostart entry."""

    REG_KEY: str = (
        r"Software\Microsoft\Windows"
        r"\CurrentVersion\Run"
    )
    """Registry key path for Windows autostart."""

    @staticmethod
    def apply(enabled: bool, exe_path: Path) -> None:
        """
        Adds or removes the autostart registry entry.

        Args:
            enabled (bool): Whether autostart should be
                enabled.
            exe_path (Path): Path to the launcher
                executable.
        """

        AutostartManager.log.info(
            f"Applying autostart:"
            f" enabled='{enabled}',"
            f" exe_path='{exe_path}'"
        )

        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                AutostartManager.REG_KEY,
                0,
                winreg.KEY_SET_VALUE,
            )

            if enabled:
                AutostartManager.log.info(
                    "Enabling autostart..."
                )
                winreg.SetValueEx(
                    key,
                    AutostartManager.REG_NAME,
                    0,
                    winreg.REG_SZ,
                    f'"{exe_path}"',
                )
                AutostartManager.log.info(
                    "Autostart entry added or updated."
                )
            else:
                try:
                    winreg.DeleteValue(
                        key,
                        AutostartManager.REG_NAME,
                    )
                    AutostartManager.log.info(
                        "Autostart entry removed."
                    )
                except FileNotFoundError:
                    AutostartManager.log.info(
                        "No autostart entry found,"
                        " nothing to remove."
                    )

            winreg.CloseKey(key)
        except Exception as exc:
            AutostartManager.log.warning(
                f"Failed to update autostart"
                f" entry: '{exc}'"
            )
