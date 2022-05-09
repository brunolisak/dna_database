#
# In-memory DNA sequence database.
#
# Future enhancements:
# 1. Since a DNA sequence database can contain hundreds of thousands of sequences (and more), sharding can be introduced
# to improve its performance.
# For examlpe, there could be different shards based on the first base in the sequence (so 4 shards), and the sequence ID
# would start with the base itself to identify which shard it belongs to.
# The "insert", "get" and "overlap" methods would directly access a particular shard based on the sequence or the sequence ID.
# The "find" method would have to search through all shards and combine together the results. But since each shard has
# independent sequenceas, these "finds" can be performed concurrently and the results merged together when each "find worker"
# has completed their search. This sharding can easily be extended to any number of bases as the shard identifier,
# like having 16 shards based on a shard identifier of 2 bases ("AA", "AC", etc...).
# 
# 2. To permit concurrency, the sequence IDs could be UUIDs to ensure that no clashes will occur between different threads
# accessing the database.
#
# 3. The "overlap" method could return the found overlap sequence, and indicate if it corresponds to the prefix or the suffix
# (or both) of the sequence.

from enum import Enum

from dna_utilities import (
    DNA_BASES,
    is_valid_sequence,
    overlap_prefix,
    overlap_suffix
)

from exceptions.invalid_sample_ex import InvalidSample
from exceptions.invalid_sequence_ex import InvalidSequence
from exceptions.invalid_sequence_id_ex import InvalidSequenceId

# Indicates the insertion result. Only two possibilities for now (which could be replaced by True/False),
# but keeping the door open in case other situations are added.
class InsertResult(Enum):
    INSERTED = "Inserted"
    ALREADY_PRESENT = "Already present"


# The in-memory DNA sequence database.
# This database will permit to insert DNA sequences, retrieve these sequences,
# search for sequences containing a sample pattern and verify if a sample pattern
# overlaps a particular sequence in the database.
class SequenceDb:

    def __init__(self):
        # This could establish a connection to an actual database.
        # But for now, just create an empty dictionary that will acts as a database.
        # The sequences that are stored will be associated with an id.
        self.database = {}

        # For now, a simple integer will serve as an ID, but to be scalable 
        # to concurrent access, a UUID should be used.
        self.sequence_id = 0 
        

    # Get the next ID t be used for a sequence to be stored.
    def _get_next_id(self):
        self.sequence_id += 1
        return f"{self.sequence_id}"

    # Get the size of the sequence database.
    def __len__(self):
        return len(self.database)

    # Search the database for the presence of an exact sequence.
    #
    # Params:
    # - sequence: the sequence to search for
    # Returns the sequence ID if found, None otherwise
    def _is_present(self, sequence):
        for id in self.database.keys():
            if self.database[id] == sequence:
                return id
        return None

    # Insert a sequence into the database.
    # A sequence will be inserted if it is valid and not already present in the database.
    # A tuple is returned indicating the insertion result (<InsertResult>, <sequence_id>):
    # Params:
    # - sequence: the sequence to insert
    # Returns:
    # - (INSERTED, sequence_id) if the sequence is new, or 
    # - (ALREADY_PRESENT, sequence_id) if the sequence was already present.
    # Raises:
    # - InvalidSequence if the sequence is not a valid DNA sequence
    def insert(self, sequence):
        if not is_valid_sequence(sequence):
            raise InvalidSequence(sequence)
        else:
            # Is the sequence already in the database?
            upper_sequence = sequence.upper()
            present_id = self._is_present(upper_sequence)
            if present_id:
                return (InsertResult.ALREADY_PRESENT, present_id)

            # Sequence not already there, insert it.
            sequence_id = self._get_next_id()
            self.database[sequence_id] = upper_sequence
            return (InsertResult.INSERTED, sequence_id)


    # Get the sequence associated with a sequence ID.
    #
    # Params:
    # - sequence_id: the ID of the sequence to retrieve
    # Returns the DNA sequence associated with the sequence ID.
    # Raises:
    # - InvalidSequenceId if the sequence ID is not found in the database.
    def get(self, sequence_id):
        if sequence_id in self.database:
            return self.database[sequence_id]

        raise InvalidSequenceId(sequence_id)


    # Find all sequences in the database that contains a sampel sequence.
    # Params:
    # - sample: the sampel DNA sequence to match
    # Returns a list of sequence IDs for all matching sequences in the database.
    # Raises:
    # - InvalidSample if the sample sequence is not a valid DNA sequence.
    def find(self, sample):
        if not is_valid_sequence(sample):
            raise InvalidSample(sample)
        upper_sample = sample.upper()
        return [id for (id, seq) in self.database.items() if upper_sample in seq]
        # Since matches can be found in all shards,
        # We can simulate a parallel search across these shards, and
        # combine the results when each "worker" provides its results


    # Validate if a sample sequence overlaps a sequence in the database.
    # The sample overlap could be with the sequence's prefix or its suffix (or both).
    # Params:
    # - sample: the sample sequence to validate the overlap
    # - sequence_id: the sequence ID in the database
    # - minimum_overlap: - the minimum lenght of an accepted overlap sequence
    # Returns True is the sample overlaps the sequence prefix or suffix (or both), False otherwise.
    def overlap(self, sample, sequence_id, minimum_overlap=2):
        if not is_valid_sequence(sample):
            raise InvalidSample(sample)
        else:
            upper_sample = sample.upper()
            sequence = self.get(sequence_id)
            prefix_overlap = overlap_prefix(upper_sample, sequence)
            suffix_overlap = overlap_suffix(upper_sample, sequence)
            # Future enhancement: could return the obtained prefix/suffix overlap sequences instead of just True/False.
            return prefix_overlap is not None or suffix_overlap is not None
