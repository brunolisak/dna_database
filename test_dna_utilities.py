#
# Unit tests for "dna_utilities.py"
#

import pytest

from dna_utilities import (
    is_valid_sequence,
    overlap_prefix,
    overlap_suffix
)

#
# Test cases for the "is_valid_sequence" function.
#
def test_is_valid_sequence_when_none_sequence_then_false():
    sequence = None

    is_valid = is_valid_sequence(sequence)

    assert is_valid == False


def test_is_valid_sequence_when_invalid_type_then_false():
    sequence = 123

    is_valid = is_valid_sequence(sequence)

    assert is_valid == False


def test_is_valid_sequence_when_empty_sequence_then_false():
    sequence = ""

    is_valid = is_valid_sequence(sequence)

    assert is_valid == False

def test_is_valid_sequence_when_only_invalid_characters_then_false():
    sequence = "ZSWQFH1234"

    is_valid = is_valid_sequence(sequence)

    assert is_valid == False

def test_is_valid_sequence_when_valid_invalid_characters_then_false():
    sequence = "ZSAWQCFHTG"

    is_valid = is_valid_sequence(sequence)

    assert not is_valid

def test_is_valid_sequence_when_A_base_then_true():
    sequence = "A"  # test uppercase

    is_valid = is_valid_sequence(sequence)

    assert is_valid

def test_is_valid_sequence_when_C_base_then_true():
    sequence = "C"  # test uppercase

    is_valid = is_valid_sequence(sequence)

    assert is_valid

def test_is_valid_sequence_when_G_base_then_true():
    sequence = "G"  # test uppercase

    is_valid = is_valid_sequence(sequence)

    assert is_valid

def test_is_valid_sequence_when_T_base_then_true():
    sequence = "T"  # test uppercase

    is_valid = is_valid_sequence(sequence)

    assert is_valid

def test_is_valid_sequence_when_a_base_then_true():
    sequence = "a"  # test lowercase

    is_valid = is_valid_sequence(sequence)

    assert is_valid

def test_is_valid_sequence_when_c_base_then_true():
    sequence = "c"  # test lowercase

    is_valid = is_valid_sequence(sequence)

    assert is_valid

def test_is_valid_sequence_when_g_base_then_true():
    sequence = "g"  # test lowercase

    is_valid = is_valid_sequence(sequence)

    assert is_valid

def test_is_valid_sequence_when_t_base_then_true():
    sequence = "t"  # test lowercase

    is_valid = is_valid_sequence(sequence)

    assert is_valid


# Test cases for the "overlap_prefix" function.
# Note that each test uses the default "minimum_overlap" value of 2.
def test_overlap_prefix_given_null_sample_then_none():
    sample = None
    sequence = "ATCAAGA"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert not overlap_sequence

def test_overlap_prefix_given_null_sequence_then_none():
    sample = "AGA"
    sequence = None

    overlap_sequence = overlap_prefix(sample, sequence)
    assert not overlap_sequence

def test_overlap_prefix_given_too_short_sequence_then_none():
    sample = "AG"
    sequence = "A"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert not overlap_sequence

def test_overlap_prefix_given_too_short_sample_then_none():
    sample = "A"
    sequence = "AG"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert not overlap_sequence

def test_overlap_prefix_given_non_matching_sequence_then_none():
    sample = "AGA"
    sequence = "TCGCAT"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert not overlap_sequence

def test_overlap_prefix_given_matching_one_base_then_none():
    sample = "AGA"
    sequence = "ACGCAT"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert not overlap_sequence

def test_overlap_prefix_given_matching_two_bases_then_matching_prefix():
    sample = "AGA"
    sequence = "GAGGCAT"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert overlap_sequence == "GA"

def test_overlap_prefix_given_matching_complete_sample_then_matching_prefix():
    sample = "AGA"
    sequence = "AGAGGCAT"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert overlap_sequence == "AGA"

def test_overlap_prefix_given_matching_complete_sequence_then_matching_prefix():
    sample = "TCCAAGA"
    sequence = "GA"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert overlap_sequence == "GA"

def test_overlap_prefix_given_matching_sample_sequence_then_matching_prefix():
    sample = "TCCAAGA"
    sequence = "TCCAAGA"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert overlap_sequence == "TCCAAGA"

def test_overlap_prefix_given_long_matching_sequence_then_matching_prefix():
    overlap = "AGAGTAGG"
    sample = "TCCA" + overlap
    sequence = overlap + "TTAAGCGTATAC"

    overlap_sequence = overlap_prefix(sample, sequence)
    assert overlap_sequence == overlap

# Test cases for the "overlap_prefix" function.
# Note that each test uses the default "minimum_overlap" value of 2.
def test_overlap_suffix_given_null_sample_then_none():
    sample = None
    sequence = "ATCAAGA"

    overlap_sequence = overlap_suffix(sample, sequence)
    assert not overlap_sequence

def test_overlap_suffix_given_null_sequence_then_none():
    sample = "AGA"
    sequence = None

    overlap_sequence = overlap_suffix(sample, sequence)
    assert not overlap_sequence

def test_overlap_suffix_given_too_short_sequence_then_none():
    sample = "AG"
    sequence = "A"

    overlap_sequence = overlap_suffix(sample, sequence)
    assert not overlap_sequence

def test_overlap_suffix_given_too_short_sample_then_none():
    sample = "A"
    sequence = "AG"

    overlap_sequence = overlap_suffix(sample, sequence)
    assert not overlap_sequence

def test_overlap_suffix_given_non_matching_sequence_then_none():
    sample = "AGA"
    sequence = "TCGCAT"

    overlap_sequence = overlap_suffix(sample, sequence)
    assert not overlap_sequence

def test_overlap_suffix_given_matching_one_base_then_none():
    sample = "AGA"
    sequence = "ACGCATA"

    overlap_sequence = overlap_suffix(sample, sequence)
    assert not overlap_sequence

def test_overlap_suffix_given_matching_two_bases_then_matching_suffix():
    sample = "AGA"
    sequence = "GAGGCATAG"

    overlap_sequence = overlap_suffix(sample, sequence)
    assert overlap_sequence == "AG"


def test_overlap_suffix_given_matching_complete_sample_then_matching_suffix():
    sample = "AGA"
    sequence = "GGCATAGA"

    overlap_sequence = overlap_suffix(sample, sequence)
    assert overlap_sequence == "AGA"

def test_overlap_suffix_given_matching_complete_sequence_then_matching_suffix():
    sample = "TCCAAGA"
    sequence = "TC"

    overlap_sequence = overlap_suffix(sample, sequence)
    assert overlap_sequence == "TC"

def test_overlap_suffix_given_matching_sample_sequence_then_matching_suffix():
    sample = "TCCAAGA"
    sequence = "TCCAAGA"

    overlap_sequence = overlap_suffix(sample, sequence)
    assert overlap_sequence == "TCCAAGA"


def test_overlap_suffix_given_long_matching_sequence_then_matching_suffix():
    overlap = "AGAGTAGG"
    sample = overlap + "TCCA"
    sequence = "TTAAGCGTATAC" + overlap

    overlap_sequence = overlap_suffix(sample, sequence)
    assert overlap_sequence == overlap
