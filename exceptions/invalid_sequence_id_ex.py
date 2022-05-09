# Exception to indicate an invalid DNA sequence ID.
class InvalidSequenceId(Exception):
    def __init__(self, sequence_id):            
        self.sequence_id = sequence_id
    def __str__(self):
        return f"ERROR - Invalid sequence id: [{self.sequence_id}]"
