# pylint: skip-file
# TODO: handle this

"""
Functions and classes related to the application
"""

import pygame
import pygame_gui
from pygame import constants

from graph import parse_graph

# from models import Establishment, parse_model
from simulation import Simulation
from simulation.state import State

from .events import event, handle_events, listener
from .visualization import Visualization


class App:
    """
    The pygame app which will glue everything together
    """

    def __init__(self):
        pygame.init()
        listener(self)

        pygame.display.set_caption("ASAE Inspection Routes")
        self.screen = pygame.display.set_mode(
            (1024, 1024), constants.RESIZABLE | constants.DOUBLEBUF, vsync=True
        )
        self.clock = pygame.time.Clock()
        self.gui_manager = pygame_gui.UIManager(self.screen.get_size())

        self.running = True

        self.visualization = Visualization()
        self.simulation = Simulation.setup()

    def loop(self):
        """
        The pygame visualization's event loop
        """
        while self.running:
            self.delta_t = self.clock.tick(200) / 1000.0
            self.gui_manager.update(self.delta_t)

            handle_events(self)

            self.visualization.draw(self.screen, self.simulation)
            self.gui_manager.draw_ui(self.screen)
            pygame.display.flip()

    @event(constants.QUIT, constants.K_q)
    def on_quit(self, _event: pygame.event.Event):
        """
        Handler called when quitting the visualization
        """
        self.running = False
