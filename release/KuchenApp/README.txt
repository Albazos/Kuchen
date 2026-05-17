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
