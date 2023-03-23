"""
The main module
"""

from copy import deepcopy
from random import sample
import numpy as np
from models import parse_model, Establishment, Brigade, Route
from graph import parse_graph
from app import App
from state import State

if __name__ == "__main__":
    establishments = parse_model("./resources/establishments.csv", Establishment)
    network = parse_graph("./resources/distances.csv")

    num_carriers: int = np.floor(0.1 * len(establishments))

    print("Matrix", network)
    print("Establishments", establishments)

    brigades: list[Brigade] = []

    establishments_copy = deepcopy(establishments)

    for i in range(num_carriers):
        route_establishments = sample(establishments_copy, num_carriers)

        # generate random initial state
        for establishment in route_establishments:
            establishments_copy.remove(establishment)

        route: Route = Route(route_establishments)
        brigade: Brigade = Brigade(route)

        brigades.append(brigade)

    state = State(establishments, brigades, network)

    App().loop()
