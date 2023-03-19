"""
Functions and classes related to the application
"""

from typing import Callable
import pygame
from pygame import constants
from visualization import Visualization


class App:
    """
    The pygame app which will glue everything together
    """

    __slots__ = ["EVENTS", "running", "clock", "screen", "visualization", "buttons"]

    def __init__(self):
        pygame.init()

        self.EVENTS: dict[int, Callable[[pygame.event.Event], None]] = {
            constants.QUIT: self.on_quit,
            # pygame.VIDEORESIZE: self.on_resize,
            constants.MOUSEBUTTONDOWN: self.mouse_event("down"),
            constants.MOUSEBUTTONUP: self.mouse_event("up"),
            constants.MOUSEMOTION: self.mouse_event("move"),
            # pygame.LETDOWN: self.on_key
        }

        self.buttons = {k: False for k in "lrm"}

        pygame.display.set_caption("ASAE Inspection Routes")
        self.screen = pygame.display.set_mode(
            (800, 800), constants.RESIZABLE | constants.DOUBLEBUF, vsync=True
        )
        self.clock = pygame.time.Clock()

        self.running = True

        self.visualization = Visualization()

    def loop(self):
        """
        The pygame visualization's event loop
        """
        x = 0

        while self.running:
            self.clock.tick(200)

            self.events()

            x = (x + 1) % (1024 * 4 - 800)

            self.visualization.draw(self.screen)
            pygame.display.flip()

    def events(self):
        """
        Process pending events
        """
        for event in pygame.event.get():
            try:
                self.EVENTS[event.type](event)
            except KeyError as err:
                print(
                    f"Event {pygame.event.event_name(event.type)} not handled",
                    event.__dict__,
                )

    def mouse_event(self, name):
        """
        Returns a handler that can process named mouse events
        """

        def inner(event):
            """
            Called whenever there is a mouse event
            """
            btns = []
            button, buttons = getattr(event, "button", -1), getattr(
                event, "buttons", []
            )
            if button == constants.BUTTON_LEFT or constants.BUTTON_LEFT in buttons:
                btns.append("l")
            if button == constants.BUTTON_RIGHT or constants.BUTTON_RIGHT in buttons:
                btns.append("r")
            if button == constants.BUTTON_MIDDLE or constants.BUTTON_MIDDLE in buttons:
                btns.append("m")

            for button in btns:
                getattr(self, f"on_mouse{name}", lambda e, b: None)(event, button)
                getattr(self, f"on_mouse{name}_{button}", lambda e: None)(event)
                getattr(self.visualization, f"on_mouse{name}", lambda e, b: None)(
                    event, button
                )
                getattr(self.visualization, f"on_mouse{name}_{button}", lambda e: None)(
                    event
                )

        return inner

    def on_quit(self, _event: pygame.event.Event):
        """
        Handler called when quitting the visualization
        """
        self.running = False
