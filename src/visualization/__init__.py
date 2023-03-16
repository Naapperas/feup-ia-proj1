import pygame

MIN_LAT = 41.01793
MAX_LAT = 41.46618
LAT_RANGE = MAX_LAT - MIN_LAT
MIN_LNG = -8.77894
MAX_LNG = -7.9169
LNG_RANGE = MAX_LNG - MIN_LNG

MIN_MAP_X = 72
MAP_X_RANGE = 884
MAX_MAP_X = MIN_MAP_X + MAP_X_RANGE
MIN_MAP_Y = 206
MAP_Y_RANGE = 612
MAX_MAP_Y = MIN_MAP_Y + MAP_Y_RANGE


class Visualization:
    __slots__ = ["map", "scaled_map", "translation", "zoom"]

    def __init__(self):
        self.zoom = 4
        self.translation = (0, 0)

        self.map = pygame.image.load("resources/Porto.png")
        self.scaled_map = pygame.transform.scale_by(self.map, self.zoom)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.scaled_map, self.map_to_screen())

    def map_to_world(self, coords: tuple[float, float] = (0, 0)) -> tuple[float, float]:
        """
        Converts the map pixel coordinates to the corresponding real world coordinates, returned as (latitude, longitude)
        """
        return (
            (coords[1] - MIN_MAP_Y) / MAP_Y_RANGE * LAT_RANGE + MIN_LAT,
            (coords[0] - MIN_MAP_X) / MAP_X_RANGE * LNG_RANGE + MIN_LNG,
        )

    def world_to_map(self, coords: tuple[float, float] = (0, 0)) -> tuple[float, float]:
        """
        Converts the real world coordinates to the corresponding map pixel coordinates
        """
        return (
            (coords[1] - MAX_LNG) / LNG_RANGE * MAP_X_RANGE + MIN_MAP_X,
            (coords[0] - MIN_LAT) / LAT_RANGE * MAP_Y_RANGE + MIN_MAP_Y,
        )

    def screen_to_map(
        self, coords: tuple[float, float] = (0, 0)
    ) -> tuple[float, float]:
        return (
            coords[0] / self.zoom + self.translation[0],
            coords[1] / self.zoom + self.translation[1],
        )

    def map_to_screen(
        self, coords: tuple[float, float] = (0, 0)
    ) -> tuple[float, float]:
        return (
            (coords[0] - self.translation[0]) * self.zoom,
            (coords[1] - self.translation[1]) * self.zoom,
        )

    def on_mousemove_l(self, event: pygame.event.Event):
        rel = self.screen_to_map((-event.rel[0], -event.rel[1]))

        self.translation = (
            min(1024, max(0, rel[0])),
            min(1024, max(0, rel[1])),
        )
