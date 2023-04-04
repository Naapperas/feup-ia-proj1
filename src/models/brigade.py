"""
Classes and methods related to brigades
"""

from typing import ClassVar

from debug import Printable

from .network import Network
from .route import Route


class Brigade(Printable):
    """
    An inspection brigade that is responsible for visiting establishments on a route
    """

    INSPECTION_START_TIME_SECONDS: ClassVar[int] = 9 * 60 * 60

    def __init__(self, route: Route):
        self.route = route
        self.utility: float = 0.0
        self.total_travel_time: float = 0

    def total_waiting_time(self, network: Network) -> float:
        """
        Returns the total waiting time in seconds for this brigade
        across its route's establishments
        """

        graph = network.graph
        depot = network.depot

        total_waiting_time: float = 0

        previous_establishment = depot
        cur_time: float = Brigade.INSPECTION_START_TIME_SECONDS

        # no need to iterate through the depot
        for establishment in self.route[1:]:
            time_to_arrive = graph.get(
                previous_establishment.establishment_id, establishment.establishment_id
            )
            cur_time += time_to_arrive  # simulate the brigade's trip

            opening_hours = establishment.opening_hours
            cur_hour = int(cur_time // 3600)

            # use only opening hours in the future
            # relative to us or that are the current one
            valid_opening_hours = (
                opening_hours[cur_hour % 24 :] + opening_hours[: cur_hour % 24]
            )

            next_open_hour = valid_opening_hours.index(1) + cur_hour

            waiting_time = (
                0
                if next_open_hour
                # should not fall in the "less than" range but just to be sure
                <= cur_hour
                else (next_open_hour * 60 * 60) - cur_time
            )

            cur_time += waiting_time
            total_waiting_time += waiting_time

            cur_time += establishment.inspection_data.inspection_time * 60
            self.utility += establishment.inspection_data.inspection_utility
            previous_establishment = establishment

        self.total_travel_time = cur_time - Brigade.INSPECTION_START_TIME_SECONDS

        return total_waiting_time
