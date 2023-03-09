"""
Logic related to an Establishment in the context of our problem
"""

from debug import Printable


class Establishment(Printable):
    """
    Represents an Establishment in the context of the problem being tackled
    """

    def __init__(
        self,
        establishment_id: int,
        district: str,
        county: str,
        parish: str,
        address: str,
        latitude: float,
        longitude: float,
        inspection_utility: int,
        inspection_time: int,
        opening_hours_str: str,
    ):
        self.establishment_id = int(establishment_id)
        self.district = district
        self.county = county
        self.parish = parish
        self.address = address
        self.coords = (float(latitude), float(longitude))
        self.inspection_utility = float(inspection_utility)
        self.inspection_time = int(inspection_time)  # minutes
        self.opening_hours: list[int] = list(
            map(int, opening_hours_str.removeprefix("[").removesuffix("]").split(", "))
        )

    def is_open(self, hour: int) -> bool:
        """
        Checks if an establishment is open at the given hour
        """

        assert 1 <= hour <= 24, "Invalid hour value"

        return self.opening_hours[hour - 1] == 1
