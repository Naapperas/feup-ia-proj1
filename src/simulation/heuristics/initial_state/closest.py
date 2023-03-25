from models.establishment import Establishment
from ...graph import Graph

from .generator import Generator


class ClosestGenerator(Generator):
    """
    Generator that takes the closest establishment from the previous one
    """

    @staticmethod
    def next(
        establishments: dict[int, Establishment],
        previous: Establishment,
        graph: Graph,
    ) -> Establishment:
        """
        Generates a sample of establishments
        to be used in the applications initial state.

        The return value takes the form (<sample>, <rest>).

        The default implementation takes no sample and returns its parameter
        """

        closest, _ = min(
            (
                (i, d)
                for i, d in enumerate(graph.get_col(previous.establishment_id))
                if i in establishments
            ),
            key=lambda x: x[1],
        )

        return establishments[closest]
