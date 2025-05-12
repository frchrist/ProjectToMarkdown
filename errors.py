"""module for error codes and messages"""
# -*- coding: utf-8 -*-
from enum import Enum

class ErrorCodes(Enum):
    """
    ErrorCodes(Enum):
        An enumeration representing various error codes and their descriptions.

        Attributes:
            E1010: Represents an error with code 1010, indicating an incorrect output format.
            E1012: Represents an error with code 1012, indicating that the program has shut down.
    """
    E1010 = "error code 1010 : INCORRECT OUTPUT FORMAT"
    E1012 = "error code 1012 : PROGRAM SHUT DOWN"
    NO_ERROR = "NO ERROR"


class FileProcessingException(Exception):
    """
      FileProcessingException
      When error accur during the file processing to Md file
    """
    def __init__(self, message):
        """
        Initializes the FileProcessingException with a custom error message.
        Args:
            message (str): The error message to be associated with the exception.
        """
        super().__init__(message)

    def __str__(self):
        return f"Md Error: {self.args[0]}"
