# Exception to indicate an invalid DNA sequence.
class InvalidSequence(Exception):
    def __init__(self, sequence):            
        self.sequence = sequence
    def __str__(self):
        return f"ERROR - Invalid sequence: [{self.sequence}]"
