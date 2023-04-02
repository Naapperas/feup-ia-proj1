"""
"Next closest" heuristic selection for the initial state
"""

from models.establishment import Establishment
from simulation.graph import Graph

from .generator import Generator


class ClosestGenerator(Generator):
    """
    Generator that returns the closest establishment from the previous one
    """

    def next(
        self,
        establishments: dict[int, Establishment],
        previous: Establishment,
        graph: Graph,
    ) -> Establishment:
        # FIXME: sometimes this breaks
        closest, _ = min(
            (
                (i, d)
                for i, d in enumerate(graph.get_col(previous.establishment_id))
                if i in establishments
            ),
            key=lambda x: x[1],
        )

        return establishments[closest]
