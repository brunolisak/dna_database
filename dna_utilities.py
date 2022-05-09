#
# Utility functions for managing DNA sequences.
#

# The DNA bases
DNA_BASES = "ACGT"

# Determine if a sequence is valid.
# A valid sequence is a string that contains at least one character and only consists of 
# characters among "DNA_BASES".
#
# Params:
# - sequence: the DNA sequence to validate
# Returns rue if the sequence is valid, False otherwise
def is_valid_sequence(sequence):
    if not sequence or not isinstance(sequence, str):
        return False

    return all(c in DNA_BASES for c in sequence.upper())


# Determine if a suffix of the sample (or the whole sample) overlaps 
# the prefix of the provided sequence (or the whole sequence).
# This overlap must be at least "minimum_overlap" bases long.
#
# Params:
# - sample: the sample to test against the sequence
# - sequence: the DNA sequence
# - minimum_overlap: - the minimum lenght of an accepted overlap sequence
# Returns the overlap sequence if found, None otherwise.
def overlap_prefix(sample, sequence, minimum_overlap=2):
    if not sample or not sequence:
        return None

    prefix_end = minimum_overlap

    while prefix_end <= len(sample) and prefix_end <= len(sequence):
        sequence_prefix = sequence[:prefix_end]
        if sample.endswith(sequence_prefix):
            return sequence_prefix
        prefix_end += 1

    return None


# Determine if a prefix of the sample (or the whole sample) overlaps 
# the suffix of the provided sequence (or the whole sequence).
# This overlap must be at least "minimum_overlap" bases long.
# Params:
# - sample: the sample to test against the sequence
# - sequence: the DNA sequence
# - minimum_overlap: - the minimum lenght of an accepted overlap sequence
# Returns the overlap sequence if found, None otherwise.
def overlap_suffix(sample, sequence, minimum_overlap=2):
    if not sample or not sequence:
        return None

    prefix_end = minimum_overlap

    while prefix_end <= len(sample) and prefix_end <= len(sequence):
        sequence_prefix = sequence[-prefix_end:]
        if sample.startswith(sequence_prefix):
            return sequence_prefix
        prefix_end += 1

    return None
