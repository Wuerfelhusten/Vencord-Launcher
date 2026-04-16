"""
Copyright (c) Wuerfelhusten
"""

from pydantic import BaseModel


class Config(BaseModel):
    """
    Configuration model for the Vencord Launcher.
    """

    branch: str
    """The Discord branch to target (stable, ptb, canary)."""

    openasar: bool
    """Whether to install OpenAsar alongside Vencord."""

    autostart: bool = False
    """Whether to add the launcher to Windows autostart."""

    start_discord_minimized: bool = True
    """Whether to start Discord minimized."""

    debug: bool = False
    """Whether to enable debug logging."""
