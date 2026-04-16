# VencordLauncher

A lightweight Windows utility that replaces the default Discord entrypoint. It ensures that [Vencord](https://vencord.dev/) and, optionally, [OpenAsar](https://openasar.dev/) stay installed and up to date — even after Discord updates itself.

## Features

- Automatically installs and updates Vencord and OpenAsar
- Downloads the Vencord CLI installer if missing
- Supports `stable`, `ptb` and `canary` branches
- Windows autostart integration (visible in Task Manager)
- Optional minimized Discord launch
- Fully portable — no installation required
- Configurable via a single `config.json`

## Usage

1. Download the latest release from the [Releases](../../releases) tab
2. Edit `config.json` to your liking
3. Run `VencordLauncher.exe`
4. Disable Discord's built-in autostart if you want to use the launcher's autostart instead

## Configuration

`config.json` (located next to the executable):

```jsonc
{
    "branch": "stable",            // stable, ptb or canary
    "OpenAsar": true,              // install OpenAsar alongside Vencord
    "Autostart": false,            // add launcher to Windows startup
    "StartDiscordMinimized": true, // start Discord minimized
    "Debug": false                 // enable debug logging
}
```

## Build

Requires [Python 3.12+](https://www.python.org/) and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
.\build.bat
```

The output will be in `dist\dist\`.

## Project Structure

```
├── assets/              # Icon and static resources
├── data/                # Default config.json
├── logs/                # Log files (latest.log + rotated)
├── src/
│   ├── main.py          # Entry point
│   ├── vencord_launcher.py
│   ├── config/
│   │   ├── config.py          # Pydantic config model
│   │   └── config_loader.py   # JSON5 config loader
│   ├── discord/
│   │   ├── discord_finder.py  # Locates Discord installation
│   │   └── discord_launcher.py
│   ├── utilities/
│   │   ├── autostart_manager.py
│   │   ├── exe_info.py        # Compiled/source detection
│   │   ├── log_formatters.py  # Console and file formatters
│   │   └── process_runner.py  # Subprocess with emoji cleanup
│   └── vencord/
│       ├── vencord_checker.py
│       └── vencord_installer.py
├── build.bat            # Nuitka build script
├── uninstall.py         # Helper to uninstall Vencord/OpenAsar
└── pyproject.toml
```

## Credits

- [Cutleast](https://github.com/Cutleast) — `exe_info.py` is based on code from [cutleast-core-lib](https://github.com/Cutleast/cutleast-core-lib/blob/master/src/cutleast_core_lib/)

## License

See [LICENSE](LICENSE) for details.
