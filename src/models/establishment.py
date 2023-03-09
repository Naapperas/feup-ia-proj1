from debug import Printable


class Establishment(Printable):
    """
        Represents an Establishment in the context of the problem being tackled
    """

    def __init__(self, id: int, district: str, county: str, parish: str,
                 address: str, latitude: float, longitude: float,
                 inspection_utility: int, inspection_time: int,
                 opening_hours_str: str):
        self.id = int(id)
        self.district = district
        self.county = county
        self.parish = parish
        self.address = address
        self.coords = (float(latitude), float(longitude))
        self.inspection_utility = float(inspection_utility)
        self.inspection_time = int(inspection_time)  # minutes
        self.opening_hours: list[int] = eval(opening_hours_str)
