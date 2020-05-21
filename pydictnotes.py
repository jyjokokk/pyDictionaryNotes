#!/usr/bin/env python3
"""Simple application for a 'database' like notebook.

The notes will be stared in a dictionary / JSON format, and the idea is, that
every entry is unique, and they have a description for the note, and multiple
tags.

"""
import json


PATH_TO_DATA = "./data/notes.json"
NOTES = {}

with open(PATH_TO_DATA, 'r') as in_file:
    data = in_file.read()
    NOTES = json.loads(data)


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
        tags.append(a)
    NOTES[entry] = {"description": description, "tags": tags}
    return True


def edit_description(entry: str, new_desc: str):
    """Updates the description of an entry 

    Args:
        entry (str): Entry to edit
        new_desc (str): New description for the entry
    """
    NOTES[entry]["desc"] = new_desc


def add_tag(entry: str, tag: str) -> bool:
    """Add a new tag to an entry.

    Args:
        entry (str): Entry which tags to update
        tag (str): New tag

    Returns:
        bool: if successfull
    """
    tags = NOTES[entry]["tags"]
    tags.append(tag)
    NOTES[entry]["tags"] = list(set(tags))
    return True


def remove_tag(entry: str, tag: str):
    """Removes the given tag from the specified entry.

    Args:
        entry (str): Entry to edit
        tag (str): Tag to remove
    """
    NOTES[entry]["tags"].remove(tag)


def update_tags(entry: str, tags: list = []):
    """Removes all tags from the specified entry.

    Args:
        entry (str): Entry to edit
        tags (set): New tags
    """
    NOTES[entry]["tags"] = tags


def delete_entry(entry: str):
    """Deletes the specified entry.

    Args:
        entry (str): Entry to delete.
    """
    NOTES.pop(entry)


def print_entries_raw():
    """Prints all the entries in raw JSON form."""
    out = json.dumps(NOTES, sort_keys=True, indent=2, separators=(",", ": "))
    print(out)


def print_entries(item: dict):
    """Prints all the entries in notes in human readable form.""" 
    for note in NOTES:
        if type(note) is dict:
            print_entries(note)
        out = json.dumps(note,
                         sort_keys=True,
                         indent=2,
                         separators=(",", ": "))
        print(out)


def save_file():
    """Writes all notes to a file"""
    with open(PATH_TO_DATA, 'w') as out_file:
        json.dump(NOTES, out_file)


def save_file_pretty():
    """Writes all notes to a file, in human readable format"""
    with open('data/notes_pretty.json', 'w') as out_file:
        out = json.dumps(NOTES, sort_keys=True, indent=2, separators=(",", ": "))
        out_file.write(out)



# Testing purposes
if __name__ == "__main__":

    # add_entry("FirstNote", "Entry in notes", "new", "sample")
    # add_entry("SecondNote", "basic stuff", "python", "json")
    add_entry("Third Note", "Third note in file", "pretty", "print", "format")
    # delete_entry('Third Note')
    save_file()
    save_file_pretty()
    print_entries_raw()
    # print_entries_raw()
    # print("========================")
    # add_tag('FirstNote', "pyflakes")
    # remove_tag('SecondNote', 'json')
    # edit_description('SecondNote', "New description!")
    # print_entries_raw()
    # print("========================")
    # update_tags('FirstNote')
    # delete_entry('SecondNote')
    # print_entries_raw()
