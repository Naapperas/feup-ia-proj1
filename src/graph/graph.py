"""
Functions and classes related to graphs
"""

import numpy as np

from debug import Printable


class Graph(Printable):
    """
    A graph that stores its data as an adjacency matrix
    """

    def __init__(self, mat: list[list[float]]):
        self.mat = np.matrix(mat) # type: ignore

    def get_row(self, establishment_id: int) -> list[float]:
        """
        Returns a row of the graph's matrix
        """

        return self.mat[establishment_id]

    def get_col(self, establishment_id: int) -> list[float]:
        """
        Returns a column of the graph's matrix
        """

        return self.mat[:, establishment_id] # type: ignore
