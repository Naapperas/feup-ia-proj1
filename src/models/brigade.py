"""
Classes and methods related to brigades
"""

from debug import Printable
from models.route import Route
from simulation.network import Network


class Brigade(Printable):
    """
    An inspection brigade that is responsible for visiting establishments on a route
    """

    def __init__(self, route: Route):
        self.route = route

    def total_waiting_time(self, network: Network) -> int:
        """
        Returns the total waiting time in seconds for this brigade
        across its route's establishments
        """

        graph = network.graph
        depot = network.depot

        total_waiting_time: int = 0

        START_TIME = 9 * 60 * 60  # assume inspection starts at 9ams
        previous_establishment = depot

        cur_time = START_TIME

        for establishment in self.route:
            time_to_arrive = graph.get(
                previous_establishment.establishment_id, establishment.establishment_id
            )
            cur_time += time_to_arrive  # simulate the brigade's trip

            # TODO: calculate waiting time according to the establishment's availability
            opening_hours = establishment.opening_hours
            cur_hour = (cur_time // 3600) % 24

            # use only opening hours in the future relative to us
            future_hours = opening_hours[cur_hour - 1 :]

            waiting_time = 0

            cur_time += waiting_time
            total_waiting_time += waiting_time

            cur_time += establishment.inspection_data.inspection_time * 60
            previous_establishment = establishment

        return total_waiting_time
