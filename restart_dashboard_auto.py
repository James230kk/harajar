"""
Stop any process using port 5000, then start the dashboard from this folder.
Run from project root: python restart_dashboard_auto.py
"""
import sys
import time
import subprocess
from pathlib import Path

PORT = 5000
PROJECT_ROOT = Path(__file__).resolve().parent

def kill_processes_on_port(port):
    """Kill any process listening on the given port. Works on Windows and Unix."""
    killed = []
    try:
        if sys.platform == "win32":
            # Find PIDs using port 5000 (e.g. TCP 0.0.0.0:5000 LISTENING)
            out = subprocess.run(
                ["netstat", "-ano"],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
            )
            if out.returncode != 0:
                return killed
            for line in out.stdout.splitlines():
                parts = line.split()
                if f":{port}" in line and "LISTENING" in line and len(parts) >= 5:
                    try:
                        pid = int(parts[-1])
                        if pid > 0:
                            subprocess.run(
                                ["taskkill", "/F", "/PID", str(pid)],
                                capture_output=True,
                                timeout=5,
                                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0,
                            )
                            killed.append(pid)
                    except (ValueError, IndexError):
                        pass
        else:
            # Linux/macOS: use lsof to find PIDs on port
            out = subprocess.run(
                ["lsof", "-ti", f":{port}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if out.returncode == 0 and out.stdout.strip():
                for pid_str in out.stdout.strip().split():
                    try:
                        pid = int(pid_str)
                        subprocess.run(["kill", "-9", str(pid)], capture_output=True, timeout=5)
                        killed.append(pid)
                    except ValueError:
                        pass
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception) as e:
        print(f"Note: could not free port {port} ({e})")
    return killed

def main():
    if not (PROJECT_ROOT / "dashboard.py").exists():
        print("Run this from the project root (where dashboard.py is).")
        sys.exit(1)

    print("Stopping any process on port", PORT, "...")
    killed = kill_processes_on_port(PORT)
    if killed:
        print("Stopped PID(s):", killed)
        time.sleep(2)
    else:
        print("No process was using port", PORT)

    print("Starting dashboard from:", PROJECT_ROOT)
    print("=" * 60)
    # Start dashboard in this process so it keeps running and shows output
    sys.exit(
        subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "start_dashboard.py")],
            cwd=str(PROJECT_ROOT),
        ).returncode
    )

if __name__ == "__main__":
    main()
