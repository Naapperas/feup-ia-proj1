# pylint: skip-file

"""
Functions and classes related to the application
"""

from itertools import pairwise

import pygame
from numpy import clip, negative

from app.events import event, listener
from models.coords import Coords
from simulation import Simulation

MIN_LAT = 41.01793
MAX_LAT = 41.46618
LAT_RANGE = MAX_LAT - MIN_LAT
MIN_LNG = -8.77894
MAX_LNG = -7.9169
LNG_RANGE = MAX_LNG - MIN_LNG

MAP_MIN_X = 72
MAP_X_RANGE = 884
MAP_MAX_X = MAP_MIN_X + MAP_X_RANGE
MAP_MIN_Y = 206
MAP_Y_RANGE = 612
MAP_MAX_Y = MAP_MIN_Y + MAP_Y_RANGE


class Visualization:
    """
    Class representing the simulation's visualization
    """

    __slots__ = [
        "cache",
        "flag",
        "map",
        "pin",
        "drawn_map",
        "translation",
        "zoom",
    ]

    def __init__(self):
        listener(self)
        self.zoom = 1
        self.translation = (0, 0)

        self.map = pygame.image.load("resources/images/Porto.png").convert()
        self.pin = pygame.transform.scale_by(
            pygame.image.load("resources/images/pin.png").convert_alpha(), 2
        )
        self.flag = pygame.transform.scale_by(
            pygame.image.load("resources/images/flag.png").convert_alpha(), 2
        )

        self.cache: tuple[
            tuple[float, float],  # depot
            list[tuple[float, float]],  # establishments
            list[list[tuple[float, float]]],  # routes
        ] = ((0, 0), [], [])

        self.redraw_map()

    def redraw_map(self):
        """
        Scales this visualization's map according to its zoom level
        and redraws this visualization's objects
        """

        self.drawn_map = pygame.transform.scale_by(self.map, self.zoom)

        self.redraw_brigades()
        self.redraw_establishments()
        self.redraw_establishment(self.cache[0], True)

    def redraw(self, simulation: Simulation):
        """
        Updates the visualization cache and redraws every object onto a static image
        """

        self.cache = (
            self.world_to_map(simulation.network.depot.coords),
            [self.world_to_map(e.coords) for e in simulation.establishments],
            [
                [self.world_to_map(e.coords) for e in b.route.route_establishments]
                for b in simulation.state.brigades
            ],
        )

        self.redraw_map()

    def draw(self, screen: pygame.Surface):
        """
        Draws this map on the given surfaces
        """
        screen.blit(self.drawn_map, self.map_to_screen())

    def redraw_brigades(self):
        """
        Draws the current state of the simulation
        """
        size = self.drawn_map.get_size()
        scaled = pygame.Surface((size[0] // 2, size[1] // 2), pygame.SRCALPHA)

        for brigade in self.cache[2]:
            self.redraw_brigade(scaled, brigade)

        self.drawn_map.blit(pygame.transform.scale(scaled, size), (0, 0))

    def redraw_brigade(
        self, surface: pygame.Surface, brigade: list[tuple[float, float]]
    ):
        """
        Draws the given brigade's route on the given surface
        """

        # since each route is a closed loop, add the first establishment again
        for start, end in pairwise([*brigade, brigade[0]]):
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (start[0] * self.zoom / 2, start[1] * self.zoom / 2),
                (end[0] * self.zoom / 2, end[1] * self.zoom / 2),
                1,
            )
            # TODO: draw arrow indicating the route direction

    def redraw_establishments(self):
        """
        Draws the establishments on the given surface
        """

        for establishment in self.cache[1]:
            self.redraw_establishment(establishment)

    def redraw_establishment(self, coords: tuple[float, float], is_depot: bool = False):
        """
        Draws the given establishment on the given surface
        """

        self.drawn_map.blit(
            self.flag if is_depot else self.pin,
            (
                coords[0] * self.zoom - self.pin.get_width() // 2,
                coords[1] * self.zoom - self.pin.get_height(),
            ),
        )

    def map_to_world(self, coords: tuple[float, float] = (0, 0)) -> Coords:
        """
        Converts the map pixel coordinates to the corresponding real world coordinates,
        returned as (latitude, longitude)
        """
        return Coords(
            (coords[1] - MAP_MAX_Y) / -MAP_Y_RANGE * LAT_RANGE + MIN_LAT,
            (coords[0] - MAP_MIN_X) / MAP_X_RANGE * LNG_RANGE + MIN_LNG,
        )

    def world_to_map(self, coords: Coords = Coords(0, 0)) -> tuple[float, float]:
        """
        Converts the real world coordinates to the corresponding map pixel coordinates
        """
        return (
            (coords.longitude - MIN_LNG) / LNG_RANGE * MAP_X_RANGE + MAP_MIN_X,
            (coords.latitude - MIN_LAT) / LAT_RANGE * -MAP_Y_RANGE + MAP_MAX_Y,
        )

    def screen_to_map(
        self, coords: tuple[float, float] = (0, 0)
    ) -> tuple[float, float]:
        """
        Converts the screen coordinates to the corresponding map pixel coordinates
        """
        return (
            coords[0] / max([self.zoom, 1]) + self.translation[0],
            coords[1] / max([self.zoom, 1]) + self.translation[1],
        )

    def map_to_screen(
        self, coords: tuple[float, float] = (0, 0)
    ) -> tuple[float, float]:
        """
        Converts the map pixel coordinates to the corresponding screen coordinates
        """
        return (
            (coords[0] - self.translation[0]) * max([self.zoom, 1]),
            (coords[1] - self.translation[1]) * max([self.zoom, 1]),
        )

    def screen_to_world(self, coords: tuple[float, float] = (0, 0)) -> Coords:
        """
        Converts the screen coordinates to the corresponding real world coordinates
        """
        return self.map_to_world(self.screen_to_map(coords))

    def world_to_screen(self, coords: Coords = Coords(0, 0)) -> tuple[float, float]:
        """
        Converts the real world coordinates to the corresponding screen coordinates
        """
        return self.map_to_screen(self.world_to_map(coords))

    def rect_in_screen(self, rect: tuple[float, float, float, float]) -> bool:
        """
        Checks if the given rectangle is within the screen
        """
        return (
            min(rect[0], rect[2]) < 1024
            or min(rect[1], rect[3]) < 1024
            or max(rect[0], rect[2]) > 0
            or max(rect[1], rect[3]) > 0
        )

    def in_screen(self, coords: tuple[float, float]) -> bool:
        """
        Checks if the given coordinates are within the screen
        """
        return 0 <= coords[0] <= 1024 and 0 <= coords[1] <= 1024

    def in_screen_loose(self, coords: tuple[float, float]) -> bool:
        """
        Checks if the given coordinates are within the screen
        """
        return -50 <= coords[0] <= 1024 + 50 and -50 <= coords[1] <= 1024 + 50

    @event(pygame.constants.MOUSEMOTION, buttons=(1, 0, 0))
    def on_pan(self, _event: pygame.event.Event):
        """
        Handler for mouse movements when the left mouse button is pressed
        """
        self.translation = self.screen_to_map(negative(_event.rel))
        self.clamp_values()

    @event(pygame.constants.MOUSEWHEEL)
    def on_zoom(self, _event: pygame.event.Event):
        """
        Handler for mouse zooms
        """
        pos = pygame.mouse.get_pos()
        self.translation = self.screen_to_map(pos)
        self.zoom += _event.y
        self.translation = self.screen_to_map(tuple(negative(pos)))
        self.clamp_values()
        self.redraw_map()

    def clamp_values(self):
        """
        Clamps this visualization's relevant values to their value interval
        """

        self.zoom = clip(self.zoom, 1, 10)
        self.translation = clip(self.translation, 0, 1024 - 1024 / self.zoom)
