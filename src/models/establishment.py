"""
Logic related to an Establishment in the context of our problem
"""

from dataclasses import dataclass
from debug import Printable
from models.parse import Parsable, get_named_field


@dataclass
class EstablishmentAddress(Printable, Parsable):
    """
    Holds data about an establishment's address
    """

    district: str
    county: str
    parish: str
    full_address: str

    @staticmethod
    def parse(data):
        district = get_named_field(data, "District", str)
        county = get_named_field(data, "County", str)
        parish = get_named_field(data, "Parish", str)
        full_address = get_named_field(data, "Address", str)
        return EstablishmentAddress(district, county, parish, full_address)


@dataclass
class Coords(Printable, Parsable):
    """
    A pair of coordinates
    """

    latitude: float
    longitude: float

    @staticmethod
    def parse(data):
        lat = get_named_field(data, "Latitude", float)
        long = get_named_field(data, "Longitude", float)

        return Coords(lat, long)


@dataclass
class InspectionData(Printable, Parsable):
    """
    Data regarding an establishment inspection
    """

    inspection_utility: float
    inspection_time: int

    @staticmethod
    def parse(data):
        inspection_utility = get_named_field(data, "Inspection Utility", float)
        inspection_time = get_named_field(data, "Inspection Time", int)

        return InspectionData(inspection_utility, inspection_time)


class Establishment(Printable, Parsable):
    """
    Represents an Establishment in the context of the problem being tackled
    """

    def __init__(
        self,
        establishment_id: int,
        address: EstablishmentAddress,
        coords: Coords,
        inspection_data: InspectionData,
        opening_hours_str: str,
    ):
        self.establishment_id = int(establishment_id)
        self.address = address
        self.coords = coords
        self.inspection_data = inspection_data
        self.opening_hours: list[int] = list(
            map(int, opening_hours_str.removeprefix("[").removesuffix("]").split(", "))
        )
        self.visited = False

    def is_open(self, hour: int) -> bool:
        """
        Checks if an establishment is open at the given hour
        """

        assert 1 <= hour <= 24, "Invalid hour value"

        return self.opening_hours[hour - 1] == 1

    def is_visited(self) -> bool:
        """
        Returns whether this establishment has already been visited or not
        """

        return self.visited

    @staticmethod
    def parse(data):
        id = get_named_field(data, "Id", int)
        address = EstablishmentAddress.parse(data)
        coords = Coords.parse(data)
        inspection_data = InspectionData.parse(data)
        opening_hours = get_named_field(data, "Opening Hours", str)

        return Establishment(id, address, coords, inspection_data, opening_hours)
