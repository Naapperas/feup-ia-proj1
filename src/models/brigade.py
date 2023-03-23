"""
Classes and methods related to brigades
"""

from debug import Printable
from graph.graph import Graph
from models.establishment import Establishment
from models.route import Route


class Brigade(Printable):
    """
    An inspection brigade that is responsible for visiting establishments on a route
    """

    def __init__(self, route: Route):
        self.route = route

    def total_waiting_time(self, network: Graph, depot: Establishment) -> int:
        """
        Returns the total waiting time for this brigade
        across its route's establishments
        """

        total_waiting_time: int = 0

        # assume inspection starts at 9am
        start_time = (9, 0, 0)
        previous_establishment = self.route[0]

        # TODO: get time from depot to first establishment

        cur_time = (start_time[0], start_time[1], start_time[2])

        for establishment in self.route[1:]:
            pass

        return total_waiting_time
