# Exception to indicate an invalid DNA sample.
class InvalidSample(Exception):
    def __init__(self, sample):            
        self.sample = sample
    def __str__(self):
        return f"ERROR - Invalid sample: [{self.sample}]"
