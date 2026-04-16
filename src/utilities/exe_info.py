"""
Copyright (c) Wuerfelhusten
"""

import sys
from pathlib import Path


def is_compiled() -> bool:
    """
    Checks whether the application is running as a
    compiled standalone executable.

    Returns:
        bool: True if running as compiled executable.
    """

    return (
        sys.argv[0].lower().endswith(".exe")
        or getattr(sys, "frozen", False)
    )


def get_exe_path() -> Path:
    """
    Returns the resolved path to the current executable
    or script.

    Returns:
        Path: Path to the executable or script file.
    """

    if is_compiled():
        return Path(sys.argv[0]).resolve()

    return Path(sys.argv[0]).resolve()


def get_base_dir() -> Path:
    """
    Returns the base directory of the application.
    For compiled builds this is the directory containing
    the executable. For source runs this is the project
    root (parent of the src directory).

    Returns:
        Path: Base directory path.
    """

    if is_compiled():
        return Path(sys.argv[0]).resolve().parent

    return Path(__file__).resolve().parent.parent.parent


def get_execution_info() -> tuple[list[str], bool]:
    """
    Returns the execution command and whether the
    application is running as a compiled executable.

    Returns:
        tuple[list[str], bool]: Execution command list
            and compiled flag.
    """

    compiled: bool = is_compiled()

    if compiled:
        return sys.argv, compiled

    cmd: list[str] = [
        sys.executable,
        sys.argv[0].replace("/", "\\"),
        *sys.argv[1:],
    ]

    return cmd, compiled
