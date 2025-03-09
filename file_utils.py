#!/usr/bin/env python3
"""
Obsidian ToDo Finder - File Utilities Module

Dieses Modul stellt Hilfsfunktionen für Dateisystemoperationen bereit.
"""

import os
import re
import datetime
import yaml
from typing import Dict, List, Tuple, Optional, Any

def find_markdown_files(vault_path: str) -> List[str]:
    """
    Findet rekursiv alle Markdown-Dateien im angegebenen Verzeichnis.

    Args:
        vault_path: Pfad zum Root-Verzeichnis der Obsidian Vault

    Returns:
        Eine Liste von Pfaden zu Markdown-Dateien
    """
    markdown_files = []
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def extract_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Extrahiert YAML-Frontmatter aus Markdown-Inhalt.

    Args:
        content: Der Markdown-Inhalt

    Returns:
        Ein Tupel mit dem geparsten Frontmatter (oder None) und dem Inhalt ohne Frontmatter
    """
    frontmatter = None
    remaining_content = content

    # Prüfe auf YAML-Frontmatter (zwischen --- Markern)
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if frontmatter_match:
        try:
            frontmatter_text = frontmatter_match.group(1)
            frontmatter = yaml.safe_load(frontmatter_text)
            remaining_content = content[frontmatter_match.end():]
        except yaml.YAMLError:
            # Bei YAML-Parsing-Fehlern ohne Frontmatter fortfahren
            pass

    return frontmatter, remaining_content

def get_file_date(file_path: str) -> datetime.datetime:
    """
    Ermittelt das Datum einer Datei, versucht zuerst das Frontmatter,
    fällt dann auf das Änderungsdatum zurück.

    Args:
        file_path: Pfad zur Datei

    Returns:
        Ein datetime-Objekt, das das Datum der Datei repräsentiert
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            frontmatter, _ = extract_frontmatter(content)

            if frontmatter:
                # Versuche verschiedene gängige Datumsfeld-Namen in Obsidian
                for date_field in ['date', 'created', 'creation_date', 'created_at']:
                    if date_field in frontmatter and frontmatter[date_field]:
                        try:
                            # Versuche das Datumsfeld zu parsen
                            if isinstance(frontmatter[date_field], datetime.date):
                                return datetime.datetime.combine(
                                    frontmatter[date_field],
                                    datetime.datetime.min.time()
                                )
                            elif isinstance(frontmatter[date_field], str):
                                # Versuche gängige Datumsformate
                                for fmt in [
                                    '%Y-%m-%d',
                                    '%Y/%m/%d',
                                    '%d.%m.%Y',
                                    '%Y-%m-%d %H:%M:%S',
                                    '%Y-%m-%dT%H:%M:%S'
                                ]:
                                    try:
                                        return datetime.datetime.strptime(
                                            frontmatter[date_field], fmt
                                        )
                                    except ValueError:
                                        continue
                        except (ValueError, TypeError):
                            # Bei Fehlern beim Datum-Parsing zum nächsten Feld gehen
                            pass
    except (UnicodeDecodeError, IOError):
        # Wenn die Datei nicht gelesen werden kann, auf Änderungsdatum zurückfallen
        pass

    # Rückfall auf Änderungsdatum
    timestamp = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(timestamp)