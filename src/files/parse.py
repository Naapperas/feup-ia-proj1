"""
Logic related to parsing a text file
"""

import math
from typing import Dict, Any, Generator

import csv


def parse_file(
    file_path: str, max_lines_read: int = -1
) -> Generator[Dict[str, Any], None, None]:
    """
    Parses a CSV file and returns a list of the data contained in it.

    Can optionally specify the amount of lines to read from the file:
    a negative value indicates that all lines should be read.
    """

    # no need to open the file, saves expensive IO operations
    if max_lines_read == 0:
        return

    limit: float = math.inf if max_lines_read < 0 else float(max_lines_read)
    counter: int = 1

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=",")

        for line in reader:
            if counter > limit:
                break

            yield line

            counter += 1
