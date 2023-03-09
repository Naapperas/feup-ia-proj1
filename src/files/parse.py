from typing import List, Dict, Any, Generator

import csv


def parse_file(file: str) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Parses a CSV file and returns a list of the data contained in it
    """

    with open(file, "r") as file:
        reader = csv.DictReader(file, delimiter=",")

        for line in reader:
            yield line
