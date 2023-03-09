import numpy as np
from typing import List

from debug import Printable


class Graph(Printable):
    def __init__(self, mat: List[List[float]]):
        self.mat = np.matrix(mat)
