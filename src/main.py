"""
The main module
"""

from models import parse_model, Establishment
from graph import parse_graph

if __name__ == "__main__":
    establishments = parse_model("./resources/establishments.csv", Establishment)
    matrix = parse_graph("./resources/distances.csv")

    print("Matrix", matrix)
    print("Establishments", "\n".join(map(str, establishments)))
