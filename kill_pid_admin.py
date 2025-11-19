import os
import sys
import ctypes
import subprocess


def is_windows() -> bool:
    """Check if the OS is Windows."""
    return os.name == "nt"


def is_admin() -> bool:
    """Check if the program is running with Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def relaunch_as_admin():
    """
    Relaunch the program with Administrator privileges.
    Works for both Python and compiled EXE (PyInstaller).
    """
    exe = sys.executable
    params = " ".join(f'"{arg}"' for arg in sys.argv)

    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", exe, params, None, 1
        )
    except Exception as e:
        print(f"Error: Failed to relaunch as Administrator: {e}")
    sys.exit(0)


def kill_pid(pid: int) -> None:
    """Try to kill the target process using taskkill."""
    try:
        result = subprocess.run(
            ["taskkill", "/PID", str(pid), "/F", "/T"],
            capture_output=True,
            text=True,
            shell=False,
        )

        if result.returncode == 0:
            print(f"Process {pid} terminated successfully.")
        else:
            print(f"Failed to terminate process {pid}.")
            if result.stderr:
                print("Taskkill error details:")
                print(result.stderr.strip())

    except Exception as e:
        print(f"Unexpected error while terminating PID {pid}: {e}")


def main():
    if not is_windows():
        print("This tool is only supported on Windows.")
        sys.exit(1)

    if not is_admin():
        print("Program is not running as Administrator. Attempting to relaunch...")
        relaunch_as_admin()

    print("====== KILL PID TOOL (Windows) ======")
    print("Type 'q' or 'quit' or 'exit' to close the program.\n")

    while True:
        user_input = input("Enter PID to terminate: ").strip()

        if user_input.lower() in {"q", "quit", "exit"}:
            print("Exiting program.")
            break

        if not user_input.isdigit():
            print("Invalid input. Please enter a valid number.\n")
            continue

        pid = int(user_input)

        if pid <= 0:
            print("PID must be a positive number.\n")
            continue

        kill_pid(pid)
        print("-" * 50)


if __name__ == "__main__":
    main()
