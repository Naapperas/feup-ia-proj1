import pygame
from visualization import Visualization
from typing import Callable


class App:
    __slots__ = ["EVENTS", "running", "clock", "screen", "visualization", "buttons"]

    def __init__(self):
        pygame.init()

        self.EVENTS: dict[int, Callable[[pygame.event.Event], None]] = {
            pygame.QUIT: self.on_quit,
            # pygame.VIDEORESIZE: self.on_resize,
            pygame.MOUSEBUTTONDOWN: self.mouse_event("down"),
            pygame.MOUSEBUTTONUP: self.mouse_event("up"),
            pygame.MOUSEMOTION: self.mouse_event("move"),
            # pygame.KEYDOWN: self.on_key
        }

        self.buttons = {k: False for k in "lrm"}

        pygame.display.set_caption("ASAE Inspection Routes")
        self.screen = pygame.display.set_mode(
            (800, 800), pygame.RESIZABLE | pygame.DOUBLEBUF, vsync=True
        )
        self.clock = pygame.time.Clock()

        self.running = True

        self.visualization = Visualization()

    def loop(self):
        x = 0

        while self.running:
            self.clock.tick(200)

            self.events()

            x = (x + 1) % (1024 * 4 - 800)

            self.visualization.draw(self.screen)
            pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            try:
                self.EVENTS[event.type](event)
            except KeyError as e:
                print(
                    f"Event {pygame.event.event_name(event.type)} not handled",
                    event.__dict__,
                )

    def mouse_event(self, name):
        def inner(event):
            btns = []
            button, buttons = getattr(event, "button", -1), getattr(
                event, "buttons", []
            )
            if button == pygame.BUTTON_LEFT or pygame.BUTTON_LEFT in buttons:
                btns.append("l")
            if button == pygame.BUTTON_RIGHT or pygame.BUTTON_RIGHT in buttons:
                btns.append("r")
            if button == pygame.BUTTON_MIDDLE or pygame.BUTTON_MIDDLE in buttons:
                btns.append("m")

            for b in btns:
                getattr(self, f"on_mouse{name}", lambda e, b: None)(event, b)
                getattr(self, f"on_mouse{name}_{b}", lambda e: None)(event)
                getattr(self.visualization, f"on_mouse{name}", lambda e, b: None)(
                    event, b
                )
                getattr(self.visualization, f"on_mouse{name}_{b}", lambda e: None)(
                    event
                )

        return inner

    def on_quit(self, _event: pygame.event.Event):
        self.running = False
