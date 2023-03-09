from typing import List

from .graph import *
from files import parse_file


def parse_graph(file: str) -> Graph:
    """
    Parses an input file and returns a dense graph representing its data
    """
    mat = []

    for line in parse_file(file):
        line = list(line.values())[1:]

        mat.append(list(map(float, line)))

    return Graph(mat)
