#!/usr/bin/env python3
"""Simple application for a 'database' like notebook.

The notes will be stared in a dictionary / JSON format, and the idea is, that
every entry is unique, and they have a description for the note, and multiple
tags.

"""
import json


NOTES = {}


def add_entry(entry: str, *args: str) -> bool:
    """Adds a new entry, with optional tags

    Args:
        entry (str): Name (and key) of the new entry.
    
    Returns:
        bool -- If operation succeeded
    """
    if len(args) < 1:
        NOTES[entry] = {}
        return True
    NOTES[entry] = set(args)
    return True
