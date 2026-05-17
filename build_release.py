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
import argparse

# --- Konfiguration ---

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEV_DIR = os.path.join(SCRIPT_DIR, "develop")
DOCS_DIR = os.path.join(SCRIPT_DIR, "docs")
RELEASE_DIR = os.path.join(SCRIPT_DIR, "release")
BUILD_DIR = os.path.join(RELEASE_DIR, "KuchenApp")
ZIP_PATH = os.path.join(RELEASE_DIR, "KuchenApp.zip")

# Doku-PDFs werden aus den LaTeX-Quellen neu gebaut und ins Release kopiert.
DOC_SOURCE_FILES = [
    "dokumentation.tex",
    "benutzerdokumentation.tex",
]

DOC_FILES = [
    "dokumentation.pdf",
    "benutzerdokumentation.pdf",
]

OS_TAG = platform.system().lower()  # "linux" oder "windows"

VERSION_INI = os.path.join(SCRIPT_DIR, "version.ini")


def _find_executable(aBaseName):
    """Sucht ein CLI-Tool plattformneutral im PATH und neben dem Python-Interpreter."""
    lCandidateNames = [aBaseName]
    if sys.platform == "win32" and not aBaseName.lower().endswith(".exe"):
        lCandidateNames.insert(0, f"{aBaseName}.exe")

    for lCandidateName in lCandidateNames:
        lFoundPath = shutil.which(lCandidateName)
        if lFoundPath:
            return lFoundPath

    lPythonDir = os.path.dirname(sys.executable)
    lSearchDirs = [
        lPythonDir,
        os.path.join(lPythonDir, "Scripts"),
        os.path.join(lPythonDir, "bin"),
    ]
    for lSearchDir in lSearchDirs:
        for lCandidateName in lCandidateNames:
            lCandidatePath = os.path.join(lSearchDir, lCandidateName)
            if os.path.isfile(lCandidatePath):
                return lCandidatePath
    return None


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
    "IServAPI.py",
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
    "chevron_down.svg",
    "theme_dark_blue.qss",
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
  |   |-- kuchen_icon.svg      <- App-Icon
  |   |-- chevron_down.svg     <- Pfeil-Icon fuer ComboBoxen
  |   +-- theme_dark_blue.qss  <- Zentrales Dark-Blue-Theme
  |-- src/
  |   |-- AppLogger.py         <- Singleton Logger (Signale fuer Fehlermeldungen)
  |   |-- DataManager.py       <- Datenverwaltung (CSV lesen/schreiben)
  |   |-- KuchenMailManager.py <- Dialog fuer Mail-Liste
  |   |-- LoginDialog.py       <- Login-Dialog fuer IServ
  |   |-- IservMailManager.py  <- Mail-Versand ueber IServ API
  |   |-- IServAPI.py          <- IServ API (nur stdlib, kein pip)
  |   +-- SettingsManager.py   <- Einstellungsverwaltung (INI-Datei)
  |-- ui/
  |   |-- UIMainWindow_ui.py
  |   |-- UIMailsDialog_ui.py
  |   +-- UILoginDialog_ui.py
  |-- docs/
  |   |-- dokumentation.pdf         <- Projektdokumentation
  |   +-- benutzerdokumentation.pdf <- Benutzerdokumentation
  +-- Data/
      |-- StandardCakeData.csv  <- Kuchendaten (Template)
      |-- Settings/
      |   +-- settings.ini     <- Neutrale Standardeinstellungen
      +-- Klassen/
          +-- StandardKlasse.csv  <- Klassenliste (Template)


Starten:
  python KuchenMain.py

Hinweis zu Daten:
  Eigene Klassen- und Kuchendaten koennen ueber CSV-Dateien gepflegt
  oder importiert werden. Die mitgelieferten Dateien sind nur neutrale
  Standardvorlagen.
"""


def compile_ui():
    """Kompiliert .ui Dateien zu _ui.py mit pyside6-uic."""
    lUic = _find_executable("pyside6-uic")
    if lUic is None:
        print("[ui]    FEHLER: pyside6-uic nicht gefunden!")
        print("        Installiere PySide6: pip install PySide6")
        sys.exit(1)

    lCount = 0
    for lUiFile, lPyFile in UI_SOURCE_FILES.items():
        lUiPath = os.path.join(DEV_DIR, "ui", lUiFile)
        lPyPath = os.path.join(DEV_DIR, "ui", lPyFile)
        if not os.path.isfile(lUiPath):
            print(f"[ui]    WARNUNG: {lUiFile} nicht gefunden, uebersprungen")
            continue
        lResult = subprocess.run([lUic, lUiPath, "-o", lPyPath],
                                 capture_output=True, text=True)
        if lResult.returncode != 0:
            print(f"[ui]    FEHLER bei {lUiFile}: {lResult.stderr.strip()}")
            sys.exit(1)
        lCount += 1
    print(f"[ui]    {lCount} UI-Datei(en) kompiliert")


def compile_docs():
    """Kompiliert LaTeX-Dokumentation nach PDF, wenn pdflatex vorhanden ist."""
    lPdfLatex = _find_executable("pdflatex")
    if lPdfLatex is None:
        print("[docs]  WARNUNG: pdflatex nicht gefunden, Doku-PDFs werden nicht neu gebaut.")
        return False

    lBuiltCount = 0
    for lTexFile in DOC_SOURCE_FILES:
        lTexPath = os.path.join(DOCS_DIR, lTexFile)
        if not os.path.isfile(lTexPath):
            print(f"[docs]  WARNUNG: {lTexFile} nicht gefunden, uebersprungen")
            continue

        for _ in range(2):
            lResult = subprocess.run(
                [lPdfLatex, "-interaction=nonstopmode", "-halt-on-error", lTexFile],
                cwd=DOCS_DIR, capture_output=True, text=True
            )
            if lResult.returncode != 0:
                print(f"[docs]  WARNUNG: {lTexFile} konnte nicht kompiliert werden.")
                print(f"        {lResult.stderr.strip() or lResult.stdout.strip()}")
                break
        else:
            lBuiltCount += 1

    if lBuiltCount:
        print(f"[docs]  {lBuiltCount} Doku-PDF(s) neu gebaut")
    return lBuiltCount == len(DOC_SOURCE_FILES)


def clean_build():
    """Loescht den alten Build-Ordner und ZIP."""
    if os.path.exists(RELEASE_DIR):
        shutil.rmtree(RELEASE_DIR)
        print("[clean] Alter release/ Ordner geloescht")


def create_dirs():
    """Erstellt die Release-Ordnerstruktur."""
    for subdir in ["src", "ui", "assets", "docs", "Data", "Data/Klassen", "Data/Settings"]:
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

    # docs/ - Doku-PDFs (falls vorhanden)
    docs_dst = os.path.join(BUILD_DIR, "docs")
    copied_docs = 0
    for f in DOC_FILES:
        src = os.path.join(DOCS_DIR, f)
        if os.path.isfile(src):
            shutil.copy2(src, docs_dst)
            copied_docs += 1
        else:
            print(f"[docs]  WARNUNG: {f} nicht gefunden, uebersprungen")
    if copied_docs:
        print(f"[docs]  {copied_docs} Doku-PDF(s) kopiert")

    # Data/ - leere CSVs mit nur Header-Zeile erstellen
    with open(os.path.join(BUILD_DIR, "Data", "StandardCakeData.csv"), "w", newline="") as f:
        f.write("Name,CakeCount,Hanuta,Waffel,Date\n")
    with open(os.path.join(BUILD_DIR, "Data", "Klassen", "StandardKlasse.csv"), "w", newline="") as f:
        f.write("Name,Mail\n")

    # Data/Settings - Default settings.ini
    with open(os.path.join(BUILD_DIR, "Data", "Settings", "settings.ini"), "w", encoding="utf-8") as f:
        f.write("[Klassen]\nDateiname = StandardKlasse.csv\n\n[CakeData]\nDateiname = StandardCakeData.csv\n\n[IServ]\nDomain = example.org\n")

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
    lStandaloneDir = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{OS_TAG}")
    lStandaloneZip = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{OS_TAG}.zip")

    lPyInstaller = _find_executable("pyinstaller")
    if lPyInstaller is None:
        print("[exe]   FEHLER: pyinstaller nicht gefunden!")
        print("        Installiere PyInstaller: pip install pyinstaller")
        return False

    lMainScript = os.path.join(BUILD_DIR, MAIN_FILE)
    lIconPath = os.path.join(BUILD_DIR, "assets", "kuchen_icon.svg")
    lDataDir = os.path.join(BUILD_DIR, "Data")

    lCommand = [
        lPyInstaller,
        "--onefile",
        "--windowed",
        "--name", "KuchenApp",
        "--distpath", lStandaloneDir,
        "--workpath", os.path.join(RELEASE_DIR, "_pybuild"),
        "--specpath", os.path.join(RELEASE_DIR, "_pybuild"),
        "--add-data", f"{lDataDir}{os.pathsep}Data",
        "--add-data", f"{lIconPath}{os.pathsep}assets",
        lMainScript,
    ]

    print(f"[exe]   PyInstaller wird ausgefuehrt ...")
    lResult = subprocess.run(lCommand, capture_output=True, text=True)
    if lResult.returncode != 0:
        print(f"[exe]   FEHLER: {lResult.stderr.strip()}")
        return False

    # Aufraumen: _pybuild Ordner entfernen
    lPyBuildDir = os.path.join(RELEASE_DIR, "_pybuild")
    if os.path.exists(lPyBuildDir):
        shutil.rmtree(lPyBuildDir)

    # Data/ neben die exe kopieren (wird zur Laufzeit beschrieben)
    lStandaloneDataDir = os.path.join(lStandaloneDir, "Data")
    shutil.copytree(lDataDir, lStandaloneDataDir)

    # assets/ neben die exe kopieren (Icons etc.)
    lAssetsSourceDir = os.path.join(BUILD_DIR, "assets")
    lAssetsTargetDir = os.path.join(lStandaloneDir, "assets")
    if os.path.isdir(lAssetsSourceDir):
        shutil.copytree(lAssetsSourceDir, lAssetsTargetDir)

    # docs/ neben die exe kopieren (Doku-PDFs)
    lDocsSourceDir = os.path.join(BUILD_DIR, "docs")
    lDocsTargetDir = os.path.join(lStandaloneDir, "docs")
    if os.path.isdir(lDocsSourceDir):
        shutil.copytree(lDocsSourceDir, lDocsTargetDir)

    print(f"[exe]   Standalone erstellt: {lStandaloneDir}")

    # ZIP fuer Standalone erstellen
    with zipfile.ZipFile(lStandaloneZip, "w", zipfile.ZIP_DEFLATED) as lZipFile:
        for lRoot, _, lFiles in os.walk(lStandaloneDir):
            for lFile in lFiles:
                lFullPath = os.path.join(lRoot, lFile)
                lArchiveName = os.path.join(f"KuchenApp_standalone_{OS_TAG}", os.path.relpath(lFullPath, lStandaloneDir))
                lZipFile.write(lFullPath, lArchiveName)
    lSizeMb = os.path.getsize(lStandaloneZip) / (1024 * 1024)
    print(f"[zip]   {lStandaloneZip}")
    print(f"        Groesse: {lSizeMb:.1f} MB")
    return True


def _find_gh():
    """Sucht die gh CLI."""
    lGh = _find_executable("gh")
    if lGh is None:
        print("[gh]    FEHLER: gh CLI nicht gefunden!")
        print("        Installiere: https://cli.github.com/")
    return lGh


def _ensure_clean_worktree():
    """Bricht ab, wenn uncommittete Aenderungen im Worktree liegen."""
    lStatusResult = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if lStatusResult.returncode != 0:
        print("[git]   FEHLER: Git-Status konnte nicht gelesen werden.")
        return False
    if lStatusResult.stdout.strip():
        print("[git]   FEHLER: Der Worktree enthaelt uncommittete Aenderungen.")
        print("        Bitte committe oder stash die Aenderungen vor dem Release.")
        return False
    return True


def _commit_release_version(aVersion):
    """Committed nur die erwartete Versionsaenderung in version.ini."""
    lIgnoredGeneratedPaths = {
        "docs/benutzerdokumentation.pdf",
        "docs/dokumentation.pdf",
    }
    lIgnoredGeneratedPrefixes = (
        "release/",
    )

    lFullStatusResult = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if lFullStatusResult.returncode != 0:
        print("[git]   FEHLER: Git-Status konnte nicht gelesen werden.")
        return False

    lUnexpectedChanges = []
    for lStatusLine in lFullStatusResult.stdout.splitlines():
        lChangedPath = lStatusLine[3:]
        if lChangedPath == "version.ini":
            continue
        if lChangedPath in lIgnoredGeneratedPaths:
            continue
        if any(lChangedPath.startswith(lPrefix) for lPrefix in lIgnoredGeneratedPrefixes):
            continue
        if " -> " in lChangedPath:
            lChangedPath = lChangedPath.split(" -> ", 1)[1]
            if lChangedPath in lIgnoredGeneratedPaths:
                continue
            if any(lChangedPath.startswith(lPrefix) for lPrefix in lIgnoredGeneratedPrefixes):
                continue
        lUnexpectedChanges.append(lStatusLine)

    if lUnexpectedChanges:
        print("[git]   FEHLER: Nach dem Build gibt es unerwartete Aenderungen:")
        for lStatusLine in lUnexpectedChanges:
            print(f"        {lStatusLine}")
        print("        Bitte diese Aenderungen vor dem Release separat pruefen und committen.")
        return False

    lStatusResult = subprocess.run(
        ["git", "status", "--porcelain", "--", "version.ini"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if lStatusResult.returncode != 0:
        print("[git]   FEHLER: Git-Status fuer version.ini konnte nicht gelesen werden.")
        return False

    if not lStatusResult.stdout.strip():
        print("[git]   WARNUNG: version.ini wurde nicht geaendert, kein Release-Commit erstellt.")
        return True

    subprocess.run(["git", "add", "version.ini"], cwd=SCRIPT_DIR, check=True)
    print("[git]   Committe version.ini fuer das Release ...")
    subprocess.run(
        ["git", "commit", "-m", f"Release {aVersion}"],
        cwd=SCRIPT_DIR, check=True
    )
    return True


def create_release(version):
    """Erstellt einen Tag, wartet auf CI, laedt Source-ZIP hoch und Standalone-ZIPs herunter."""
    lGh = _find_gh()
    if lGh is None:
        return False
    if not _commit_release_version(version):
        return False

    # Pruefen ob Tag schon existiert
    lTagResult = subprocess.run(
        ["git", "tag", "-l", version],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if version in lTagResult.stdout.strip().splitlines():
        print(f"[tag]   FEHLER: Tag {version} existiert bereits!")
        return False

    print(f"[tag]   Erstelle lokalen Tag {version} ...")
    subprocess.run(["git", "tag", version], cwd=SCRIPT_DIR, check=True)

    # Branch und Tag pushen
    print("[git]   Pushe commits ...")
    subprocess.run(["git", "push"], cwd=SCRIPT_DIR, check=True)
    print(f"[git]   Pushe Tag {version} ...")
    subprocess.run(["git", "push", "origin", version], cwd=SCRIPT_DIR, check=True)

    # Auf CI warten (baut Standalone fuer Linux + Windows)
    print("[ci]    Warte auf GitHub Actions Workflow ...")
    print("        (Das kann einige Minuten dauern)")
    time.sleep(10)

    lWatchResult = subprocess.run(
        [lGh, "run", "watch", "--exit-status"],
        capture_output=False, text=True, cwd=SCRIPT_DIR
    )
    if lWatchResult.returncode != 0:
        print("[ci]    FEHLER: Workflow fehlgeschlagen!")
        print("        Pruefe: gh run list")
        return False

    print("[ci]    Workflow erfolgreich abgeschlossen!")
    print()

    print(f"[gh]    Lade Source-ZIP zu Release {version} hoch ...")
    lUploadResult = subprocess.run(
        [lGh, "release", "upload", version, ZIP_PATH, "--clobber"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if lUploadResult.returncode != 0:
        print(f"[gh]    FEHLER: {lUploadResult.stderr.strip()}")
        return False

    # Standalone-ZIPs vom Release herunterladen
    return download_release(version)


def download_release(version=None):
    """Laedt die Standalone-ZIPs vom GitHub Release herunter."""
    lGh = _find_gh()
    if lGh is None:
        return False

    os.makedirs(RELEASE_DIR, exist_ok=True)

    # Version bestimmen
    if version is None:
        try:
            lViewResult = subprocess.run(
                [lGh, "release", "view", "--json", "tagName"],
                capture_output=True, text=True, cwd=SCRIPT_DIR
            )
            if lViewResult.returncode != 0:
                print(f"[dl]    FEHLER: {lViewResult.stderr.strip()}")
                return False
            version = json.loads(lViewResult.stdout).get("tagName", "")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[dl]    FEHLER: {e}")
            return False

    print(f"[dl]    Lade von Release {version} herunter ...")
    lDownloadResult = subprocess.run(
        [lGh, "release", "download", version,
         "--pattern", "KuchenApp_standalone_*.zip",
         "--dir", RELEASE_DIR, "--clobber"],
        capture_output=True, text=True, cwd=SCRIPT_DIR
    )
    if lDownloadResult.returncode != 0:
        print(f"[dl]    FEHLER: {lDownloadResult.stderr.strip()}")
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
    compile_docs()
    create_dirs()
    copy_files()
    write_readme()
    create_zip()
    print()
    print("--- Source-Release ---")
    print(f"  ZIP:  {ZIP_PATH}")


def main():
    lArgumentParser = argparse.ArgumentParser(description="Build-Skript fuer KuchenApp Releases.")
    lArgumentParser.add_argument("--source", action="store_true", help="Nur das Source-Bundle bauen.")
    lArgumentParser.add_argument("--standalone", action="store_true", help="Nur die Standalone-Version fuer das aktuelle OS bauen.")
    lArgs = lArgumentParser.parse_args()

    lCiStandalone = lArgs.standalone
    lCiSource = lArgs.source

    # Aktuelle Version anzeigen
    major, minor, patch = read_version()
    current_ver = f"v{major}.{minor}.{patch}"

    print("=" * 40)
    print("  KuchenApp Release Build")
    if lCiStandalone:
        print(f"  Modus: Standalone ({OS_TAG})")
    elif lCiSource:
        print("  Modus: Source-Bundle (CI)")
    else:
        print(f"  Modus: Release")
        print(f"  Aktuelle Version: {current_ver}")
    print("=" * 40)
    print()

    if lCiStandalone:
        clean_build()
        compile_ui()
        compile_docs()
        create_dirs()
        copy_files()
        if build_standalone():
            print()
            print(f"--- Standalone {OS_TAG.capitalize()} ---")
            lStandaloneZip = os.path.join(RELEASE_DIR, f"KuchenApp_standalone_{OS_TAG}.zip")
            print(f"  ZIP:  {lStandaloneZip}")
        else:
            print("[exe]   Standalone-Build fehlgeschlagen.")
            sys.exit(1)

    elif lCiSource:
        _build_source()

    else:
        # Normaler Aufruf: Patch hochzaehlen, Source bauen, Release erstellen
        if not _ensure_clean_worktree():
            sys.exit(1)
        release_version = bump_patch()
        _build_source()
        print()
        create_release(release_version)

    print()
    print("Fertig!")


if __name__ == "__main__":
    main()
