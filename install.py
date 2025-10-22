import subprocess
import sys
import os

dependencies = [
    ["docker", "--version"],
    ["docker", "compose", "version"],
]

def sys_type():
    return "windows" if sys.platform.startswith("win") else "linux"

def check_dependency(cmd_list):
    try:
        subprocess.run(cmd_list, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

for dep in dependencies:
    if not check_dependency(dep):
        dep_name = " ".join(dep[:-1]) if len(dep) > 1 else dep[0]
        print(f"Missing dependency: {dep_name}")
        if sys_type() == "linux":
            print(f"Run: sudo apt install {dep_name}")
        else:
            print(f"Please install {dep_name} manually for Windows.")
    else:
        print(f"{dep[0]} installed")