# DNA sequence database

The in-memory DNA sequence database.
This database will permit to insert DNA sequences, retrieve these sequences,
search for sequences containing a sample pattern and verify if a sample pattern
overlaps a particular sequence in the database.

## To get started:

    > python sequence_db_cli.py

This will display a simple interactive menu for accessing the database:

    DNA Sequence Database
    ---------------------
    I - Insert sequence
    G - Get sequence
    F - Find sequence
    O - Overlap sequence
    E - Exit
    >

## To execute the unit tests:

    > pytest
