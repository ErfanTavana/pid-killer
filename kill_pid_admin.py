import os
import sys
import ctypes
import subprocess

from colorama import init, Fore, Style


# Initialize colorama (for Windows CMD)
init(autoreset=True)


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

    print(Fore.YELLOW + "[*] Elevating privileges to Administrator...")
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", exe, params, None, 1
        )
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to relaunch as Administrator: {e}")
    sys.exit(0)


def kill_pid(pid: int) -> None:
    """Try to kill the target process using taskkill."""
    print(Fore.CYAN + f"[*] Attempting to terminate PID: {pid}")
    try:
        result = subprocess.run(
            ["taskkill", "/PID", str(pid), "/F", "/T"],
            capture_output=True,
            text=True,
            shell=False,
        )

        if result.returncode == 0:
            print(Fore.GREEN + f"[OK] Process {pid} terminated successfully.")
        else:
            print(Fore.RED + f"[ERROR] Failed to terminate process {pid}.")
            if result.stderr:
                print(Fore.YELLOW + "[DETAIL] Taskkill error output:")
                print(Fore.RED + result.stderr.strip())

    except Exception as e:
        print(Fore.RED + f"[FATAL] Unexpected error while terminating PID {pid}: {e}")


def print_banner():
    """Display hacker-style ASCII banner."""
    os.system("cls")  # Clear screen on Windows for a clean look (optional)
    banner = r"""
  _  __ _ _ _      ____ ___ ____   ____ ___ 
 | |/ /(_) | | ___|  _ \_ _|  _ \ / ___|_ _|
 | ' / | | | |/ _ \ |_) | || | | | |    | | 
 | . \ | | | |  __/  __/| || |_| | |___ | | 
 |_|\_\|_|_|_|\___|_|  |___|____/ \____|___|
        KILL PID TOOL  |  Windows Admin
    """
    print(Fore.GREEN + banner)
    print(Fore.GREEN + "-" * 60)
    print(Fore.GREEN + "[INFO] Windows PID termination utility with Admin elevation")
    print(Fore.GREEN + "[INFO] Type 'q' or 'quit' or 'exit' to leave the program")
    print(Fore.GREEN + "-" * 60 + "\n")


def main():
    if not is_windows():
        print(Fore.RED + "[ERROR] This tool is only supported on Windows.")
        sys.exit(1)

    if not is_admin():
        print(Fore.YELLOW + "[WARN] Not running as Administrator.")
        relaunch_as_admin()

    print_banner()

    while True:
        user_input = input(
            Fore.CYAN + "[PID] Enter PID to terminate (or 'q' to quit): " + Style.RESET_ALL
        ).strip()

        if user_input.lower() in {"q", "quit", "exit"}:
            print(Fore.YELLOW + "[*] Exiting program. Goodbye.")
            break

        if not user_input.isdigit():
            print(Fore.RED + "[ERROR] Invalid input. Please enter a valid numeric PID.\n")
            continue

        pid = int(user_input)

        if pid <= 0:
            print(Fore.RED + "[ERROR] PID must be a positive number.\n")
            continue

        kill_pid(pid)
        print(Fore.GREEN + "-" * 60 + "\n")


if __name__ == "__main__":
    main()
