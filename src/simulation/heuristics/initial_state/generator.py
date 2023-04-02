"""
Initial State Generator
"""

from models.establishment import Establishment
from simulation.graph import Graph


class Generator:  # pylint: disable=too-few-public-methods
    """
    Generator class that has a method **generate**
    that takes a list of establishments and the desired number of carriers
    and generates a sample from the same list to be used
    in the initial state of the simulation
    """

    def next(
        self,
        establishments: dict[int, Establishment],
        previous: Establishment,  # pylint: disable=unused-argument
        graph: Graph,  # pylint: disable=unused-argument
    ) -> Establishment:
        """
        Returns an establishment to be used in the applications initial state.

        The default implementation returns
        the last establishment added to the argument dictionary
        """

        return establishments.popitem()[1]
