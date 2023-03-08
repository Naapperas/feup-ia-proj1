from typing import List, TypeVar

import csv

Model = TypeVar('Model')
def parse_model(file: str, model: Model) -> List[Model]:
    """
        Parses a CSV file and returns an array of the specified model
    """

    models = []

    with open(file, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')

        for line in reader:
            models.append(model(*line.values()))

    return models
