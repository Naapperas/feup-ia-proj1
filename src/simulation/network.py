"""
Classes and functions related to the establishment network
"""

from graph.graph import Graph
from models.establishment import Establishment


class Network:
    """
    The establishment network
    """

    def __init__(self, depot: Establishment, graph: Graph):
        self.depot = depot
        self.graph = graph
