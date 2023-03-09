"""
Logic related to parsing a text file
"""

from typing import Dict, Any, Generator

import csv


def parse_file(file_path: str) -> Generator[Dict[str, Any], None, None]:
    """
    Parses a CSV file and returns a list of the data contained in it
    """

    with open(file_path, mode="r", encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=",")

        for line in reader:
            yield line
