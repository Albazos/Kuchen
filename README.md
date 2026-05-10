# KuchenApp

KuchenApp ist eine Desktop-Anwendung zur Verwaltung von Kuchen-Listen und zum Versenden von Erinnerungs-Mails ueber IServ.

Das Projekt ist waehrend meiner Schulzeit entstanden, um nachzuhalten, wer als Naechstes Kuchen mitbringen muss. Da ich die Schule bald verlasse, ist dieses Repository so vorbereitet, dass Lehrkraefte und Schueler das Projekt weiterverwenden, pflegen und erweitern koennen.

## Ziele

- Kuchen-Termine und Eintraege in einer Tabelle verwalten
- Daten als CSV importieren, bearbeiten und speichern
- Empfaengerlisten fuer Klassen verwalten
- Erinnerungs-Mails ueber IServ versenden
- Das Projekt fuer kuenftige Schueler leicht erweiterbar halten

## Technologien

- Python 3.10+
- PySide6 / Qt 6
- CSV-Dateien fuer die Datenhaltung
- INI-Datei fuer Einstellungen
- PyInstaller fuer Builds

## Projektstruktur

```text
Kuchen/
|- develop/
|  |- KuchenMain.py
|  |- src/
|  |- ui/
|  |- Data/
|  `- assets/
|- docs/
|- build_ui.py
|- build_release.py
|- open_designer.py
`- requirements.txt
```

## Starten

1. Python 3.10 oder neuer installieren
2. Abhaengigkeiten installieren
3. Anwendung starten

```bash
pip install -r requirements.txt
python develop/KuchenMain.py
```

## Demo- und Standarddaten

Die im Repository enthaltenen CSV-Dateien wurden von mir auch im Schulalltag verwendet und dienen hier gleichzeitig als Standard- bzw. Demo-Daten.

Wichtig:
- Vor einer Weitergabe ausserhalb des vorgesehenen Schulkontexts sollte geprueft werden, ob enthaltene Daten weiterhin veroeffentlicht werden duerfen.
- Fuer eine spaetere breitere Nutzung empfiehlt es sich, zusaetzlich anonymisierte Beispieldaten bereitzustellen.

## Plattformen

Die Anwendung ist fuer Windows und Linux gedacht.

Helper-Skripte:
- `build_ui.py` kompiliert `.ui`-Dateien nach Python
- `open_designer.py` oeffnet `.ui`-Dateien im Qt Designer
- `build_release.py` erstellt Release-Bundles

## Weiterentwicklung

Beitraege sind willkommen. Fuer groessere Aenderungen bitte einen Pull Request erstellen, damit die Aenderungen nachvollziehbar bleiben.

Die wichtigsten Hinweise fuer Beitraege stehen in [CONTRIBUTING.md](CONTRIBUTING.md).

## Uebergabe und Zukunft

Dieses Projekt kann auch nach meiner Schulzeit weiterverwendet werden. Ein Vorschlag fuer Rollen, Zugriff und Pflege steht in [HANDOVER_PROPOSAL.md](HANDOVER_PROPOSAL.md).

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Details stehen in [LICENSE](LICENSE).
