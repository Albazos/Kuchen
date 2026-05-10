# Contributing

Vielen Dank fuer dein Interesse an der Weiterentwicklung von KuchenApp.

## Grundidee

Kleinere und groessere Verbesserungen sind willkommen. Damit das Projekt auch fuer Lehrkraefte und Schueler spaeter gut wartbar bleibt, sollen Aenderungen moeglichst nachvollziehbar und konsistent eingebracht werden.

## Empfohlener Ablauf

1. Repository forken oder einen Branch anlegen
2. Aenderungen umsetzen
3. Wenn moeglich kurz lokal testen
4. Pull Request mit kurzer Beschreibung erstellen

## Was in einen Pull Request gehoert

- Was wurde geaendert
- Warum war die Aenderung noetig
- Ob Verhalten in der GUI betroffen ist
- Ob CSV-, Settings- oder Mail-Funktionalitaet betroffen ist

## Coding-Regeln in diesem Projekt

Bitte die bestehende Namenskonvention beibehalten:

- Lokale Variablen mit `lName`
- Argumente mit `aName`
- Member mit `mName`
- Klassen mit `cName` bzw. bestehende Klassenpraefixe beibehalten
- Funktionen mit klaren, beschreibenden Namen

Weitere Hinweise:

- Nach Moeglichkeit plattformneutral fuer Windows und Linux entwickeln
- Dateipfade immer ueber `os.path.join(...)` behandeln
- Keine geheimen Zugangsdaten, Passwoerter oder Tokens committen
- UI-Aenderungen nach Moeglichkeit mit den `.ui`-Dateien und nicht nur mit generierten `_ui.py`-Dateien pflegen

## Inhaltliche Regeln

- Keine sensiblen personenbezogenen Daten ohne ausdrueckliche Freigabe ins Repository aufnehmen
- Bei Aenderungen an Standarddaten sorgfaeltig pruefen, ob diese fuer den vorgesehenen Einsatzzweck geeignet sind
- Bei Aenderungen am Mail-Versand bitte besonders vorsichtig testen

## Maintainer-Hinweis

Wenn du als Schueler beitragen willst, aber keinen direkten Schreibzugriff hast, ist das normal. Bitte arbeite ueber Forks und Pull Requests.

Direkter Schreibzugriff sollte nur an wenige verantwortliche Personen vergeben werden, zum Beispiel:

- betreuende Lehrkraft
- aktuelle Projektverantwortliche
- verlaessliche Schueler mit Wartungsaufgaben
