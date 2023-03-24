# pylint: skip-file
# TODO: handle this

"""
Functions and classes related to the application
"""

import pygame
import pygame_gui
from pygame import constants
from .visualization import Visualization
from simulation import Simulation
from .events import listener, event, handle_events

from models import parse_model, Establishment
from graph import parse_graph
from state.state import State

# For development purposes
_NUM_MODELS_TO_PARSE: int = 20


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
        self.setup_simulation()

    def setup_simulation(self):
        """
        Sets up the simulation
        """
        establishments = parse_model(
            "./resources/establishments.csv", Establishment, _NUM_MODELS_TO_PARSE
        )
        network = parse_graph("./resources/distances.csv")

        depot, establishments = establishments[0], establishments[1:]

        num_carriers: int = Simulation.get_num_carriers(establishments)

        state: State = State.initial_state(establishments, num_carriers)

        self.simulation = Simulation(depot, state, network, establishments)

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
