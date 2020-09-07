# DictioNotes

Simple command line (for now) application to take small notes, and add Tags and Descriptions to them. Is and most likely will be written mostly in Python.

Plan is to keep the application relatively simple, with the data stored in a simple
JSON file and format at first. Future plans (might) feature either a Web hosted
user interface and/or a browser extension, at which point a document oriented database
might be a good upgrade. Unless I want to sharpen up my relational database skills.

## TODO

- [ ] Tests
- [ ] Access entries by index
    - Idea: Change the 'outermost' layer of the database to a list, instead of a dict
- [ ] Error handling
- [ ] Clean up argparse
- [ ] Better printing

## Future ideas

- Web interface
    - Access backend by API
    - Option to host either from cloud, or locally
- Browser extension
    - No need for a hosting site
    - Quick integration for taking notes directly from Websites DOM
- Proper database
    - mongoDB would be a very easy transistion, and very easily deployable
