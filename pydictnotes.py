#!/usr/bin/env python3
"""Simple application for a 'database' like notebook.

The notes will be stared in a dictionary / JSON format, and the idea is, that
every entry is unique, and they have a description for the note, and multiple
tags.

TODO:
    - Make entries case insensitive
    - Replace argparse with Click
    - Write tests
    - Integrate to GUI or web
    - Access entries with numbers
"""
import argparse
import json
import sys

from collections import OrderedDict
from dictnoteconfig import *
from typing import Callable, List, OrderedDict, Dict

# PATH_TO_JSON = "./data/notes.json"
NOTES = OrderedDict()
KEYS_LIST = list(NOTES.keys())


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
        tags.append(a.lower())
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
    tags.append(tag.lower())
    NOTES[entry]["tags"] = list(set(tags))
    return True


def remove_tag(entry: str, tag: str):
    """Removes the given tag from the specified entry.

    Args:
        entry (str): Entry to edit
        tag (str): Tag to remove
    """
    NOTES[entry]["tags"].remove(tag.lower())


def update_tags(entry: str, tags: List[str] = []):
    """Removes all tags from the specified entry.

    Args:
        entry (str): Entry to edit
        tags (set): New tags
    """
    new_tags = map(lambda t: t.lower(), tags)
    NOTES[entry]["tags"] = list(set(new_tags))


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


def print_entries(items: OrderedDict[str, str]):
    """Prints all the entries in notes in human readable form."""
    key_id = 0
    for key, value in items.items():
        values = json.dumps(value,
                            sort_keys=True,
                            indent=2,
                            separators=("", ": "))
        print(f"[{key_id}] {key}:{values}")
        key_id += 1


def print_entry(entry_ind: int):
    """Print a single entry out.

    Arguments:
        items {OrderedDict} -- Dictionary to to search from
        entry_ind {int} -- Index of the entry in items.keys() as a list
    """
    target_entry = KEYS_LIST[entry_ind]
    values = json.dumps(NOTES[target_entry],
                        indent = 2,
                        separators=("", ": "))
    out = f"[{entry_ind}] {target_entry}: {values}"
    print(out)


def save_file(path: str):
    """Write entries data to JSON file

    Args:
        path (str): Path to JSON file

    """
    with open(path, "w") as out_file:
        json.dump(NOTES, out_file)


def save_file_pretty(path: str):
    """Writes all notes to a file, in human readable format
    
    Args:
        path (str): Path to JSON file
    
    """
    pretty_file = f"{path[:-5]}_pretty.json" 
    with open(pretty_file, "w") as out_file:
        out = json.dumps(NOTES,
                         sort_keys=True,
                         indent=2,
                         separators=(",", ": "))
        out_file.write(out)


def read_file(path: str) -> OrderedDict:
    """Reads data from a JSON file in given path.

    Args:
        path (str): Path to JSON file

    Returns:
        dict: Data from the JSON as a dictionary.
    """
    with open(path, "r") as f:
        data = json.load(f)
    return OrderedDict(data)


def cli_multivalue(func: Callable, *args: str):
    """Call functions that take multiple arguments.

    Args:
        func (Callable): Function to call with given values
        args (str): Va len of arguments
    """
    target_entry = KEYS_LIST[int(args[0])]
    for a in args[1:]:
        func(target_entry, a)
    save_file(PATH_TO_JSON)


def cli_singlevalue(func: Callable, *args: int):
    """Call functions with single target.

    Args:
        func (Callable): Function to call with given values
        args (str): Varying lenght of arguments
    """
    for a in args[1:]:
        target_entry = KEYS_LIST[a]
        func(target_entry)
    


# Main
if __name__ == "__main__":

    try:
        NOTES = read_file(PATH_TO_JSON)
    except json.JSONDecodeError as e:
        print(f"Error occured when trying to read the file: {e}")
    except IOError as e:
        print("File not found, writing a new one...")
        save_file(PATH_TO_JSON)

    parser = argparse.ArgumentParser(
        description="Add or manage JSON style notes", prog="dictnotes"
    )
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    parser.add_argument(
        "-a", "--add", nargs="+", type=str, dest="addentry", help="Add a new entry",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        dest="list",
        help="List entries as raw JSON",
    )
    parser.add_argument(
        "-rm", "--remove", nargs="+", type=int, dest="rmentry", help="Remove an entry",
    )
    parser.add_argument(
        "-t", "--tag", nargs="+", type=str, help="Add a new tag to an entry"
    )
    parser.add_argument(
        "-d",
        "--delete",
        nargs="+",
        type=str,
        dest="rmtag",
        help="Remove a tag from an entry",
    )
    parser.add_argument(
        "-e",
        "--edit",
        nargs="+",
        dest="descedit",
        help="Edit the description of an entry.",
    )

    args = parser.parse_args()



    if args.list:
        print_entries(NOTES)

    if args.addentry:
        cli_multivalue(add_entry, *args.addentry)

    if args.tag:
        cli_multivalue(add_tag, *args.tag)

    if args.descedit:
        cli_multivalue(edit_description, *args.descedit)

    if args.rmentry:
        cli_singlevalue(delete_entry, *args.rmentry)

    if args.rmtag:
        cli_multivalue(remove_tag, *args.rmtag)
