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
  ├── KuchenMain.py            <- Hauptprogramm (hier starten)
  ├── README.txt               <- Diese Datei
  ├── assets/
  │   └── kuchen_icon.svg      <- App-Icon
  ├── src/
  │   ├── DataManager.py       <- Datenverwaltung (CSV lesen/schreiben)
  │   ├── KuchenMailManager.py <- Dialog fuer Mail-Liste
  │   ├── LoginDialog.py       <- Login-Dialog fuer IServ
  │   ├── IservMailManager.py  <- Mail-Versand ueber IServ API
  │   └── IServAPIEdited_standalone.py  <- IServ API (nur stdlib, kein pip)
  ├── ui/
  │   ├── UIMainWindow_ui.py   <- Hauptfenster UI (generiert)
  │   ├── UIMailsDialog_ui.py  <- Mail-Dialog UI (generiert)
  │   └── UILoginDialog_ui.py  <- Login-Dialog UI (generiert)
  └── Data/
      ├── CakeData.csv         <- Kuchen-Daten
      └── Klassen/
          └── EITB23A.csv      <- Klassenliste


Starten:
  cd KuchenApp
  python KuchenMain.py


Hinweise:
  - Die IServ-API (IServAPIEdited_standalone.py) benoetigt KEINE
    zusaetzlichen pip-Pakete. Sie nutzt nur die Python-Standardbibliothek.
  - PySide6 ist die einzige externe Abhaengigkeit die installiert werden muss.
  - Die CSV-Dateien im Data/-Ordner koennen angepasst werden.
