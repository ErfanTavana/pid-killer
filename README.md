# Kill PID (Windows Admin Tool)

<p align="center">
  <img src="logo.ico" alt="Kill PID logo" width="120" />
</p>

A lightweight Windows command-line helper to force-kill processes by PID with automatic Administrator elevation and a hacker-style console UI.

> Binary screenshots are not stored in the repo. Capture your own `docs/cli-screenshot.png` locally (see instructions below).

## Features

- 🔐 **Auto Admin Elevation** – relaunches itself with Administrator privileges using `ShellExecuteW`.
- 🎯 **PID-based termination** – quickly terminate any process by PID using `taskkill /F /T`.
- 🧠 **Pre-kill process inspection** – shows process name, user, memory usage, and executable path before killing (via `psutil`).
- 💻 **Hacker-style colored CLI** – powered by `colorama` with a custom ASCII banner.
- 🪟 **Windows-only** – designed and tested for Windows 10 / 11.

## Requirements

- Windows 10 or 11
- Python 3.10+ (tested on Python 3.12)
- Packages: `colorama`, `psutil`
- Optional: `pyinstaller` for building a standalone `.exe`

Install dependencies:

```bash
pip install colorama psutil pyinstaller
```

## Usage (Python)

Run directly with Python:

```bash
python kill_pid_admin.py
```

The tool will:

1. Check that it is running on Windows.
2. Elevate to Administrator if needed.
3. Show the hacker-style banner.
4. Prompt for a PID in a loop.
5. Display process information (name, user, RAM, path).
6. Ask for confirmation before killing the process.

## Build an EXE with PyInstaller

From the project root:

```bash
pyinstaller --onefile --uac-admin --icon=logo.ico --version-file=version_info.txt kill_pid_admin.py
```

The output executable will be located in the `dist/` folder. You can upload the built EXE as a GitHub Release asset.

## Screenshot

Example hacker-style CLI interface (text preview):

```
 _  __ _ _ _     ___ ___ ___     _ _
| |/ _(_) | |   |_ _| _ \ _ \___| | |_
| |  _| | | |    | ||   /   / -_) |  _|
|_|_| |_|_|_|   |___|_|_\_|_\___|_|\__|

Process info:
PID 4242 | python.exe | user: AdminUser | RAM: 42 MB | path: C:\\Tools\\python.exe

Kill this process? [y/N]:
```

> To include a real screenshot, generate `docs/cli-screenshot.png` locally (e.g., with Snipping Tool) and add it to your fork.

## Security / Disclaimer

⚠ Use at your own risk. Killing critical system processes can cause Windows to become unstable or crash. This tool is intended for advanced users, developers, and system administrators. Do not use this tool on systems you do not own or do not have explicit permission to manage. The author is not responsible for any damage, data loss, or instability caused by misuse.

## Roadmap / Ideas

- Kill by process name (not just PID).
- SAFE / AGGRESSIVE modes (taskkill without `/F /T` vs with).
- Config file (`config.json`) for protected processes and defaults.
- Process history and logging to file.
- Optional simple GUI on top of this CLI core.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
