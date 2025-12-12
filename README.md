# Kill PID (Windows Administrator CLI)

## Project Overview
Kill PID is a Windows-only command-line utility that elevates itself to Administrator privileges and terminates a user-specified process ID (PID). The tool inspects the target process before termination, displaying metadata such as name, owner, memory usage, and executable path.

## Key Features
- Administrator self-elevation via `ShellExecuteW` when not already elevated.
- Windows platform guard that exits on non-Windows hosts.
- Process inspection before termination using `psutil` (name, user, memory, executable path).
- Confirmation prompt prior to issuing a forced termination.
- Process killing executed through `taskkill /PID <pid> /F /T` with success and error reporting.
- Colored console output and ASCII banner using `colorama`.

## Architecture / Structure
- `kill_pid_admin.py`: Entry point. Handles platform and elevation checks, input loop, process inspection, confirmation, and termination.
- `requirements.txt`: Runtime dependencies (`colorama`, `psutil`) and optional bundling tool (`pyinstaller`).
- `version_info.txt`: Version metadata consumed by PyInstaller when building a Windows executable.
- `logo.ico`: Icon file referenced during executable packaging.

## How It Works
1. The program starts in `main()` and exits immediately if the host OS is not Windows (`os.name != "nt"`).
2. If not running as Administrator, it relaunches itself with the `runas` verb to obtain elevated privileges, then terminates the original process.
3. After elevation, it clears the console and prints an ASCII banner.
4. A loop prompts for a PID. Inputs of `q`, `quit`, or `exit` end the program; non-numeric or non-positive values are rejected.
5. For a valid PID, `psutil` is queried to gather name, username (best effort), RSS memory usage, and executable path. Missing data is reported as `N/A`.
6. The collected details are shown to the user, who must confirm termination. Only `y` or `yes` proceed.
7. Confirmed requests call `taskkill` with `/F /T` to forcibly terminate the process and any child processes. The tool reports success or displays `taskkill` error output.

## Requirements & Dependencies
- Windows operating system.
- Python 3.x.
- Packages: `colorama`, `psutil`.
- Optional for packaging: `pyinstaller` (uses `logo.ico` and `version_info.txt`).

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## How to Run / Use
Run the script directly:

```bash
python kill_pid_admin.py
```

Interaction flow:
- The script elevates to Administrator if needed and restarts itself.
- Enter a PID when prompted. Invalid input is rejected with an error message.
- Review the displayed process information and confirm with `y` or `yes` to terminate.
- Type `q`, `quit`, or `exit` to stop the loop.

## Packaging with PyInstaller (Windows)
To build a standalone executable (requires PyInstaller installed):

```bash
pyinstaller --onefile --uac-admin --icon=logo.ico --version-file=version_info.txt kill_pid_admin.py
```

The resulting binary is created under `dist/` and inherits metadata from `version_info.txt` and the icon from `logo.ico`.

## Notes & Limitations
- The utility relies on Windows-specific APIs (`ShellExecuteW`) and the `taskkill` command; it will exit on non-Windows systems.
- Process information retrieval depends on `psutil`; missing permissions or terminated processes may result in `N/A` values.
- Termination is forceful (`/F /T`), so use caution to avoid killing critical system processes.
