"""
Copyright (c) Wuerfelhusten
"""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """
    Uninstalls Vencord and OpenAsar from the configured
    Discord branch. Uses the VencordInstallerCli.exe
    located next to this script or in the dist folder.
    """

    base_dir: Path = Path(__file__).resolve().parent
    cli_path: Path = base_dir / "VencordInstallerCli.exe"

    if not cli_path.exists():
        cli_path = (
            base_dir
            / "dist"
            / "main.dist"
            / "VencordInstallerCli.exe"
        )

    if not cli_path.exists():
        print(
            "ERROR: VencordInstallerCli.exe not found."
        )
        sys.exit(1)

    branch: str = "stable"

    if len(sys.argv) > 1:
        branch = sys.argv[1]

    print(f"Uninstalling Vencord ({branch})...")

    try:
        subprocess.run(
            [
                str(cli_path),
                "-uninstall",
                "-branch",
                branch,
            ],
            check=True,
        )
        print("Vencord uninstalled.")
    except subprocess.CalledProcessError as exc:
        print(f"Failed to uninstall Vencord: {exc}")

    print(f"Uninstalling OpenAsar ({branch})...")

    try:
        subprocess.run(
            [
                str(cli_path),
                "-uninstall-openasar",
                "-branch",
                branch,
            ],
            check=True,
        )
        print("OpenAsar uninstalled.")
    except subprocess.CalledProcessError as exc:
        print(f"Failed to uninstall OpenAsar: {exc}")

    print("Done.")


if __name__ == "__main__":
    main()
