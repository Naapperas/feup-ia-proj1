"""
Logic related to parsing models out of text
"""

from typing import Callable, Type, TypeVar, Any
from files import parse_file


class Parsable:  # pylint:`` disable=too-few-public-methods
    """
    Defines that a class can be parsed from a dict containing its relevant data
    """

    @staticmethod
    def parse(data: dict[str, Any]):
        """
        Returns a model parsed from the given data dict
        """


Model = TypeVar("Model", bound=Parsable)

FT_co = TypeVar("FT_co", bound=Type, covariant=True)


def get_named_field(
    data: dict[str, Any], field_name: str, field_type: Callable[[Any], FT_co]
) -> FT_co:
    """
    Gets a field from the given data dict using the given name,
    optionally converting it to the given type
    """
    if (field := data.get(field_name, None)) is None:
        raise KeyError(f"{field_name} is required")

    return field_type(field)


def parse_model(file: str, model: Model) -> list[Model]:
    """
    Parses a CSV file and returns an array of the specified model
    """

    models: list[Model] = []

    for line in parse_file(file):
        model_data = dict(line.items())  # this is ugly but at least we get types

        models.append(model.parse(model_data))
    return models
