"""
Classes and functions related to the establishment network
"""

from simulation.graph import Graph

from .establishment import Establishment


class Network:
    """
    The establishment network
    """

    def __init__(self, depot: Establishment, graph: Graph):
        self.depot = depot
        self.graph = graph
