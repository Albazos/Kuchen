#!/usr/bin/env python3
"""Open a .ui file in Qt Designer. Lists all .ui files for selection."""

import glob
import os
import shutil
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(SCRIPT_DIR, "develop", "ui")


def find_designer():
    lDesigner = shutil.which("pyside6-designer")
    if lDesigner:
        return lDesigner

    lPythonDir = os.path.dirname(sys.executable)
    lExecutableName = "pyside6-designer.exe" if sys.platform == "win32" else "pyside6-designer"
    lCandidateDirs = [
        lPythonDir,
        os.path.join(lPythonDir, "Scripts"),
        os.path.join(lPythonDir, "bin"),
    ]
    for lCandidateDir in lCandidateDirs:
        lCandidatePath = os.path.join(lCandidateDir, lExecutableName)
        if os.path.isfile(lCandidatePath):
            return lCandidatePath

    print("ERROR: pyside6-designer not found. Install PySide6: pip install PySide6")
    sys.exit(1)


def main():
    ui_files = sorted(glob.glob(os.path.join(UI_DIR, "*.ui")))

    if not ui_files:
        print("No .ui files found in", UI_DIR)
        sys.exit(1)

    print("Available .ui files:\n")
    for i, f in enumerate(ui_files, 1):
        print(f"  {i}. {os.path.basename(f)}")

    print()
    choice = input("Select file number (or press Enter for all): ").strip()

    designer = find_designer()

    if choice == "":
        files = ui_files
    else:
        try:
            idx = int(choice) - 1
            files = [ui_files[idx]]
        except (ValueError, IndexError):
            print("Invalid selection.")
            sys.exit(1)

    print(f"Opening in Designer: {', '.join(os.path.basename(f) for f in files)}")
    subprocess.Popen([designer] + files)


if __name__ == "__main__":
    main()
