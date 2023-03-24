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
        "map",
        "scaled_map",
        "translation",
        "zoom",
    ]

    def __init__(self):
        listener(self)
        self.zoom = 1
        self.translation = (0, 0)

        self.map = pygame.image.load("resources/Porto.png")
        self.scaled_map = pygame.transform.scale_by(self.map, self.zoom)

    def scale_map(self):
        self.scaled_map = pygame.transform.scale_by(self.map, self.zoom)

    def draw(self, screen: pygame.Surface, simulation: Simulation):
        """
        Draws this map on the given surfaces
        """
        screen.blit(self.scaled_map, self.map_to_screen())
        self.draw_state(screen, simulation)
        self.draw_establishments(screen, simulation)

    def draw_state(self, screen: pygame.Surface, simulation: Simulation):
        """
        Draws the current state of the simulation
        """
        for brigade in simulation.state.brigades:
            for start, end in pairwise(brigade.route):
                start = self.world_to_screen(start.coords)
                end = self.world_to_screen(end.coords)
                if self.rect_in_screen((*start, *end)):
                    pygame.draw.line(
                        screen,
                        (0, 0, 255),
                        start,
                        end,
                        2,
                    )

    def draw_establishments(self, screen: pygame.Surface, simulation: Simulation):
        """
        Draws the establishments on the given surface
        """
        for establishment in simulation.establishments:
            coords = self.world_to_screen(establishment.coords)
            if self.in_screen_loose(coords):
                pygame.draw.circle(screen, (255, 0, 0), coords, 5)

        coords = self.world_to_screen(simulation.depot.coords)
        if self.in_screen_loose(coords):
            pygame.draw.circle(screen, (0, 255, 0), coords, 5)

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
            coords[0] / self.zoom + self.translation[0],
            coords[1] / self.zoom + self.translation[1],
        )

    def map_to_screen(
        self, coords: tuple[float, float] = (0, 0)
    ) -> tuple[float, float]:
        """
        Converts the map pixel coordinates to the corresponding screen coordinates
        """
        return (
            (coords[0] - self.translation[0]) * self.zoom,
            (coords[1] - self.translation[1]) * self.zoom,
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
        return -10 <= coords[0] <= 1024 + 10 and -10 <= coords[1] <= 1024 + 10

    @event(pygame.constants.MOUSEMOTION, buttons=(1, 0, 0))
    def on_pan(self, event: pygame.event.Event):
        """
        Handler for mouse movements when the left mouse button is pressed
        """
        self.translation = self.screen_to_map(negative(event.rel))
        self.clamp_values()
        print(event)

    @event(pygame.constants.MOUSEWHEEL)
    def on_zoom(self, event: pygame.event.Event):
        """
        Handler for mouse zooms
        """
        self.zoom += event.y
        self.clamp_values()
        self.scale_map()

    def clamp_values(self):
        """
        Clamps this visualization's relevant values to their value interval
        """

        self.zoom = clip(self.zoom, 1, 10)
        self.translation = clip(self.translation, 0, 1024 - 1024 / self.zoom)
