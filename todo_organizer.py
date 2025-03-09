#!/usr/bin/env python3
"""
Obsidian ToDo Finder - ToDo Organizer Module

Dieses Modul stellt Funktionen zur Organisation und Gruppierung von ToDo-Einträgen bereit.
"""

import datetime
from collections import defaultdict
from typing import Dict, List, Tuple

def organize_todos_by_date(
        todos_by_file: Dict[str, List[Tuple[str, bool, str, int, bool, bool]]],
        file_dates: Dict[str, datetime.datetime]
) -> Dict[Tuple[int, int], Dict[str, List[Tuple[str, bool, str, int, bool, bool]]]]:
    """
    Organisiert ToDos nach Monat und Jahr und dann nach Datei.

    Args:
        todos_by_file: Dictionary, das Dateipfade auf Listen von ToDo-Einträgen abbildet
        file_dates: Dictionary, das Dateipfade auf ihre Änderungsdaten abbildet

    Returns:
        Ein Dictionary, das (Jahr, Monat)-Tupel auf Dictionaries von Dateipfaden und ToDo-Einträgen abbildet
    """
    todos_by_date = defaultdict(dict)

    for file_path, todos in todos_by_file.items():
        date = file_dates[file_path]
        year_month = (date.year, date.month)
        todos_by_date[year_month][file_path] = todos

    return todos_by_date

def format_month_year(year: int, month: int) -> str:
    """
    Formatiert Jahr und Monat wie angegeben (MonatJahr).

    Args:
        year: Das Jahr
        month: Der Monat (1-12)

    Returns:
        Ein formatierter String im Format "MonatJahr"
    """
    # Verwende den deutschen Monatsnamen
    month_names = [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]
    month_name = month_names[month - 1]
    return f"{month_name}{year}"