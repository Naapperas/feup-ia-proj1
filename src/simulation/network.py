from graph.graph import Graph
from models.establishment import Establishment


class Network:
    def __init__(self, depot: Establishment, graph: Graph):
        self.depot = depot
        self.graph = graph
