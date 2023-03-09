"""
Logic related to parsing the problem's graph out of a text file
"""

from files import parse_file
from .graph import *


def parse_graph(file: str) -> Graph:
    """
    Parses an input file and returns a dense graph representing its data
    """
    mat = []

    for line in parse_file(file):
        line = list(line.values())[1:]

        mat.append(list(map(float, line)))

    return Graph(mat)
