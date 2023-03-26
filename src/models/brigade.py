"""
Classes and methods related to brigades
"""

from typing import ClassVar
from debug import Printable
from models.route import Route
from models.network import Network


class Brigade(Printable):
    """
    An inspection brigade that is responsible for visiting establishments on a route
    """

    INSPECTION_START_TIME_SECONDS: ClassVar[int] = 9 * 60 * 60

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

        previous_establishment = depot
        cur_time: float = Brigade.INSPECTION_START_TIME_SECONDS

        # no need to iterate through the depot
        for establishment in self.route[1:]:
            time_to_arrive = graph.get(
                previous_establishment.establishment_id, establishment.establishment_id
            )
            cur_time += time_to_arrive  # simulate the brigade's trip

            opening_hours = establishment.opening_hours
            cur_hour = int(cur_time // 3600) % 24

            # use only opening hours in the future relative to us
            future_hours = opening_hours[cur_hour:]

            try:
                next_open_hour = future_hours.index(1) + cur_hour
            except ValueError:
                # if we reach this point,
                # most likely this establishment is closed for the rest of the day
                # return large value so the enclosing state is deemed bad

                return 999999999

            waiting_time = (next_open_hour - cur_hour) * 60 * 60

            cur_time += waiting_time
            total_waiting_time += waiting_time

            cur_time += establishment.inspection_data.inspection_time * 60
            previous_establishment = establishment

        return total_waiting_time
