#!/usr/bin/env python3
"""
Obsidian ToDo Finder - Summary Generator Module

Dieses Modul stellt Funktionen zur Generierung einer strukturierten ToDo-Zusammenfassung bereit.
"""

import datetime
import os
from typing import Optional

from file_utils import find_markdown_files, get_file_date
from todo_organizer import organize_todos_by_date, format_month_year
from todo_parser import extract_todos


def generate_todo_summary(
        vault_path: str,
        output_file: Optional[str] = None,
        todo_collector_tag: str = "ToDo Sammler"
) -> str:
    """
    Generiert eine Zusammenfassung der ToDos aus einer Obsidian Vault.

    Args:
        vault_path: Pfad zum Root-Verzeichnis der Obsidian Vault
        output_file: Pfad zur Ausgabe-Markdown-Datei (optional)
        todo_collector_tag: Text zur Identifizierung spezieller ToDo-Sammler-Einträge

    Returns:
        Pfad zur generierten Datei
    """
    # Finde alle Markdown-Dateien
    markdown_files = find_markdown_files(vault_path)
    print(f"Gefunden: {len(markdown_files)} Markdown-Dateien")

    # Extrahiere ToDos und verfolge Dateidaten
    todos_by_file = {}
    file_dates = {}

    for file_path in markdown_files:
        todos = extract_todos(file_path, todo_collector_tag)
        if todos:  # Nur Dateien einschließen, die ToDos enthalten
            todos_by_file[file_path] = todos
            file_dates[file_path] = get_file_date(file_path)

    print(f"ToDos in {len(todos_by_file)} Dateien gefunden")

    # Organisiere ToDos nach Datum
    todos_by_date = organize_todos_by_date(todos_by_file, file_dates)

    # Sortiere Daten in umgekehrter Reihenfolge (neueste zuerst)
    sorted_dates = sorted(todos_by_date.keys(), reverse=True)

    # Generiere den Ausgabedateinamen, wenn nicht angegeben
    if output_file is None:
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(vault_path, f"parser_{current_datetime}_todo.md")

    # Sammle leere ToDos
    empty_todos = []

    # Generiere die Zusammenfassung als Markdown
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"# ToDo Zusammenfassung\n\n")
        file.write(f"Generiert am: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Zuerst prüfen, ob es ToDo-Sammler gibt
        collector_todos = []
        for year_month in sorted_dates:
            for file_path in todos_by_date[year_month]:
                for todo in todos_by_date[year_month][file_path]:
                    if todo[4]:  # is_collector Flag
                        collector_todos.append((year_month, file_path, todo))

        # Schreibe ToDo-Sammler-Abschnitt, wenn welche existieren
        if collector_todos:
            file.write("## ToDo Sammler\n\n")
            for (year, month), file_path, (todo_text, is_completed, file_link, indentation, _, _) in collector_todos:
                month_year = format_month_year(year, month)
                status = "✓" if is_completed else "☐"
                file.write(f"- {status} {file_link} ({month_year}): {todo_text}\n")
            file.write("\n")

        # Schreibe reguläre ToDos nach Datum
        for year, month in sorted_dates:
            # Schreibe die Monat-Jahr-Überschrift
            file.write(f"## {format_month_year(year, month)}\n\n")

            # Sammle alle offenen und abgeschlossenen ToDos für diesen Monat mit ihren Dateiinfos
            open_todos = []
            completed_todos = []

            # Sortiere Dateien nach Datum innerhalb dieses Monats (neueste zuerst)
            sorted_files = sorted(
                todos_by_date[(year, month)].keys(),
                key=lambda f: file_dates[f],
                reverse=True
            )

            for file_path in sorted_files:
                todos = todos_by_date[(year, month)][file_path]
                file_name = os.path.basename(file_path).replace('.md', '')
                file_link = f"[[{file_name}]]"

                for todo in todos:
                    todo_text, is_completed, _, indentation, is_collector, is_empty = todo

                    # Überspringe Sammler-ToDos in den regulären Abschnitten, um Duplikate zu vermeiden
                    if is_collector:
                        continue

                    # Sammle leere ToDos separat
                    if is_empty:
                        empty_todos.append((file_link, is_completed, (year, month)))
                        continue

                    # Füge Einrückung basierend auf der ursprünglichen Einrückungsebene hinzu
                    indent_str = "    " * (indentation // 4)  # Ungefähre Einrückung
                    todo_entry = f"{indent_str}- {file_link}: {todo_text}\n"
                    if is_completed:
                        completed_todos.append(todo_entry)
                    else:
                        open_todos.append(todo_entry)

            # Schreibe offene ToDos
            if open_todos:
                file.write("### Offene ToDos\n\n")
                for todo in open_todos:
                    file.write(todo)
                file.write("\n")

            # Schreibe abgeschlossene ToDos
            if completed_todos:
                file.write("### Erledigte ToDos\n\n")
                for todo in completed_todos:
                    file.write(todo)
                file.write("\n")

        # Schreibe leere ToDos in einem separaten Abschnitt
        if empty_todos:
            file.write("## Leere ToDos\n\n")

            # Sortiere leere ToDos nach Datum (neueste zuerst)
            empty_todos.sort(key=lambda x: x[2], reverse=True)

            # Trenne in offene und erledigte leere ToDos
            open_empty = []
            completed_empty = []

            for file_link, is_completed, (year, month) in empty_todos:
                month_year = format_month_year(year, month)
                todo_entry = f"- {file_link} ({month_year})\n"

                if is_completed:
                    completed_empty.append(todo_entry)
                else:
                    open_empty.append(todo_entry)

            if open_empty:
                file.write("### Offene leere ToDos\n\n")
                for todo in open_empty:
                    file.write(todo)
                file.write("\n")

            if completed_empty:
                file.write("### Erledigte leere ToDos\n\n")
                for todo in completed_empty:
                    file.write(todo)
                file.write("\n")

    return output_file