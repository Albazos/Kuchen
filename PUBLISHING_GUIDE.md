# Publishing Guide

Diese Anleitung beschreibt, wie du das `Kuchen`-Repository ohne GitHub-Organisation veroeffentlichst und gleichzeitig sicherstellst, dass Aenderungen nur ueber Pull Requests und mit deiner Freigabe in `develop` landen.

## Ziel

Am Ende soll das Repository so aufgesetzt sein:

- das Repository ist oeffentlich sichtbar
- Lehrkraft und Schueler koennen den Code sehen
- Beitraege laufen ueber Pull Requests
- direkte Aenderungen am Hauptbranch `develop` sind gesperrt
- ein Merge braucht eine Freigabe
- idealerweise braucht es deine Freigabe als Code Owner

## Empfohlene Reihenfolge

1. Repository auf `public` stellen
2. Lehrkraft optional als Collaborator hinzufuegen
3. Branch `develop` per Ruleset schuetzen
4. `CODEOWNERS` einrichten
5. Pull-Request-Workflow kommunizieren

## 1. Repository oeffentlich machen

Wenn das Repository oeffentlich ist, kann jeder den Code lesen und forken. Schreibzugriff bekommt dadurch aber noch niemand.

### Schritte

1. Repository auf GitHub oeffnen
2. `Settings` anklicken
3. In `General` ganz nach unten zu `Danger Zone` scrollen
4. `Change repository visibility` auswaehlen
5. `Public` bestaetigen

### Wirkung

- Jeder kann das Projekt ansehen
- Jeder kann einen Fork erstellen
- Issues und Pull Requests koennen von anderen genutzt werden
- Schreibzugriff bleibt weiterhin nur bei dir und eingeladenen Collaborators

## 2. Lehrkraft als Collaborator hinzufuegen

Das ist nur noetig, wenn die Lehrkraft direkt im Repository mitarbeiten oder spaeter Pull Requests besser mitverwalten soll.

### Schritte

1. `Settings` oeffnen
2. Im linken Menue `Collaborators` auswaehlen
3. `Add people` klicken
4. GitHub-Benutzernamen der Lehrkraft eingeben
5. Einladung absenden

### Hinweis

Fuer reines Lesen ist keine Einladung noetig, weil das Repository ja oeffentlich ist.

## 3. Branch `develop` schuetzen

Da dein Arbeitsbranch jetzt `develop` ist, sollte genau dieser Branch abgesichert werden.

### Schritte

1. `Settings` oeffnen
2. Links `Rules` > `Rulesets`
3. `New ruleset`
4. `New branch ruleset`
5. Als Namen zum Beispiel `Protect develop` vergeben
6. Als Zielbranch `develop` auswaehlen

### Diese Regeln aktivieren

- `Require a pull request before merging`
- `Require approvals`
- `Require approval of the most recent reviewable push`
- `Dismiss stale pull request approvals when new commits are pushed`
- `Require conversation resolution before merging`
- `Block force pushes`
- `Restrict deletions`

### Empfohlene Werte

- Required approvals: `1`

### Wirkung

- Niemand kann einfach direkt nach `develop` mergen
- Wenn nach einer Freigabe neue Commits gepusht werden, muss erneut geprueft werden
- Offene Review-Kommentare muessen vor dem Merge geklaert werden

## 4. CODEOWNERS einrichten

Wenn du moechtest, dass moeglichst deine Freigabe gebraucht wird, solltest du `CODEOWNERS` verwenden.

Lege eine Datei an:

```text
.github/CODEOWNERS
```

### Beispielinhalt

```text
* @DEIN_GITHUB_USERNAME
/.github/ @DEIN_GITHUB_USERNAME
```

Danach aktivierst du im Ruleset zusaetzlich:

- `Require review from code owners`

### Wirkung

- Du wirst automatisch als Reviewer angefragt
- Pull Requests koennen nicht ohne Code-Owner-Freigabe gemerged werden
- Wenn nur du als Code Owner eingetragen bist, ist praktisch deine Freigabe noetig

## 5. Empfohlener Pull-Request-Ablauf

### Fuer Schueler ohne Schreibzugriff

1. Repository forken
2. Im eigenen Fork einen Branch anlegen
3. Aenderungen committen und pushen
4. Pull Request gegen dein Original-Repository erstellen
5. Review abwarten
6. Nach Freigabe wird in `develop` gemerged

### Fuer Collaborators mit Schreibzugriff

1. Niemals direkt auf `develop` arbeiten
2. Immer einen eigenen Branch anlegen
3. Pull Request nach `develop` erstellen
4. Review abwarten
5. Erst nach Freigabe mergen

## 6. Was du Lehrkraft und Schuelern sagen kannst

Ein kurzer Standardtext koennte so aussehen:

> Das Repository ist oeffentlich, damit der Code langfristig sichtbar und nutzbar bleibt. Bitte arbeitet nicht direkt auf `develop`, sondern immer ueber Branches und Pull Requests. Aenderungen werden vor dem Merge geprueft. Wer das Projekt aktiv mitpflegen moechte, kann sich melden oder zuerst einen Pull Request einreichen.

## 7. Empfohlene Grundeinstellung fuer dein Projekt

Fuer `Kuchen` wuerde ich dieses Setup empfehlen:

- Repository: `public`
- Hauptbranch: `develop`
- Branch-Regeln: Pull Request erforderlich
- Required approvals: `1`
- Code Owners: aktiviert
- Direkter Schreibzugriff: nur du und optional Lehrkraft
- Weitere Schueler: ueber Forks und Pull Requests

## 8. Wichtige Hinweise

### Wenn nur du als Code Owner eingetragen bist

Dann blockierst du alle Merges, sobald du nicht mehr erreichbar bist.

Deshalb gibt es zwei sinnvolle Varianten:

### Variante A: zuerst streng

- nur du bist Code Owner
- gut fuer die erste Uebergangsphase

### Variante B: spaeter wartbarer

```text
* @DEIN_GITHUB_USERNAME @LEHRER_USERNAME
/.github/ @DEIN_GITHUB_USERNAME @LEHRER_USERNAME
```

Dann kann entweder du oder die Lehrkraft freigeben.

## 9. Optional spaeter

Wenn das Projekt nach deiner Schulzeit weiterlebt, kannst du spaeter noch ergaenzen:

- `CODEOWNERS`
- Pull-Request-Template
- Issue-Templates
- GitHub Actions fuer einfache Checks

## 10. Passende GitHub-Dokumentation

- Repository-Sichtbarkeit aendern:
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility
- Collaborators in persoenlichen Repositories:
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository
- Rulesets fuer ein Repository:
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
- Verfuegbare Ruleset-Regeln:
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- CODEOWNERS:
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
