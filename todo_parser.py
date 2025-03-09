#!/usr/bin/env python3
"""
Obsidian ToDo Finder - ToDo Parser Module

Dieses Modul stellt Funktionen zum Extrahieren von ToDo-Einträgen aus Markdown-Dateien bereit.
"""

import os
import re
from typing import List, Tuple

from file_utils import extract_frontmatter

def extract_todos(file_path: str, todo_collector_tag: str = "ToDo Sammler") -> List[Tuple[str, bool, str, int, bool, bool]]:
    """
    Extrahiert ToDo-Einträge aus einer Markdown-Datei.

    Args:
        file_path: Pfad zur Markdown-Datei
        todo_collector_tag: Text zur Identifizierung spezieller ToDo-Sammler-Einträge

    Returns:
        Eine Liste von Tupeln mit (todo_text, is_completed, link_to_file, indentation_level, is_collector, is_empty)
    """
    todos = []
    file_name = os.path.basename(file_path).replace('.md', '')
    file_link = f"[[{file_name}]]"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Extrahiere Frontmatter falls vorhanden
            _, content_without_frontmatter = extract_frontmatter(content)

            # Teile in Zeilen, um Einrückungsebenen zu verfolgen
            lines = content_without_frontmatter.split('\n')

            # Flag, um ToDos unter einer "## ✅ ToDo" Überschrift zu ignorieren
            under_todo_template_heading = False

            for i, line in enumerate(lines):
                # Prüfe auf ToDo Template Überschrift
                if re.match(r'^##\s+✅\s+ToDo', line):
                    under_todo_template_heading = True
                    continue
                # Reset das Flag bei jeder anderen Überschrift
                elif line.startswith('#'):
                    under_todo_template_heading = False
                    continue

                # Ignoriere ToDos unter der ToDo Template Überschrift
                if under_todo_template_heading:
                    continue

                # Finde ToDo-Einträge mit beliebiger Einrückung
                todo_match = re.match(r'^(\s*)- \[([ xX])\] (.*?)$', line)
                if todo_match:
                    indentation = len(todo_match.group(1))
                    is_completed = todo_match.group(2).lower() == 'x'
                    todo_text = todo_match.group(3).strip()

                    # Prüfe, ob es sich um einen leeren ToDo-Eintrag handelt
                    is_empty = todo_text == ""

                    # Prüfe, ob es sich um einen speziellen "ToDo Sammler" Eintrag handelt
                    is_collector = todo_collector_tag in todo_text

                    todos.append((todo_text, is_completed, file_link, indentation, is_collector, is_empty))
    except (UnicodeDecodeError, IOError) as e:
        print(f"Fehler beim Lesen der Datei {file_path}: {e}")

    return todos