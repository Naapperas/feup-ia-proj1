"""
Classes and methods related to routes
"""

from debug import Printable
from models.establishment import Establishment


class Route(Printable):
    """
    A route to be taken by a brigade
    """

    def __init__(self, route_establishments: list[Establishment]):
        self.route_establishments = route_establishments
