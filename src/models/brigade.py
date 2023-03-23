"""
Classes and methods related to brigades
"""

from debug import Printable
from models.route import Route


class Brigade(Printable):
    """
    An inspection brigade that is responsible for visiting establishments on a route
    """

    def __init__(self, route: Route):
        self.route = route
