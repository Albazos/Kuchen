#!/usr/bin/env python3
"""
Converts all .ui files in develop/ui/ to _ui.py files using pyside6-uic.

Usage:
  python build_ui.py
"""

import os
import shutil
import subprocess
import sys
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(SCRIPT_DIR, "develop", "ui")


def _find_uic():
    """Locate pyside6-uic executable."""
    uic = shutil.which("pyside6-uic")
    if uic:
        return [uic]
    # Fallback: look next to the Python executable (Scripts folder)
    scripts_dir = os.path.join(os.path.dirname(sys.executable), "Scripts")
    candidate = os.path.join(scripts_dir, "pyside6-uic.exe" if sys.platform == "win32" else "pyside6-uic")
    if os.path.isfile(candidate):
        return [candidate]
    print("ERROR: pyside6-uic not found. Install PySide6: pip install PySide6")
    sys.exit(1)


def main():
    ui_files = glob.glob(os.path.join(UI_DIR, "*.ui"))

    if not ui_files:
        print("No .ui files found in", UI_DIR)
        sys.exit(1)

    uic_cmd = _find_uic()
    errors = 0

    for ui_file in ui_files:
        base = os.path.splitext(os.path.basename(ui_file))[0]
        out_file = os.path.join(UI_DIR, f"{base}_ui.py")

        print(f"Converting {base}.ui -> {base}_ui.py")
        result = subprocess.run(
            uic_cmd + ["-g", "python", "-o", out_file, ui_file],
            capture_output=True, text=True,
        )

        if result.returncode != 0:
            print(f"  ERROR: {result.stderr.strip()}")
            errors += 1
        else:
            print(f"  OK")

    if errors:
        print(f"\n{errors} file(s) failed.")
        sys.exit(1)

    print(f"\nConverted {len(ui_files)} file(s).")


if __name__ == "__main__":
    main()
