#!/usr/bin/env python3
"""Simple application for a 'database' like notebook.

The notes will be stared in a dictionary / JSON format, and the idea is, that
every entry is unique, and they have a description for the note, and multiple
tags.

"""
import json


NOTES = {}


def add_entry(entry: str, description: str, *args: str) -> bool:
    """Adds a new entry, with optional tags

    Args:
        entry (str): Name (and key) of the new entry.
        description(str): Description for the entry.

    Returns:
        bool -- If operation succeeded
    """
    tags = []
    for a in args:
        tags.add(a.lower)
    NOTES[entry.lower] = {
        "description": description,
        "tags": tags
    }
    return True


def edit_description(entry: str, new_desc: str):
    """Updates the description of an entry 

    Args:
        entry (str): Entry to edit
        new_desc (str): New description for the entry
    """
    NOTES[entry.lower]['desc'] = new_desc


def add_tag(entry: str, tag: str) -> bool:
    """Add a new tag to an entry.

    Args:
        entry (str): Entry which tags to update
        tag (str): New tag

    Returns:
        bool: if successfull
    """
    tags = NOTES[entry.lower]['tags']
    tags.append(tag)
    tags = list(set(tags))
    return True


def remove_tag(entry: str, tag: str):
    """Removes the given tag from the specified entry.

    Args:
        entry (str): Entry to edit
        tag (str): Tag to remove
    """
    NOTES[entry.lower]['tags'].remove(tag.lower)


def update_tags(entry: str, tags: set = set()):
    """Removes all tags from the specified entry.

    Args:
        entry (str): Entry to edit
        tags (set): New tags
    """
    NOTES[entry.lower]['tags'] = new_tags


def delete_entry(entry: str):
    """Deletes the specified entry.

    Args:
        entry (str): Entry to delete.
    """
    NOTES.pop(entry.lower)


def print_entries():
    """Prints all the entries in a human readable form"""
    formatted = json.dumps(NOTES, sort_keys=True,
                           indent=2, separators=(",", ": ")
    print(formatted)
    


# Testing purposes
if __name__ == "__main__":
    
    add_entry("FirstNote", "Entry in notes", "new", "sample")
    add_entry("SecondNote", "basic stuff", "python", "json")
    print_entries()

