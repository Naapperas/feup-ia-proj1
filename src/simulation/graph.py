"""
Functions and classes related to graphs
"""

import numpy as np

from files import parse_file
from debug import Printable


class Graph(Printable):
    """
    A graph that stores its data as an adjacency matrix
    """

    def __init__(self, mat: list[list[float]]):
        self.mat = np.matrix(mat)  # type: ignore

    def get_row(self, establishment_id: int) -> list[float]:
        """
        Returns a row of the graph's matrix
        """

        return self.mat[establishment_id]

    def get_col(self, establishment_id: int) -> list[float]:
        """
        Returns a column of the graph's matrix
        """

        return self.mat[:, establishment_id]  # type: ignore

    def get(self, first_establishment_id: int, second_establishment_id: int) -> float:
        """
        Returns the element at the given column and row
        """

        return self.mat[first_establishment_id, second_establishment_id]


def parse_graph(file: str) -> Graph:
    """
    Parses an input file and returns a dense graph representing its data
    """
    mat: list[list[float]] = []

    for line in parse_file(file):
        line = list(line.values())[1:]

        mat.append(list(map(float, line)))

    return Graph(mat)
