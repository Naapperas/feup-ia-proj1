from typing import List, Dict, Any, Generator, TypeVar

import csv

def parse_file(file: str) -> Generator[List[Dict[str, Any]], None, None]:
    """
        Parses a CSV file and returns a list of the data contained in it
    """

    with open(file, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')

        for line in reader:
            yield line

Model = TypeVar('Model')
def parse_model(file: str, model: Model) -> List[Model]:
    """
        Parses a CSV file and returns an array of the specified model
    """

    models = []

    for line in parse_file(file):
        models.append(model(*line.values()))

    return models
