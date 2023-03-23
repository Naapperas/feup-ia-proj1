"""
Classes and methods related to routes
"""

from typing import Iterable, Iterator
from debug import Printable
from models.establishment import Establishment


class Route(Printable, Iterable[Establishment]):
    """
    A route to be taken by a brigade
    """

    def __init__(self, route_establishments: list[Establishment]):
        self.route_establishments = route_establishments

    def __iter__(self) -> Iterator[Establishment]:
        return self.route_establishments.__iter__()
