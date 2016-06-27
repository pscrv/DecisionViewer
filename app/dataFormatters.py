"""
Module for formatting elements for models
"""

import re

def formatCaseNumber(input:str):
    """
    Attempts to parse input into the form "T nnnn/nn"
    and returns the result. Returns input unaltered, if 
    parsing fails
    """
    search = input.strip().upper()
    if search == "":
        return input

    finder = re.compile(r'(.*)([DGJRTW]) *(\d*)/(\d*)(.*)') #newlines are unlikely to matter
    found = re.search(finder, search)

    if found is None:
        return input

    prefix = found.group(1)
    suffix = found.group(5)
    if not (prefix == '' and suffix == ''):
        return input

    letter = found.group(2)
    first = found.group(3)
    second = found.group(4)

    return letter + " " + first.zfill(4) + "/" + second




