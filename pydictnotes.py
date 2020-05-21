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
"""
import argparse
import json
import sys


PATH_TO_DATA = "./data/notes.json"
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


def update_tags(entry: str, tags: list = []):
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


def print_entries(item: dict):
    """Prints all the entries in notes in human readable form."""
    for note in NOTES:
        if type(note) is dict:
            print_entries(note)
        out = json.dumps(
            note, sort_keys=True, indent=2, separators=(",", ": ")
        )
        print(out)


def save_file():
    """Writes all notes to a file"""
    with open(PATH_TO_DATA, "w") as out_file:
        json.dump(NOTES, out_file)


def save_file_pretty():
    """Writes all notes to a file, in human readable format"""
    with open("data/notes_pretty.json", "w") as out_file:
        out = json.dumps(
            NOTES, sort_keys=True, indent=2, separators=(",", ": ")
        )
        out_file.write(out)


def main():
    """Function to execute when ran from the command line.

    Serves as a container function for functionality only needed when executed
    directly.
    """
    parser = argparse.ArgumentParser(
        description="Add or manage JSON style notes", prog="dictnotes"
    )
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    parser.add_argument(
        "-a",
        "--add",
        nargs="+",
        type=str,
        dest="addentry",
        help="Add a new entry",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        dest="list",
        help="List entries as raw JSON",
    )
    parser.add_argument(
        "-rm",
        "--remove",
        nargs="+",
        type=str,
        dest="rmentry",
        help="Remove an entry",
    )
    parser.add_argument(
        "-t", "--tag", nargs="+", type=str, help="Add a new tag to an entry"
    )
    parser.add_argument(
        "-d",
        "--delete",
        nargs="n",
        type=str,
        dest="rmtag",
        help="Remove a tag from an entry",
    )
    parser.add_argument(
        "-e",
        "--edit",
        nargs="n",
        dest="descedit",
        help="Edit the description of an entry."
    )

    args = parser.parse_args()

    if args.list:
        print_entries_raw()

    if args.addentry:
        add_entry(
            args.addentry[0], "placeholder description", args.addentry[1]
        )
        if len(args.addentry) > 2:
            for t in args.addentry[2:]:
                add_tag(args.addentry[0], t)
        save_file()

    if args.tag:
        for t in args.tag[1:]:
            add_tag(args.tag[0], t)
        save_file()
    
    if args.descedit:
        edit_description(args.descedit[0], args.descedit[1])

    if args.rmentry:
        for r in args.rmentry:
            delete_entry(args.rmentry[0])
        save_file()

    if args.rmtag:
        for t in args.rmtag[1:]:
            remove_tag(args.rmtag[0], t)
        save_file()


# Main
if __name__ == "__main__":

    try:
        with open(PATH_TO_DATA, "r") as in_file:
            data = in_file.read()
            NOTES = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error occured when trying to read the file: {e}")
    except IOError as e:
        print("File not found, writing a new one...")
        new_json = {}
        with open(PATH_TO_DATA, 'w') as out_file:
            json.dump(new_json, out_file)
            

    with open(PATH_TO_DATA, "r") as in_file:
        data = in_file.read()
        NOTES = json.loads(data)
    
    main()

    # add_entry("FirstNote", "Entry in notes", "new", "sample")
    # add_entry("SecondNote", "basic stuff", "python", "json")
    # add_entry("Third Note", "Third note in file", "pretty", "print", "format")
    # delete_entry('Third Note')
    # save_file()
    # save_file_pretty()
    # print_entries_raw()
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
