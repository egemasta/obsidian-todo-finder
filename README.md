# Obsidian ToDo Finder

## Beschreibung | Description

**[DE]** Ein modulares Python-Framework zur systematischen Erfassung und Organisation von ToDo-Einträgen in einer Obsidian-Wissensdatenbank. Die Architektur basiert auf einem komponentenbasierten Design, das die Wiederverwendbarkeit einzelner Module in anderen Projekten ermöglicht.

**[EN]** A modular Python framework for systematically collecting and organizing ToDo entries across an Obsidian vault. The architecture is based on a component-based design that enables the reusability of individual modules in other projects.

## Systemarchitektur | System Architecture

Das System basiert auf einer **modularen Mehrschichtarchitektur** mit folgenden Schlüsselkomponenten:

### Modulare Struktur | Modular Structure

```
obsidian_todo_finder/
│
├── __init__.py             # Package-Definition
├── file_utils.py           # Hilfsfunktionen für Dateisystemoperationen
├── todo_parser.py          # Funktionen zum Extrahieren von ToDo-Einträgen
├── todo_organizer.py       # Funktionen zur Organisation von ToDo-Einträgen
├── summary_generator.py    # Funktionen zur Generierung der Zusammenfassung
│
├── main.py                 # Hauptskript als Einstiegspunkt
├── requirements.txt        # Abhängigkeiten
├── setup.py                # Setup-Skript für die Installation als Paket
└── README.md               # Projektdokumentation
```

### Architekturprinzipien | Architectural Principles

Das System implementiert folgende Designprinzipien:

#### Schichtenmodell | Layer Model

- **Dateisystem-Interface** (`file_utils.py`): Abstraktion des Zugriffs auf Obsidian-Vaults
- **Parsing-Engine** (`todo_parser.py`): Extraktion und Klassifizierung von ToDo-Elementen
- **Organisationslogik** (`todo_organizer.py`): Strukturierung und Gruppierung der Daten
- **Präsentationsschicht** (`summary_generator.py`): Generierung des finalen Outputs

#### Modularer Datenfluss | Modular Data Flow

```
Dateisystem → Parsing → Organisation → Ausgabegenerierung
file_utils.py → todo_parser.py → todo_organizer.py → summary_generator.py
```

## Modulbeschreibungen | Module Descriptions

### file_utils.py

**[DE]** Stellt Hilfsfunktionen für Dateisystemoperationen bereit, einschließlich der rekursiven Durchsuchung von Verzeichnissen, Extraktion von YAML-Frontmatter und Datumsermittlung aus Dateien.

**[EN]** Provides utility functions for file system operations, including recursive directory scanning, YAML frontmatter extraction, and date determination from files.

#### Kernfunktionalitäten | Core Functions:

- `find_markdown_files(vault_path)`: Rekursive Suche nach .md-Dateien
- `extract_frontmatter(content)`: Extraktion von YAML-Metadaten
- `get_file_date(file_path)`: Intelligente Datumserkennung

### todo_parser.py

**[DE]** Implementiert die Parsing-Engine für ToDo-Einträge in Markdown-Dateien, mit Unterstützung für verschiedene ToDo-Formate und Kontext-Erkennung.

**[EN]** Implements the parsing engine for ToDo entries in markdown files, with support for various ToDo formats and context detection.

#### Kernfunktionalitäten | Core Functions:

- `extract_todos(file_path, todo_collector_tag)`: Extraktion von ToDo-Einträgen mit Metadaten

### todo_organizer.py

**[DE]** Enthält Funktionen zur Strukturierung und Organisation der ToDo-Daten nach zeitlichen und inhaltlichen Kriterien.

**[EN]** Contains functions for structuring and organizing ToDo data according to temporal and content-related criteria.

#### Kernfunktionalitäten | Core Functions:

- `organize_todos_by_date(todos_by_file, file_dates)`: Zeitbasierte Gruppierung
- `format_month_year(year, month)`: Formatierung von Zeitangaben

### summary_generator.py

**[DE]** Stellt die Präsentationsschicht dar, die die verarbeiteten Daten in ein strukturiertes Markdown-Dokument umwandelt.

**[EN]** Represents the presentation layer that transforms the processed data into a structured markdown document.

#### Kernfunktionalitäten | Core Functions:

- `generate_todo_summary(vault_path, output_file, todo_collector_tag)`: Erstellung der Zusammenfassung

## Kernfunktionalitäten | Core Functionalities

- **Vollständige Vault-Analyse**: Rekursive Durchsuchung aller Markdown-Dateien im Vault
- **Intelligente ToDo-Erkennung**: Erfassung von offenen (`- [ ]`) und erledigten (`- [x]`) Aufgaben
- **Strukturierte Ausgabe**: Übersichtliche Zusammenfassung nach Monaten und Jahren geordnet
- **Chronologische Sortierung**: Neueste Einträge werden priorisiert dargestellt
- **Kontext-Bewahrung**: Beibehaltung der ursprünglichen Einrückungsebenen und Verlinkung zur Quelldatei
- **Spezialbehandlung**: Separate Darstellung leerer ToDos und `ToDo Sammler`-Einträge
- **Template-Filter**: Ignorieren von ToDos unter Template-Überschriften (`## ✅ ToDo`)

## Technische Voraussetzungen | Technical Requirements

- Python 3.11 oder höher
- PyYAML-Bibliothek

## Installation und Integration | Installation and Integration

### Als eigenständiges Tool | As a standalone tool

1. Repository klonen:

    ```bash
    git clone https://github.com/[dein-username]/obsidian-todo-collector.git
    cd obsidian-todo-collector
    ```

2. Abhängigkeiten installieren:

    ```bash
    pip install -r requirements.txt
    ```

3. Als Paket installieren (optional):

    ```bash
    pip install -e .
    ```


### Als Bibliothek in anderen Projekten | As a library in other projects

#### Installation der Bibliothek | Library Installation

```bash
pip install git+https://github.com/[dein-username]/obsidian-todo-collector.git
```

#### Import einzelner Module | Import individual modules

```python
# Beispiel: Nur den ToDo-Parser verwenden
from obsidian_todo_collector.todo_parser import extract_todos

# Beispiel: Nur den Dateisystem-Utility verwenden
from obsidian_todo_collector.file_utils import find_markdown_files, extract_frontmatter

# Beispiel: Nur den Organisator verwenden
from obsidian_todo_collector.todo_organizer import organize_todos_by_date

# Beispiel: Die Zusammenfassungsgenerierung verwenden
from obsidian_todo_collector.summary_generator import generate_todo_summary
```

## Verwendung | Usage

### Kommandozeileninterface | Command-Line Interface

#### Grundlegende Anwendung | Basic Usage

```bash
python -m obsidian_todo_collector.main -v "Pfad/zu/deinem/obsidian/vault"
```

Oder, wenn als Paket installiert:

```bash
obsidian-todo-collector -v "Pfad/zu/deinem/obsidian/vault"
```

#### Ausgabedatei anpassen | Custom Output File

```bash
python -m obsidian_todo_collector.main -v "Pfad/zu/deinem/obsidian/vault" -o "custom_todo_summary.md"
```

#### ToDo-Sammler-Tag anpassen | Custom ToDo Collector Tag

```bash
python -m obsidian_todo_collector.main -v "Pfad/zu/deinem/obsidian/vault" -t "Projekte"
```

### Programmatische Nutzung | Programmatic Usage

```python
from obsidian_todo_collector.summary_generator import generate_todo_summary

# Generiere eine ToDo-Zusammenfassung
output_file = generate_todo_summary(
    vault_path="/pfad/zu/deinem/obsidian/vault",
    output_file="custom_output.md",
    todo_collector_tag="ToDo Sammler"
)

print(f"ToDo-Zusammenfassung wurde erstellt: {output_file}")
```

### Parameter | Parameters

|Parameter|Beschreibung|Standard|
|---|---|---|
|`-v, --vault`|Pfad zum Obsidian Vault|`\\Orion\home\obsidian`|
|`-o, --output`|Ausgabedateiname|`parser_DATETIME_todo.md`|
|`-t, --tag`|Spezifischer Tag für ToDo-Sammler|`ToDo Sammler`|

## Beispiel-Ausgabe | Example Output

```markdown
# ToDo Zusammenfassung

Generiert am: 2025-03-09 14:30:45

## ToDo Sammler

- ☐ [[Projektplanung]] (März2025): ToDo Sammler für Q2 Projekte
- ✓ [[Meeting-Notizen]] (Februar2025): ToDo Sammler für Teamabsprachen

## März2025

### Offene ToDos

- [[Forschung]]: Neue Quellen für Abschnitt 3 finden
- [[Projektplanung]]: Budget für Q2 finalisieren

### Erledigte ToDos

- [[Notizen]]: Meeting-Protokoll an Team senden

## Februar2025

### Offene ToDos

- [[Ideen]]: Konzept für neue Feature-Reihe ausarbeiten

## Leere ToDos

### Offene leere ToDos

- [[Notizen]] (März2025)

### Erledigte leere ToDos

- [[Archiv]] (Januar2025)
```

## Erweiterbarkeit | Extensibility

Das modulare Design ermöglicht die einfache Erweiterung um zusätzliche Funktionen:

1. **Anpassung der Parsing-Logik**: Erweitern Sie `todo_parser.py` um zusätzliche ToDo-Formate
2. **Eigene Ausgabeformate**: Implementieren Sie neue Generator-Module basierend auf `summary_generator.py`
3. **Alternative Datenquellen**: Erweitern Sie `file_utils.py` für die Unterstützung anderer Notiz-Systeme

## Beitragen | Contributing

Beiträge zum Projekt sind willkommen! Bitte beachten Sie die folgenden Schritte:

1. Fork des Repositories erstellen
2. Feature-Branch anlegen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add some AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request erstellen

## Lizenz | License

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

## Kontakt | Contact

Serge Decker - [sergedecker.ch](https://sergedecker.ch/)

Projekt-Link: [https://github.com/egemasta/obsidian-todo-finder](https://github.com/egemasta/obsidian-todo-finder)