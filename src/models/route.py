"""
Classes and methods related to routes
"""

from typing import Iterable, Iterator, SupportsIndex, overload

from debug import Printable
from models.establishment import Establishment


class Route(Printable, Iterable[Establishment]):
    """
    A route to be taken by a brigade
    """

    def __init__(self, route_establishments: list[Establishment]):
        self.route_establishments = route_establishments

    def __iter__(self) -> Iterator[Establishment]:
        return iter(self.route_establishments)

    def __len__(self) -> int:
        return len(self.route_establishments)

    @overload
    def __getitem__(self, __i: SupportsIndex) -> Establishment:
        ...

    @overload
    def __getitem__(self, __s: slice) -> list[Establishment]:
        ...

    def __getitem__(
        self, __arg: slice | SupportsIndex
    ) -> Establishment | list[Establishment]:
        return self.route_establishments[__arg]
