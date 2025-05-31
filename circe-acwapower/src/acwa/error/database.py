"""
acwa.error.database

Contains class DatabaseError
"""

class DatabaseError(Exception):

    def __init__(
            self, action: str, original_error: str):
        """Init method

        Args:
            action (str): Description of action being executed
            original_error (str): Original error
        """

        self.message = f"Error running {action}: {original_error}"

    def __str__(self):
        return self.message
