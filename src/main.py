"""
The main module
"""

from typing import Type
from models import parse_model, Establishment
from graph import parse_graph

if __name__ == "__main__":
    establishments = parse_model("./resources/establishments.csv", Establishment) # TODO: figure out a way to remove this type error
    matrix = parse_graph("./resources/distances.csv")

    print("Matrix", matrix)
    print("Establishments", "\n".join(map(str, establishments)))
