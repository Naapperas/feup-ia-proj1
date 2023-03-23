"""
Initial State Generator
"""

from models.establishment import Establishment


class Generator:
    """
    Generator class that has a method **generate**
    that takes a list of establishments and the desired number of carriers
    and generates a sample from the same list to be used
    in the initial state of the simulation
    """

    @staticmethod
    def generate(
        establishments: list[Establishment], num_carriers: int
    ) -> tuple[list[Establishment], list[Establishment]]:
        """
        Generates a sample of establishments
        to be used in the applications initial state.

        The return value takes the form (<sample>, <rest>).

        The default implementation takes no sample and returns its parameter
        """

        return ([], establishments)
