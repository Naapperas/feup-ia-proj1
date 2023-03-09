from typing import List, TypeVar

from files import parse_file

Model = TypeVar("Model")


def parse_model(file: str, model: Model) -> List[Model]:
    """
    Parses a CSV file and returns an array of the specified model
    """

    models = []

    for line in parse_file(file):
        models.append(model(*line.values()))

    return models
