#!/usr/bin/env python3
"""
Obsidian Todo Finder

Durchsucht eine Obsidian Vault nach ToDo-Einträgen (- [ ], - [x]) und generiert eine
Zusammenfassung in einer Markdown-Datei im Root-Verzeichnis.

Author: Serge Decker
Version: 1.0.0
GitHub: https://github.com/egemasta/obsidian-todo-finder
Web: https://sergedecker.ch/
License: MIT

Copyright (c) 2025 Serge Decker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Warum dieses Skript?
-------------------
Dieses Skript wurde entwickelt, um Obsidian-Nutzer dabei zu unterstützen,
alle ToDo-Einträge über ihre gesamte Wissensdatenbank hinweg zu verfolgen.
Es löst das Problem der verteilten ToDo-Einträge in verschiedenen Notizen,
indem es eine zentrale, nach Datum sortierte Übersicht aller offenen und
erledigten Aufgaben erstellt.

Changelog:
----------
v1.0.0 (2025-03-09)
- Erste öffentliche Version
- Erkennung von ToDo-Einträgen mit und ohne Checkbox
- Sortierung nach Datum (neuste zuerst)
- Separate Anzeige von offenen und erledigten ToDos
- Spezielle Behandlung von "ToDo Sammler"-Einträgen
- Gruppierung nach Monat und Jahr
- Ignorieren von ToDo-Templates (unter "## ✅ ToDo" Überschriften)
- Separate Auflistung leerer ToDos (ohne Text)
"""

import os
import argparse
from summary_generator import generate_todo_summary

def main():
    """
    Haupteinstiegspunkt für das Skript.
    """
    # Fester Pfad zur Obsidian Vault
    vault_path = os.path.join("\\\\Orion\\home\\obsidian")

    # Standardausgabedatei im Vault-Root
    output_file = None

    # ToDo-Sammler-Tag
    todo_collector_tag = "ToDo Sammler"

    # Ermögliche optionale Kommandozeilenargumente, die die Standardwerte überschreiben
    parser = argparse.ArgumentParser(
        description="Sammelt und fasst ToDos aus einer Obsidian Vault zusammen"
    )
    parser.add_argument(
        "-v", "--vault",
        help="Pfad zum Root-Verzeichnis der Obsidian Vault (Standard: \\\\Orion\\home\\obsidian)",
        default=vault_path
    )
    parser.add_argument(
        "-o", "--output",
        help="Pfad zur Ausgabedatei (Standard: parser_DATETIME_todo.md im Vault-Root)",
        default=output_file
    )
    parser.add_argument(
        "-t", "--tag",
        help="Text-Tag zur Identifizierung spezieller ToDo-Sammler (Standard: 'ToDo Sammler')",
        default=todo_collector_tag
    )

    # Verwende die Argumente oder die Standard-Werte
    args = parser.parse_args()

    # Generiere die ToDo-Zusammenfassung
    output_file = generate_todo_summary(args.vault, args.output, args.tag)
    print(f"ToDo-Zusammenfassung generiert: {output_file}")

if __name__ == "__main__":
    main()