# Kill PID (Windows Admin CLI)

Force-terminate Windows processes by PID with a colorful console interface and automatic Administrator elevation.

<p align="center">
  <img src="logo.ico" alt="Kill PID logo" width="120" />
</p>

## Overview
- Windows-only Python script that relaunches itself with UAC elevation when needed.
- Shows an ASCII banner, prompts for a PID, prints process details (name, user, memory, executable path), and then confirms before killing.
- Uses `taskkill /PID <pid> /F /T` for termination and `psutil` for process inspection.

## Requirements
- Windows 10/11
- Python 3.10+ (Python executable or a PyInstaller-built EXE)
- Dependencies: `colorama`, `psutil` (PyInstaller is optional for packaging)

Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage (run with Python)
From a Windows shell in the project directory:
```bash
python kill_pid_admin.py
```
Execution flow:
1) Script exits immediately on non-Windows platforms.
2) If not elevated, it relaunches itself via `ShellExecuteW(..., "runas", ...)` and exits the original process.
3) Clears the screen and prints the banner.
4) Prompts repeatedly for a PID (accepts `q`, `quit`, or `exit` to stop).
5) Displays target process info; if the PID does not exist, it reports the error and reprompts.
6) After "y/yes" confirmation, calls `taskkill /PID <pid> /F /T` and prints the result.

Example session (text only):
```
  _  __ _ _ _      ____ ___ ____   ____ ___
 | |/ /(_) | | ___|  _ \_ _|  _ \ / ___|_ _|
 | '/ | | | |/ _ \ |_) | || | | | |    | |
 | . \ | | | |  __/  __/| || |_| | |___ | |
 |_|\_\|_|_|_|\___|_|  |___|____/ \____|___|
        KILL PID TOOL  |  Windows Admin
------------------------------------------------------------
[INFO] Windows PID termination utility with Admin elevation
[INFO] Type 'q' or 'quit' or 'exit' to leave the program
------------------------------------------------------------
[PID] Enter PID to terminate (or 'q' to quit): 4242
[TARGET] Process information:
  Name   : python.exe
  PID    : 4242
  User   : AdminUser
  Memory : 42.0 MB
  Path   : C:\\Tools\\python.exe
[CONFIRM] Kill this process? (y/N): y
[*] Attempting to terminate PID: 4242
[OK] Process 4242 terminated successfully.
------------------------------------------------------------
```

## Build a standalone EXE (PyInstaller)
From the project root on Windows:
```bash
pyinstaller --onefile --uac-admin --icon=logo.ico --version-file=version_info.txt kill_pid_admin.py
```
- `--uac-admin` prompts for elevation in the generated EXE.
- `version_info.txt` supplies file metadata for the Windows properties dialog.
- The packaged binary is placed in `dist/`.

## Files & Structure
- `kill_pid_admin.py` – main script with elevation logic, PID prompt loop, process inspection, and taskkill execution.
- `requirements.txt` – runtime dependencies (plus PyInstaller for packaging).
- `version_info.txt` – metadata used by PyInstaller when embedding version info.
- `logo.ico` – app icon for the EXE and README.
- `LICENSE` – MIT license.

## Limitations & Notes
- Designed for Windows; exits immediately on other operating systems.
- Requires Administrator privileges to terminate processes reliably (`taskkill /F /T`).
- Invalid or non-existent PIDs are handled interactively (no batch mode).

## Security / Disclaimer
Use cautiously. Terminating critical system processes can destabilize Windows or cause data loss. Only manage systems you are authorized to control. The author assumes no responsibility for misuse.

## License
MIT – see [LICENSE](LICENSE).
