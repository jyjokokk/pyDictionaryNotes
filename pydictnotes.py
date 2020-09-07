#!/usr/bin/env python3
"""Simple application for a 'database' like notebook.

The notes will be stared in a dictionary / JSON format, and the idea is, that
every entry is unique, and they have a description for the note, and multiple
tags.

Todo:
    * Better printing
    * Clean up argparse to it's own function, and call it from main()
    * Description adding on input
    * Add error handling to functions (try / catch)
    * Make entries case insensitive
    * Access entries by index / id
    * Write a better config file
    * Write tests
    * (Replace argparse with Click?)

"""
import argparse
import json
import sys

# will be changed to attribute instead of import
from dictnoteconfig import PATH_TO_JSON


NOTES: dict = {}  # Holds all the notes once read from disk


def add_entry(entry: str, description: str, *args: str) -> bool:
    """Adds a new entry, with optional tags

    Args:
        entry (str): Name (and key) of the new entry.
        description(str): Description for the entry.

    Returns:
        True for success, False for failure

    Todo:
        * Switch from bool returns to try / catch for error handling
    """
    try:
        tags = []
        for a in args:
            tags.append(a.lower())
        tags.sort()
        NOTES[entry] = {"description": description, "tags": tags}
        return True
    except NameError:
        print("Notes object not found.")
    except Exception as e:
        print(e)
        return False


def edit_description(entry: str, new_desc: str) -> None:
    """Updates the description of an entry

    Args:
        entry (str): Entry to edit
        new_desc (str): New description for the entry
    """
    NOTES[entry]["description"] = new_desc


def add_tag(entry: str, tag: str) -> bool:
    """Add a new tag to an entry.

    Args:
        entry (str): Entry which tags to update
        tag (str): New tag

    Returns:
        True if operation succesfull, False if not.

    Todo:
        * Why does this return a boolean, is it even needed?
    """
    tags = NOTES[entry]["tags"]
    tags.append(tag.lower())
    NOTES[entry]["tags"] = list(set(tags))
    return True


def remove_tag(entry: str, tag: str) -> None:
    """Removes the given tag from the specified entry.

    Args:
        entry (str): Entry to edit
        tag (str): Tag to remove
    """
    NOTES[entry]["tags"].remove(tag.lower())


def update_tags(entry: str, tags: list = []) -> None:
    """Removes all tags from the specified entry.

    Args:
        entry (str): Entry to edit
        tags (set): New tags
    """
    new_tags = map(lambda t: t.lower(), tags)
    NOTES[entry]["tags"] = list(set(new_tags))
    print(f"Tags for {entry} updated to: {NOTES[entry]['tags']}")


def delete_entries(entries: list) -> bool:
    """Delete the given entries.

    Args:
        entry: List of entries to delete.

    Returns:
        Was the process completed or not.
    """
    if len(entries) > 1:
        question = f"Are you sure you want to delete {len(entries)} entries?"
        if not confirm(question):
            return False
    for e in entries:
        NOTES.pop(e)
    return True


def delete_all_entries() -> bool:
    """Delete all entries from the dictionary and overwrite the save file.

    Prompts the user to confirm the action, with default option being 'No'.

    Returns:
        True if process was completed, False if not.

    """
    question = "Are you sure you want to permanently delete all entries?"
    if not confirm(question, "no"):  # if answer is 'no'
        return False
    NOTES.clear()
    save_file()
    return True


def print_entries_json() -> None:
    """Prints all the entries in human readable JSON form."""
    out = json.dumps(
        NOTES, sort_keys=True, indent=2, separators=(",", ": ")
    )
    print(out)


def print_entries() -> None:
    """Prints all the note entries in human readable form.

    Formats the entries in a table like manner, with the 'Name' of the entry
    on the left, tags on the middle, and description on the right.

    Todo:
        * Add description to printing
        * See for better formatting

    """
    if len(NOTES) == 0:
        print("No entries found!")
        print("Use 'dictnote --help' to list available commands.")
        return None
    print(f"{'Note':^20} {'Tags':^20}")
    print(f"{'----':^20} {'----':^20}")
    for key, value in NOTES.items():
        print(f"{key:^20}|   {str(sorted(value['tags']))}")


def save_file() -> None:
    """Writes all notes to a file"""
    with open(PATH_TO_JSON, "w") as out_file:
        json.dump(NOTES, out_file)


def save_file_pretty() -> None:
    """Writes all notes to a file, in human readable format"""
    with open(PATH_TO_JSON + "_hr", "w") as out_file:
        out = json.dumps(
            NOTES, sort_keys=True, indent=2, separators=(",", ": ")
        )
        out_file.write(out)


def confirm(question: str, default: str = "yes") -> bool:
    """Ask confirmation to a yes/no question and return the result as boolean.

    Args:
        question: Question to ask and print for user
        default: The default answer (used if answer input is left empty)

    Returns: True if yes, False if no or the input was incorrect

    """
    valid = {"yes": True, "ye": True, "y": True,
             "no": False, "n": False}
    if default is None:
        prompt = "[y/n]"
    elif default == "yes":
        prompt = "[Y/n]"
    else:
        prompt = "[y/N]"
    while True:
        print(f"{question} {prompt}")
        answer = input(">").lower()
        if default is not None and answer == '':
            return valid[default]
        elif answer in valid:
            return valid[answer]
        else:
            return False


def main() -> None:
    """Function to execute when ran from the command line.

    Serves as a container function for functionality only needed when executed
    directly.
    """


# Main
if __name__ == "__main__":

    try:
        with open(PATH_TO_JSON, "r") as in_file:
            data = in_file.read()
            NOTES = json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error occured when trying to read the file: {e}")
    except IOError:
        print("File not found, writing a new one...")
        new_json = {}
        with open(PATH_TO_JSON, 'w') as out_file:
            json.dump(new_json, out_file)

    parser = argparse.ArgumentParser(
        prog="dictnote",
        usage="%(prog)s [options]",
        description="Add or manage JSON style notes",
        epilog="You can change options in the dictnoteconfig.py file. Happy notekeeping!"
    )
    if len(sys.argv) == 1:
        print_entries()

    parser.add_argument(
        "-a",
        "--add",
        nargs="+",
        metavar='ENTRY',
        help="Add a new entry",
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List entries as raw JSON",
    )
    parser.add_argument(
        "-rm",
        "--remove",
        nargs="+",
        metavar='ENTRY',
        help="Remove an entry",
    )
    parser.add_argument(
        "--remove-all",
        action="store_true",
        dest="rmall",
        help="Delete all entries in dictnote and overwrite the savefile",
    )
    parser.add_argument(
        "-t", "--tag", nargs="+", help="Add a new tag to an entry"
    )
    parser.add_argument(
        "-d",
        "--delete",
        nargs="+",
        metavar='TAG',
        help="Remove a tag from an entry"
    )
    parser.add_argument(
        "-e",
        "--edit",
        nargs="+",
        help="Edit the description of an entry."
    )

    args = parser.parse_args()

    if args.add:
        add_entry(
            args.add[0], "", args.add[1]
        )
        if len(args.add) > 2:
            for t in args.add[2:]:
                add_tag(args.add[0], t)
        save_file()

    if args.list:
        print_entries()

    if args.rmall:
        delete_all_entries()
        save_file()

    if args.tag:
        for t in args.tag[1:]:
            add_tag(args.tag[0], t)
        save_file()

    if args.edit:
        edit_description(args.edit[0], args.edit[1])

    if args.remove:
        delete_entries(args.remove)
        save_file()

    if args.delete:
        for t in args.delete[1:]:
            remove_tag(args.delete[0], t)
        save_file()

