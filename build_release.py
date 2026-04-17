#!/usr/bin/env python3
"""
Build-Skript fuer KuchenApp Release.

Erstellt aus den Quelldateien eine strukturierte Release-Version
mit src/, ui/, assets/ Ordnern und passt die Imports automatisch an.
Erzeugt am Ende eine KuchenApp.zip.

Ausfuehren:  python3 build_release.py
"""

import os
import shutil
import subprocess
import sys
import zipfile

# --- Konfiguration ---

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEV_DIR = os.path.join(SCRIPT_DIR, "develop")
BUILD_DIR = os.path.join(SCRIPT_DIR, "release", "KuchenApp")
ZIP_PATH = os.path.join(SCRIPT_DIR, "release", "KuchenApp.zip")

# Dateien die nach src/ kopiert werden
SRC_FILES = [
    "DataManager.py",
    "IServAPIEdited_standalone.py",
    "IservMailManager.py",
    "KuchenMailManager.py",
    "LoginDialog.py",
    "SettingsManager.py",
    "AppLogger.py",
]

# UI-Quelldateien (.ui -> _ui.py) - werden vor dem Kopieren kompiliert
UI_SOURCE_FILES = {
    "UIMainWindow.ui":  "UIMainWindow_ui.py",
    "UIMailsDialog.ui": "UIMailsDialog_ui.py",
    "UILoginDialog.ui": "UILoginDialog_ui.py",
}

# UI-Dateien die nach ui/ kopiert werden
UI_FILES = [
    "UIMainWindow_ui.py",
    "UIMailsDialog_ui.py",
    "UILoginDialog_ui.py",
]

# Asset-Dateien die nach assets/ kopiert werden
ASSET_FILES = [
    "kuchen_icon.svg",
]

# Hauptdatei (bleibt im Root)
MAIN_FILE = "KuchenMain.py"

README_CONTENT = """\
========================================
  KuchenApp - Anleitung / README
========================================

Beschreibung:
  KuchenApp ist eine Desktop-Anwendung zur Verwaltung von Kuchen-Listen
  und zum Versenden von Erinnerungs-Mails ueber IServ.


Voraussetzungen:
  - Python 3.10 oder neuer
  - PySide6 (Qt fuer Python)

  Installation von PySide6:
    pip install PySide6


Projektstruktur:
  KuchenApp/
  |-- KuchenMain.py            <- Hauptprogramm (hier starten)
  |-- README.txt               <- Diese Datei
  |-- assets/
  |   +-- kuchen_icon.svg      <- App-Icon
  |-- src/
  |   |-- AppLogger.py         <- Singleton Logger (Signale fuer Fehlermeldungen)
  |   |-- DataManager.py       <- Datenverwaltung (CSV lesen/schreiben)
  |   |-- KuchenMailManager.py <- Dialog fuer Mail-Liste
  |   |-- LoginDialog.py       <- Login-Dialog fuer IServ
  |   |-- IservMailManager.py  <- Mail-Versand ueber IServ API
  |   |-- IServAPIEdited_standalone.py  <- IServ API (nur stdlib, kein pip)
  |   +-- SettingsManager.py   <- Einstellungsverwaltung (INI-Datei)
  |-- ui/
  |   |-- UIMainWindow_ui.py
  |   |-- UIMailsDialog_ui.py
  |   +-- UILoginDialog_ui.py
  +-- Data/
      |-- CakeData.csv         <- Kuchendaten (leer, nur Header)
      |-- Settings/
      |   +-- settings.ini     <- Einstellungen (z.B. Klassen-Dateiname)
      +-- Klassen/
          +-- StandardKlasse.csv  <- Klassenliste (leer, nur Header)


Starten:
  python KuchenMain.py
"""


def compile_ui():
    """Kompiliert .ui Dateien zu _ui.py mit pyside6-uic."""
    # pyside6-uic aus dem gleichen Python-Environment nutzen
    uic = shutil.which("pyside6-uic")
    if uic is None:
        # Fallback: im gleichen Prefix wie das aktuelle Python suchen
        prefix = os.path.dirname(sys.executable)
        candidate = os.path.join(prefix, "pyside6-uic")
        if os.path.isfile(candidate):
            uic = candidate
    if uic is None:
        print("[ui]    FEHLER: pyside6-uic nicht gefunden!")
        print("        Installiere PySide6: pip install PySide6")
        sys.exit(1)

    count = 0
    for ui_file, py_file in UI_SOURCE_FILES.items():
        ui_path = os.path.join(DEV_DIR, "ui", ui_file)
        py_path = os.path.join(DEV_DIR, "ui", py_file)
        if not os.path.isfile(ui_path):
            print(f"[ui]    WARNUNG: {ui_file} nicht gefunden, uebersprungen")
            continue
        result = subprocess.run([uic, ui_path, "-o", py_path],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[ui]    FEHLER bei {ui_file}: {result.stderr.strip()}")
            sys.exit(1)
        count += 1
    print(f"[ui]    {count} UI-Datei(en) kompiliert")


def clean_build():
    """Loescht den alten Build-Ordner und ZIP."""
    if os.path.exists(os.path.join(SCRIPT_DIR, "release")):
        shutil.rmtree(os.path.join(SCRIPT_DIR, "release"))
        print("[clean] Alter release/ Ordner geloescht")


def create_dirs():
    """Erstellt die Release-Ordnerstruktur."""
    for subdir in ["src", "ui", "assets", "Data", "Data/Klassen", "Data/Settings"]:
        os.makedirs(os.path.join(BUILD_DIR, subdir), exist_ok=True)
    print("[dirs]  Ordnerstruktur erstellt")


def copy_files():
    """Kopiert alle Dateien in die Release-Struktur."""
    # Hauptdatei
    shutil.copy2(os.path.join(DEV_DIR, MAIN_FILE), BUILD_DIR)

    # src/
    for f in SRC_FILES:
        shutil.copy2(os.path.join(DEV_DIR, "src", f), os.path.join(BUILD_DIR, "src"))

    # ui/
    for f in UI_FILES:
        shutil.copy2(os.path.join(DEV_DIR, "ui", f), os.path.join(BUILD_DIR, "ui"))

    # assets/
    for f in ASSET_FILES:
        shutil.copy2(os.path.join(DEV_DIR, "assets", f), os.path.join(BUILD_DIR, "assets"))

    # Data/ - leere CSVs mit nur Header-Zeile erstellen
    with open(os.path.join(BUILD_DIR, "Data", "CakeData.csv"), "w", newline="") as f:
        f.write("Name,CakeCount,Hanuta,Waffel,Date\n")
    with open(os.path.join(BUILD_DIR, "Data", "Klassen", "StandardKlasse.csv"), "w", newline="") as f:
        f.write("Name,Mail\n")

    # Data/Settings - Default settings.ini
    with open(os.path.join(BUILD_DIR, "Data", "Settings", "settings.ini"), "w", encoding="utf-8") as f:
        f.write("[Klassen]\nDateiname = StandardKlasse.csv\n\n[CakeData]\nDateiname = CakeData.csv\n\n[IServ]\nDomain = wvss.de\n")

    # __init__.py fuer src/ und ui/
    for pkg in ["src", "ui"]:
        init_path = os.path.join(BUILD_DIR, pkg, "__init__.py")
        with open(init_path, "w") as f:
            pass

    print("[copy]  Dateien kopiert")


def write_readme():
    """Schreibt die README.txt."""
    with open(os.path.join(BUILD_DIR, "README.txt"), "w", encoding="utf-8") as f:
        f.write(README_CONTENT)
    print("[readme] README.txt erstellt")


def create_zip():
    """Erstellt die Release-ZIP-Datei."""
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(BUILD_DIR):
            # __pycache__ ueberspringen
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.join("KuchenApp", os.path.relpath(full_path, BUILD_DIR))
                zf.write(full_path, arcname)

    size_kb = os.path.getsize(ZIP_PATH) / 1024
    print(f"[zip]   {ZIP_PATH}")
    print(f"        Groesse: {size_kb:.0f} KB")


def main():
    print("=" * 40)
    print("  KuchenApp Release Build")
    print("=" * 40)
    print()

    clean_build()
    compile_ui()
    create_dirs()
    copy_files()
    write_readme()
    create_zip()

    print()
    print("Fertig! Release liegt in:")
    print(f"  Ordner: {BUILD_DIR}")
    print(f"  ZIP:    {ZIP_PATH}")


if __name__ == "__main__":
    main()
