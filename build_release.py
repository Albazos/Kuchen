#!/usr/bin/env python3
"""
Build-Skript fuer KuchenApp Release.

Erstellt aus den Quelldateien:
  1) Eine strukturierte Source-Release-Version (KuchenApp.zip)
  2) Eine standalone Anwendung fuer Linux
  3) Eine standalone Anwendung fuer Windows

Ausfuehren:
  python3 build_release.py            # Alle 3 Versionen
  python3 build_release.py --source   # Nur Source-Bundle
  python3 build_release.py --linux    # Nur Linux Standalone
  python3 build_release.py --windows  # Nur Windows Standalone

Die Version fuer das aktuelle OS wird lokal gebaut (PyInstaller).
Die Version fuer das andere OS wird via GitHub Actions gebaut.

Voraussetzungen fuer Remote-Build:
  - gh CLI installiert und authentifiziert (gh auth login)
  - GitHub Repository konfiguriert
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import time
import zipfile

# --- Konfiguration ---

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEV_DIR = os.path.join(SCRIPT_DIR, "develop")
RELEASE_DIR = os.path.join(SCRIPT_DIR, "release")
BUILD_DIR = os.path.join(RELEASE_DIR, "KuchenApp")
ZIP_PATH = os.path.join(RELEASE_DIR, "KuchenApp.zip")

OS_TAG = platform.system().lower()  # "linux" oder "windows"
STANDALONE_DIR = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{OS_TAG}")
STANDALONE_ZIP_PATH = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{OS_TAG}.zip")

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
      |-- StandardCakeData.csv  <- Kuchendaten (leer, nur Header)
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
    if os.path.exists(RELEASE_DIR):
        shutil.rmtree(RELEASE_DIR)
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
    with open(os.path.join(BUILD_DIR, "Data", "StandardCakeData.csv"), "w", newline="") as f:
        f.write("Name,CakeCount,Hanuta,Waffel,Date\n")
    with open(os.path.join(BUILD_DIR, "Data", "Klassen", "StandardKlasse.csv"), "w", newline="") as f:
        f.write("Name,Mail\n")

    # Data/Settings - Default settings.ini
    with open(os.path.join(BUILD_DIR, "Data", "Settings", "settings.ini"), "w", encoding="utf-8") as f:
        f.write("[Klassen]\nDateiname = StandardKlasse.csv\n\n[CakeData]\nDateiname = StandardCakeData.csv\n\n[IServ]\nDomain = wvss.de\n")

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


def build_standalone():
    """Erstellt eine standalone Anwendung mit PyInstaller."""
    pyinstaller = shutil.which("pyinstaller")
    if pyinstaller is None:
        prefix = os.path.dirname(sys.executable)
        candidate = os.path.join(prefix, "pyinstaller")
        if os.path.isfile(candidate):
            pyinstaller = candidate
    if pyinstaller is None:
        print("[exe]   FEHLER: pyinstaller nicht gefunden!")
        print("        Installiere PyInstaller: pip install pyinstaller")
        return False

    main_script = os.path.join(BUILD_DIR, MAIN_FILE)
    icon_path = os.path.join(BUILD_DIR, "assets", "kuchen_icon.svg")
    data_dir = os.path.join(BUILD_DIR, "Data")

    cmd = [
        pyinstaller,
        "--onefile",
        "--windowed",
        "--name", "KuchenApp",
        "--distpath", STANDALONE_DIR,
        "--workpath", os.path.join(RELEASE_DIR, "_pybuild"),
        "--specpath", os.path.join(RELEASE_DIR, "_pybuild"),
        "--add-data", f"{data_dir}{os.pathsep}Data",
        "--add-data", f"{icon_path}{os.pathsep}assets",
        main_script,
    ]

    print(f"[exe]   PyInstaller wird ausgefuehrt ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[exe]   FEHLER: {result.stderr.strip()}")
        return False

    # Aufraumen: _pybuild Ordner entfernen
    pybuild = os.path.join(RELEASE_DIR, "_pybuild")
    if os.path.exists(pybuild):
        shutil.rmtree(pybuild)

    # Data/ neben die exe kopieren (wird zur Laufzeit beschrieben)
    standalone_data = os.path.join(STANDALONE_DIR, "Data")
    shutil.copytree(data_dir, standalone_data)

    print(f"[exe]   Standalone erstellt: {STANDALONE_DIR}")

    # ZIP fuer Standalone erstellen
    with zipfile.ZipFile(STANDALONE_ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(STANDALONE_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.join(f"KuchenApp_standalone_{OS_TAG}", os.path.relpath(full_path, STANDALONE_DIR))
                zf.write(full_path, arcname)
    size_mb = os.path.getsize(STANDALONE_ZIP_PATH) / (1024 * 1024)
    print(f"[zip]   {STANDALONE_ZIP_PATH}")
    print(f"        Groesse: {size_mb:.1f} MB")
    return True


def _run_gh(args):
    """Fuehrt einen gh CLI Befehl aus und gibt stdout zurueck."""
    result = subprocess.run(
        ["gh"] + args, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def build_remote_standalone():
    """Baut die Standalone-Version fuer das andere OS via GitHub Actions."""
    if shutil.which("gh") is None:
        print("[remote] FEHLER: gh CLI nicht gefunden!")
        print("         Installiere: https://cli.github.com/")
        return False

    remote_os = "windows" if OS_TAG == "linux" else "linux"
    print(f"[remote] Starte GitHub Actions Build fuer {remote_os} ...")

    # Workflow triggern
    try:
        _run_gh(["workflow", "run", "build_release.yml"])
    except RuntimeError as e:
        print(f"[remote] FEHLER beim Triggern: {e}")
        return False

    # Warten bis der Run gestartet ist
    print("[remote] Warte auf Workflow-Start ...")
    time.sleep(5)

    # Neuesten Run finden
    try:
        runs_json = _run_gh([
            "run", "list",
            "--workflow", "build_release.yml",
            "--limit", "1",
            "--json", "databaseId,status"
        ])
        runs = json.loads(runs_json)
        if not runs:
            print("[remote] FEHLER: Kein Workflow-Run gefunden")
            return False
        run_id = str(runs[0]["databaseId"])
    except (RuntimeError, json.JSONDecodeError, KeyError) as e:
        print(f"[remote] FEHLER: {e}")
        return False

    # Auf Abschluss warten
    print(f"[remote] Warte auf Run {run_id} ...")
    try:
        _run_gh(["run", "watch", run_id, "--exit-status"])
    except RuntimeError as e:
        print(f"[remote] FEHLER: Workflow fehlgeschlagen: {e}")
        return False

    # Artifact herunterladen
    artifact_name = f"KuchenApp-standalone-{remote_os}"
    remote_zip_name = f"KuchenApp_standalone_{remote_os}.zip"
    download_dir = os.path.join(RELEASE_DIR, "_remote_download")
    os.makedirs(download_dir, exist_ok=True)

    print(f"[remote] Lade Artifact '{artifact_name}' herunter ...")
    try:
        _run_gh([
            "run", "download", run_id,
            "--name", artifact_name,
            "--dir", download_dir
        ])
    except RuntimeError as e:
        print(f"[remote] FEHLER beim Download: {e}")
        return False

    # ZIP in release/ verschieben
    downloaded_zip = os.path.join(download_dir, remote_zip_name)
    target_zip = os.path.join(RELEASE_DIR, remote_zip_name)
    if os.path.isfile(downloaded_zip):
        shutil.move(downloaded_zip, target_zip)
    else:
        # gh download entpackt manchmal in einen Unterordner
        for root, dirs, files in os.walk(download_dir):
            for f in files:
                if f == remote_zip_name:
                    shutil.move(os.path.join(root, f), target_zip)
                    break

    # Aufraemen
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)

    if os.path.isfile(target_zip):
        # ZIP auch in Ordner entpacken
        remote_dir = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{remote_os}")
        os.makedirs(remote_dir, exist_ok=True)
        with zipfile.ZipFile(target_zip, "r") as zf:
            for member in zf.namelist():
                # Ersten Pfadteil (Archiv-Ordnername) entfernen
                parts = member.split("/", 1)
                if len(parts) > 1 and parts[1]:
                    target_path = os.path.join(remote_dir, parts[1])
                    if member.endswith("/"):
                        os.makedirs(target_path, exist_ok=True)
                    else:
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        with zf.open(member) as src, open(target_path, "wb") as dst:
                            shutil.copyfileobj(src, dst)

        size_mb = os.path.getsize(target_zip) / (1024 * 1024)
        print(f"[remote] {target_zip}")
        print(f"[remote] {remote_dir}")
        print(f"         Groesse: {size_mb:.1f} MB")
        return True
    else:
        print(f"[remote] FEHLER: {remote_zip_name} nicht gefunden")
        return False


def main():
    print("=" * 40)
    print("  KuchenApp Release Build")
    print("=" * 40)
    print()

    clean_build()
    compile_ui()

    # Source-Bundle
    create_dirs()
    copy_files()
    write_readme()
    create_zip()
    print()
    print("--- Source-Release ---")
    print(f"  ZIP:  {ZIP_PATH}")

    local_os = OS_TAG  # "linux" oder "windows"
    remote_os = "windows" if local_os == "linux" else "linux"

    # Lokales OS bauen (Linux oder Windows)
    print()
    if build_standalone():
        print()
        print(f"--- Standalone {local_os.capitalize()} ---")
        print(f"  ZIP:  {STANDALONE_ZIP_PATH}")
    else:
        print("[exe]   Lokaler Standalone-Build fehlgeschlagen.")

    # Remote OS bauen (das jeweils andere)
    print()
    if build_remote_standalone():
        remote_zip = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{remote_os}.zip")
        print()
        print(f"--- Standalone {remote_os.capitalize()} (remote) ---")
        print(f"  ZIP:  {remote_zip}")
    else:
        print(f"[remote] {remote_os.capitalize()}-Build fehlgeschlagen.")

    print()
    print("Fertig!")


if __name__ == "__main__":
    main()
