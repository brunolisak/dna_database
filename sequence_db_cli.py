#
# Simple command line interface for the Sequence Database
# Just execute this script to get things going!
#
from sequence_db import (
    SequenceDb,
)
from exceptions.invalid_sample_ex import InvalidSample
from exceptions.invalid_sequence_ex import InvalidSequence
from exceptions.invalid_sequence_id_ex import InvalidSequenceId

MINIMUM_OVERLAP_SIZE = 2

# Instantiate the application's sequence database.
database = SequenceDb()

# Insert a DNA sequence and persists it to the database.
# Prompts for a DNA sequence.
def insert_sequence():
    print("\nInsert Sequence: ", end="")
    user_sequence = input()
    try:
        (result, sequence_id) = database.insert(user_sequence)
        print(f"Insert result:[{result.value}] Sequence:[{user_sequence}] ID:[{sequence_id}]")
    except InvalidSequence as e:
        print(e)
    return True


# Gets a sequence from the database using the unique sequence identifier.
# Prompts for the sequence ID.
def get_sequence():
    print("Get Sequence from ID: ", end="")
    sequence_id = input()
    try:
        sequence = database.get(sequence_id)
        print(f"Get result:[{sequence}] for ID:[{sequence_id}]")
    except InvalidSequenceId as e:
        print(e)
    return True


# Finds all sequences containing the sample sequence.
# Prompts for the sample DNA sequence.
def find_sequence():
    print("Find sequence from sample: ", end="")
    sample = input()
    try:
        sequence_ids = database.find(sample)
        print(f"Find result: {sequence_ids} from Sample:[{sample}]")
    except InvalidSample as e:
        print(e)
    return True


# Validate if a sample sequence overlaps a DNA sequence.
# Prompts for he sample sequence and the sequence ID.
def overlap_sequence():
    print("Overlap sample: ", end="")
    sample = input()
    print("Overlap sequence id: ", end="")
    sequence_id = input()
    try:
        is_overlap = database.overlap(sample, sequence_id, MINIMUM_OVERLAP_SIZE)
        print(f"Overlap result:[{is_overlap}] for Sample:[{sample}] and ID:[{sequence_id}]")
    except InvalidSample as ise:
        print(ise)
    except InvalidSequenceId as iside:
        print(iside)
    return True


# Exit the CLI.
def exit_application():
    print("Exiting...To the next!")
    return False


# The accepted commands and the functions to execute.
commands = {
    "I": insert_sequence,
    "G": get_sequence,
    "F": find_sequence,
    "O": overlap_sequence,
    "E": exit_application
}


def display_menu():
    print("\nDNA Sequence Database")
    print("---------------------")
    print("I - Insert sequence")
    print("G - Get sequence")
    print("F - Find sequence")
    print("O - Overlap sequence")
    print("E - Exit")
    print("> ", end="")

keep_on_going = True

while keep_on_going:
    display_menu()
    choice = input()
    upper_choice = choice.upper()

    if len(upper_choice) == 1 and upper_choice in commands:
        keep_on_going = commands[upper_choice]()
    else:
        print(f"ERROR - Invalid choice: [{choice}]")
