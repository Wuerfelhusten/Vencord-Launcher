"""
Copyright (c) Wuerfelhusten
"""

from vencord_launcher import VencordLauncher


def main() -> None:
    """
    Entry point for the Vencord Launcher application.
    """

    launcher: VencordLauncher = VencordLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
