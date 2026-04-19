#!/usr/bin/env python3
"""
Build-Skript fuer KuchenApp Release.

Ausfuehren:
  python3 build_release.py          # Vollstaendiges Release:
                                    # Patch hochzaehlen, Source bauen,
                                    # Tag+Push, CI abwarten, download

  Major/Minor manuell in version.ini aendern.
  Patch wird bei jedem Build automatisch hochgezaehlt.

Nur fuer CI (nicht manuell aufrufen):
  python3 build_release.py --source     # Nur Source bauen
  python3 build_release.py --standalone  # Standalone fuer aktuelles OS
"""

import configparser
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

VERSION_INI = os.path.join(SCRIPT_DIR, "version.ini")


def read_version():
    """Liest die aktuelle Version aus version.ini."""
    cfg = configparser.ConfigParser()
    cfg.read(VERSION_INI, encoding="utf-8")
    major = cfg.getint("Version", "major", fallback=0)
    minor = cfg.getint("Version", "minor", fallback=0)
    patch = cfg.getint("Version", "patch", fallback=0)
    return major, minor, patch


def bump_patch():
    """Erhoeht den Patch-Zaehler und schreibt zurueck. Gibt den Tag-String zurueck."""
    major, minor, patch = read_version()
    patch += 1

    cfg = configparser.ConfigParser()
    cfg["Version"] = {
        "major": str(major),
        "minor": str(minor),
        "patch": str(patch),
    }
    with open(VERSION_INI, "w", encoding="utf-8") as f:
        cfg.write(f)

    tag = f"v{major}.{minor}.{patch}"
    print(f"[ver]   Version: {tag}")
    return tag

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
    """Erstellt eine standalone Anwendung mit PyInstaller (nur fuer CI)."""
    standalone_dir = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{OS_TAG}")
    standalone_zip = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{OS_TAG}.zip")

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
        "--distpath", standalone_dir,
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
    standalone_data = os.path.join(standalone_dir, "Data")
    shutil.copytree(data_dir, standalone_data)

    # assets/ neben die exe kopieren (Icons etc.)
    assets_src = os.path.join(BUILD_DIR, "assets")
    assets_dst = os.path.join(standalone_dir, "assets")
    if os.path.isdir(assets_src):
        shutil.copytree(assets_src, assets_dst)

    print(f"[exe]   Standalone erstellt: {standalone_dir}")

    # ZIP fuer Standalone erstellen
    with zipfile.ZipFile(standalone_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(standalone_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.join(f"KuchenApp_standalone_{OS_TAG}", os.path.relpath(full_path, standalone_dir))
                zf.write(full_path, arcname)
    size_mb = os.path.getsize(standalone_zip) / (1024 * 1024)
    print(f"[zip]   {standalone_zip}")
    print(f"        Groesse: {size_mb:.1f} MB")
    return True


def _find_gh():
    """Sucht die gh CLI."""
    gh = shutil.which("gh")
    if gh is None:
        candidate = os.path.join("C:\\", "Program Files", "GitHub CLI", "gh.exe")
        if os.path.isfile(candidate):
            gh = candidate
    if gh is None:
        print("[gh]    FEHLER: gh CLI nicht gefunden!")
        print("        Installiere: https://cli.github.com/")
    return gh


def create_release(version):
    """Erstellt Release lokal mit gh, wartet auf CI, laedt Standalone herunter."""
    gh = _find_gh()
    if gh is None:
        return False

    # Pruefen ob Tag schon existiert
    result = subprocess.run(
        ["git", "tag", "-l", version],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if version in result.stdout.strip().splitlines():
        print(f"[tag]   FEHLER: Tag {version} existiert bereits!")
        return False

    # Uncommitted changes committen (inkl. version.ini)
    subprocess.run(["git", "add", "-A"], cwd=SCRIPT_DIR)
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if status.stdout.strip():
        print("[git]   Committe Aenderungen ...")
        subprocess.run(
            ["git", "commit", "-m", f"Release {version}"],
            cwd=SCRIPT_DIR, check=True
        )

    # Pushen
    print("[git]   Pushe commits ...")
    subprocess.run(["git", "push"], cwd=SCRIPT_DIR, check=True)

    # GitHub Release erstellen (laedt Source-ZIP sofort hoch)
    print(f"[gh]    Erstelle GitHub Release {version} ...")
    create_result = subprocess.run(
        [gh, "release", "create", version, ZIP_PATH,
         "--title", f"KuchenApp {version}",
         "--notes", f"Automatisches Release {version}"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if create_result.returncode != 0:
        print(f"[gh]    FEHLER: {create_result.stderr.strip()}")
        return False
    print(f"[gh]    Release {version} erstellt (Source-ZIP hochgeladen)")

    # Auf CI warten (baut Standalone fuer Linux + Windows)
    print("[ci]    Warte auf GitHub Actions Workflow ...")
    print("        (Das kann einige Minuten dauern)")
    time.sleep(10)

    watch_result = subprocess.run(
        [gh, "run", "watch", "--exit-status"],
        capture_output=False, text=True, cwd=SCRIPT_DIR
    )
    if watch_result.returncode != 0:
        print("[ci]    FEHLER: Workflow fehlgeschlagen!")
        print("        Pruefe: gh run list")
        return False

    print("[ci]    Workflow erfolgreich abgeschlossen!")
    print()

    # Standalone-ZIPs vom Release herunterladen
    return download_release(version)


def download_release(version=None):
    """Laedt die Standalone-ZIPs vom GitHub Release herunter."""
    gh = _find_gh()
    if gh is None:
        return False

    os.makedirs(RELEASE_DIR, exist_ok=True)

    # Version bestimmen
    if version is None:
        try:
            result = subprocess.run(
                [gh, "release", "view", "--json", "tagName"],
                capture_output=True, text=True, cwd=SCRIPT_DIR
            )
            if result.returncode != 0:
                print(f"[dl]    FEHLER: {result.stderr.strip()}")
                return False
            version = json.loads(result.stdout).get("tagName", "")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[dl]    FEHLER: {e}")
            return False

    print(f"[dl]    Lade von Release {version} herunter ...")
    dl_result = subprocess.run(
        [gh, "release", "download", version,
         "--pattern", "KuchenApp_standalone_*.zip",
         "--dir", RELEASE_DIR, "--clobber"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if dl_result.returncode != 0:
        print(f"[dl]    FEHLER: {dl_result.stderr.strip()}")
        return False

    # Heruntergeladene Dateien auflisten
    for f in os.listdir(RELEASE_DIR):
        if f.startswith("KuchenApp_standalone_") and f.endswith(".zip"):
            path = os.path.join(RELEASE_DIR, f)
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print(f"[dl]    {f} ({size_mb:.1f} MB)")

    print(f"[dl]    Download abgeschlossen -> {RELEASE_DIR}")
    return True


def _build_source():
    """Baut das Source-Bundle (ZIP)."""
    clean_build()
    compile_ui()
    create_dirs()
    copy_files()
    write_readme()
    create_zip()
    print()
    print("--- Source-Release ---")
    print(f"  ZIP:  {ZIP_PATH}")


def main():
    ci_standalone = "--standalone" in sys.argv
    ci_source = "--source" in sys.argv

    # Aktuelle Version anzeigen
    major, minor, patch = read_version()
    current_ver = f"v{major}.{minor}.{patch}"

    print("=" * 40)
    print("  KuchenApp Release Build")
    if ci_standalone:
        print(f"  Modus: Standalone ({OS_TAG})")
    elif ci_source:
        print("  Modus: Source-Bundle (CI)")
    else:
        print(f"  Modus: Release")
        print(f"  Aktuelle Version: {current_ver}")
    print("=" * 40)
    print()

    if ci_standalone:
        clean_build()
        compile_ui()
        create_dirs()
        copy_files()
        if build_standalone():
            print()
            print(f"--- Standalone {OS_TAG.capitalize()} ---")
            standalone_zip = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{OS_TAG}.zip")
            print(f"  ZIP:  {standalone_zip}")
        else:
            print("[exe]   Standalone-Build fehlgeschlagen.")
            sys.exit(1)

    elif ci_source:
        _build_source()

    else:
        # Normaler Aufruf: Patch hochzaehlen, Source bauen, Release erstellen
        release_version = bump_patch()
        _build_source()
        print()
        create_release(release_version)

    print()
    print("Fertig!")


if __name__ == "__main__":
    main()
