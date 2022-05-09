#
# Unit tests for "sequence_db.py"
#

import pytest

from sequence_db import (
    InsertResult,
    SequenceDb
)
from exceptions.invalid_sample_ex import InvalidSample
from exceptions.invalid_sequence_ex import InvalidSequence
from exceptions.invalid_sequence_id_ex import InvalidSequenceId

#
# Test cases for "insert"
#
def test_insert_when_invalid_sequence_then_exception():
    db = SequenceDb()
    sequence = "QWACATAGA"

    with pytest.raises(InvalidSequence) as e:
        db.insert(sequence)


def test_insert_when_new_sequence_then_persisted_and_id():
    db = SequenceDb()
    sequence = "ACATAGA"

    (result, sequence_id) = db.insert(sequence)

    assert len(db) == 1
    assert result == InsertResult.INSERTED
    assert sequence_id

def test_insert_when_2_new_sequences_then_persisted_and_unique_ids():
    db = SequenceDb()
    sequence1 = "ACATAGA"
    sequence2 = "AAGATTT"

    (result1, sequence_id1) = db.insert(sequence1)
    (result2, sequence_id2) = db.insert(sequence2)

    assert len(db) == 2
    assert result1 == InsertResult.INSERTED
    assert result2 == InsertResult.INSERTED
    assert sequence_id1 != sequence_id2
    
def test_insert_when_sequence_inserted_twice_then_persisted_first_time_and_same_id():
    db = SequenceDb()
    sequence = "ACATAGA"

    (result1, sequence_id1) = db.insert(sequence)
    (result2, sequence_id2) = db.insert(sequence)

    assert len(db) == 1
    assert result1 == InsertResult.INSERTED
    assert result2 == InsertResult.ALREADY_PRESENT
    assert sequence_id1 == sequence_id2

def test_inset_when_sequence_different_case_then_persisted_first_time_and_same_id():
    db = SequenceDb()
    sequence1 = "ac"
    sequence2 = "aC"

    (result1, sequence_id1) = db.insert(sequence1)
    (result2, sequence_id2) = db.insert(sequence2)

    assert len(db) == 1
    assert result1 == InsertResult.INSERTED
    assert result2 == InsertResult.ALREADY_PRESENT
    assert sequence_id1 == sequence_id2

#
# Test cases for "get"
#
def test_get_when_sequence_absent_then_exception():
    db = SequenceDb()
    sequence_id = "A-1"

    with pytest.raises(InvalidSequenceId) as e:
        db.get(sequence_id)


def test_get_one_sequence_unknown_id_then_exception():
    db = SequenceDb()
    sequence = "ACATAGA"
    unknown_id = "A-2"

    (result, sequence_id) = db.insert(sequence)

    with pytest.raises(InvalidSequenceId) as e:
        db.get(unknown_id)
   

def test_get_one_sequence_correct_id_then_return_sequence():
    db = SequenceDb()
    sequence = "ACATAGA"

    (result, sequence_id) = db.insert(sequence)
    got_sequence = db.get(sequence_id)

    assert got_sequence == sequence

#
# Test cases for "find"
#
def test_find_empty_database_then_empty_list():
    db = SequenceDb()
    sample = "ACT"

    sequence_ids = db.find(sample)

    assert len(sequence_ids) == 0


def test_find_invalid_sample_then_exception():
    db = SequenceDb()
    sequence = "ACATAGA"
    sample = None

    (result, sequence_id) = db.insert(sequence)

    with pytest.raises(InvalidSample) as e:
        db.find(sample)


def test_find_non_matching_sample_then_empty_list():
    db = SequenceDb()
    sequence = "ACATAGA"
    sample = "GCG"

    (result, sequence_id) = db.insert(sequence)
    sequence_ids = db.find(sample)

    assert len(sequence_ids) == 0


def test_find_one_matching_sample_then_one_result():
    db = SequenceDb()
    sequence = "ACATAGA"
    sample = "TAG"

    (result, sequence_id) = db.insert(sequence)
    sequence_ids = db.find(sample)

    assert len(sequence_ids) == 1
    assert sequence_ids[0] == sequence_id


def test_find_one_matching_one_not_matching_sample_then_one_result():
    db = SequenceDb()
    sequence1 = "AAAAAAA"
    sequence2 = "CCCCCCC"
    sample = "AA"

    (result1, sequence_id1) = db.insert(sequence1)
    (result2, sequence_id2) = db.insert(sequence2)
    sequence_ids = db.find(sample)

    assert len(sequence_ids) == 1
    assert sequence_id1 in sequence_ids


def test_find_two_matching_sample_then_two_results():
    db = SequenceDb()
    sequence1 = "AAAAAAA"
    sequence2 = "CCCAACC"
    sample = "AA"

    (result1, sequence_id1) = db.insert(sequence1)
    (result2, sequence_id2) = db.insert(sequence2)
    sequence_ids = db.find(sample)

    assert len(sequence_ids) == 2
    assert sequence_id1 in sequence_ids
    assert sequence_id2 in sequence_ids

def test_find_matching_sample_different_case_then_one_result():
    db = SequenceDb()
    sequence = "AAAAAAA"
    sample = "aa"

    (result, sequence_id) = db.insert(sequence)
    sequence_ids = db.find(sample)

    assert len(sequence_ids) == 1
    assert sequence_id in sequence_ids


#
# Test cases for "overlap"
# Note that each test uses the default "minimum_overlap" value of 2.
def test_overlap_given_invalid_sequence_id_then_exception():
    db = SequenceDb()
    sample = "AGA"
    sequence_id = "A-1"

    with pytest.raises(InvalidSequenceId) as e:
        db.overlap(sample, sequence_id)

def test_overlap_given_empty_sample_then_exception():
    db = SequenceDb()
    sample = None
    sequence = "ACATAGA"

    (result, sequence_id) = db.insert(sequence)

    with pytest.raises(InvalidSample) as e:
        db.overlap(sample, sequence_id)


def test_overlap_given_prefix_sample_then_True():
    db = SequenceDb()
    sample = "ACA"
    sequence = "ACATAGA"

    (result, sequence_id) = db.insert(sequence)
    is_overlap = db.overlap(sample, sequence_id)

    assert is_overlap

def test_overlap_given_suffix_sample_then_True():
    db = SequenceDb()
    sample = "AGA"
    sequence = "ACATAGA"

    (result, sequence_id) = db.insert(sequence)
    is_overlap = db.overlap(sample, sequence_id)

    assert is_overlap

def test_overlap_given_prefix_suffix_sample_then_True():
    db = SequenceDb()
    sample = "AGA"
    sequence = "AGATAGA"

    (result, sequence_id) = db.insert(sequence)
    is_overlap = db.overlap(sample, sequence_id)

    assert is_overlap

def test_overlap_given_prefix_sample_different_case_then_True():
    db = SequenceDb()
    sample = "agA"
    sequence = "AGATAGA"

    (result, sequence_id) = db.insert(sequence)
    is_overlap = db.overlap(sample, sequence_id)

    assert is_overlap
