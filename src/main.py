"""
The main module
"""

from models import parse_model, Establishment
from graph import parse_graph
from app import App
from simulation.heuristics.initial_state import initial_state
from simulation.simulation import Simulation
from state.state import State

if __name__ == "__main__":
    establishments = parse_model("./resources/establishments.csv", Establishment)
    network = parse_graph("./resources/distances.csv")

    depot, establishments = establishments[0], establishments[1:]

    num_carriers: int = Simulation.get_num_carriers(establishments)

    state: State = initial_state(establishments, num_carriers)

    print("Matrix", network)
    print("Establishments", establishments)
    print("State", state)

    simulation = Simulation(depot, state, network, establishments)

    App().loop()
