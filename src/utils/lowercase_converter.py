"""A module housing the method to abstractly convert strings to lowercase"""

def convert_to_lowercase(string: str) -> str:
    """Convert a string to lowercase. If used for non-strings, will return an unmodified object"""

    if isinstance(string, str):
        return string.lower()
    return string
