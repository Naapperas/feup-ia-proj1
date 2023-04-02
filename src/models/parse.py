"""
Logic related to parsing models out of text
"""

from typing import Any, Callable, Type, TypeVar

from files import parse_file


class Parsable:  # pylint: disable=too-few-public-methods
    """
    Defines that a class can be parsed from a dict containing its relevant data
    """

    @staticmethod
    def parse(data: dict[str, Any]) -> "Parsable":  # pylint: disable=unused-argument
        """
        Returns a model parsed from the given data dict
        """

        return Parsable()


FT_co = TypeVar("FT_co", bound=Type, covariant=True)
DicDT = TypeVar("DicDT")


def get_named_field(
    data: dict[str, DicDT], field_name: str, field_type: Callable[[DicDT], FT_co]
) -> FT_co:
    """
    Gets a field from the given data dict using the given name,
    optionally converting it to the given type
    """
    if (field := data.get(field_name, None)) is None:
        raise KeyError(f"{field_name} is required")

    return field_type(field)


Model = TypeVar("Model", bound=Parsable)


def parse_model(
    file: str, model: Type[Model], max_lines_parsed: int = -1
) -> list[Model]:
    """
    Parses a CSV file and returns an array of the specified model.

    Can optionally specify the amount of lines to parse from the file:
    a negative value indicates that all lines should be parsed.
    """

    models: list[Model] = []

    for line in parse_file(file, max_lines_parsed):
        model_data = dict(line.items())

        models.append(model.parse(model_data))
    return models
