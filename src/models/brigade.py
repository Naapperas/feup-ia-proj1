"""
Classes and methods related to brigades
"""

from debug import Printable
from graph.graph import Graph
from models.route import Route


class Brigade(Printable):
    """
    An inspection brigade that is responsible for visiting establishments on a route
    """

    def __init__(self, route: Route):
        self.route = route

    def total_waiting_time(self, network: Graph) -> int:
        """
        Returns the total waiting time for this brigade
        across its route's establishments
        """

        return 0
