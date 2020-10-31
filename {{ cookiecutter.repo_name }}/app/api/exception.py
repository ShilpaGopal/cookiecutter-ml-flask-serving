class NoPredictionException(Exception):
    """Raised when no prediction returned from model"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'No prediction from model'


class InputFormatException(Exception):
    """Raised when input image is not readable by open CV
       CV return None if input image is with unexpected format or wrong input path"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Expected input format is numpy.ndarray, input {} is with {} format'.format(self.value, type(self.value))
