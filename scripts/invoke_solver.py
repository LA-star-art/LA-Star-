import os
import subprocess
import sys


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: invoke_solver.py <acf-path>")
        return 2

    acf_path = sys.argv[1]
    topdir = os.environ.get("topdir")
    if not topdir:
        print("Missing ADAMS environment variable: topdir")
        return 3

    solver = os.path.join(topdir, "solver", "win64", "solver.exe")
    if not os.path.exists(solver):
        print(f"solver not found: {solver}")
        return 4

    proc = subprocess.run([solver, acf_path], cwd=os.getcwd(), text=True)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
