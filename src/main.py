"""
The main module
"""

from models import parse_model, Establishment
from graph import parse_graph
from app import App

if __name__ == "__main__":
    establishments = parse_model("./resources/establishments.csv", Establishment)
    matrix = parse_graph("./resources/distances.csv")

    print("Matrix", matrix)
    print("Establishments", establishments)

    App().loop()
