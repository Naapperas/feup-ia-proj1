"""
Classes and methods related to coordinates
"""

import sys
from dataclasses import dataclass
from typing import ClassVar

import numpy as np

from debug import Printable
from models.parse import Parsable, get_named_field

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


@dataclass
class Coords(Printable, Parsable):
    """
    A pair of coordinates
    """

    latitude: float
    longitude: float

    EARTH_RADIUS_KM: ClassVar[int] = 6371

    @staticmethod
    def parse(data):
        lat = get_named_field(data, "Latitude", float)
        long = get_named_field(data, "Longitude", float)

        return Coords(lat, long)

    def as_tuple(self) -> tuple[float, float]:
        """
        Returns this coordinate pair as a tuple of latitude and longitude
        """

        return (self.latitude, self.longitude)

    def round_dist_to(self, other: Self) -> float:
        """
        Returns the distance between the two coordinates
        as if they were on the surface of the earth,
        as per the Haversine formula: https://en.wikipedia.org/wiki/Haversine_formula
        """

        lat_diff: float = np.radians(other.latitude - self.latitude)
        long_diff: float = np.radians(other.longitude - self.longitude)

        self_lat_rad: float = np.radians(self.latitude)
        other_lat_rad: float = np.radians(other.latitude)

        arc: float = np.power(np.sin(lat_diff / 2), 2) + np.power(
            np.sin(long_diff / 2), 2
        ) * np.cos(self_lat_rad) * np.cos(other_lat_rad)
        coef: float = 2 * np.arcsin(np.sqrt(arc))

        return coef * Coords.EARTH_RADIUS_KM
