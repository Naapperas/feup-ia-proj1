# pylint: skip-file
# TODO: handle this

"""
Functions and classes related to the application
"""

import pygame
import pygame_gui
import threading
from pygame import constants
from config import Config

from simulation import Simulation
from simulation.state import State
from simulation.heuristics.initial_state.closest import ClosestGenerator

from .events import event, handle_events, listener
from .visualization import Visualization
from .constants import *


class App:
    """
    The pygame app which will glue everything together
    """

    def __init__(self):
        pygame.init()
        listener(self)

        pygame.display.set_caption(Config.get("DISPLAY_TITLE"))
        self.screen = pygame.display.set_mode(
            (1024, 1024), constants.RESIZABLE | constants.DOUBLEBUF, vsync=True
        )
        self.clock = pygame.time.Clock()
        self.gui_manager = pygame_gui.UIManager(
            self.screen.get_size(), "resources/theme.json"
        )
        self.gui_manager.preload_fonts(
            [
                {
                    "name": "Minecraftia",
                    "point_size": 16,
                    "regular_path": "resources/font.ttf",
                }
            ]
        )

        self.running = True

        self.visualization = Visualization()

        self.simulation: Simulation | None = None

        self.setup_ui()

        threading.Thread(target=self.setup_simulation).start()

    def setup_ui(self):
        """
        Sets up the UI
        """

        pygame_gui.elements.UILabel(
            text=Config.get("DISPLAY_TITLE"),
            relative_rect=pygame.Rect(0, -480, 1024, 64),
            manager=self.gui_manager,
            anchors={"center": "center"},
            object_id="#big",
        )

        self.loading = pygame_gui.elements.UIPanel(
            relative_rect=self.screen.get_rect(), manager=self.gui_manager
        )
        pygame_gui.elements.UILabel(
            text="Loading...",
            relative_rect=pygame.Rect(0, 0, 1024, 64),
            manager=self.gui_manager,
            anchors={"center": "center"},
            container=self.loading,
            object_id="#big",
        )

        self.main_menu = pygame_gui.elements.UIPanel(
            relative_rect=self.screen.get_rect(), manager=self.gui_manager
        )
        pygame_gui.elements.UIButton(
            text="Start simulation",
            relative_rect=pygame.Rect(0, -40, 256, 64),
            manager=self.gui_manager,
            anchors={"center": "center"},
            container=self.main_menu,
            object_id=START_SIMULATION,
        )
        pygame_gui.elements.UIButton(
            text="Quit",
            relative_rect=pygame.Rect(0, 40, 256, 64),
            manager=self.gui_manager,
            anchors={"center": "center"},
            container=self.main_menu,
            object_id=QUIT,
        )
        self.establishments_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 480, 992, 32),
            start_value=0,
            value_range=(0, 100),
            manager=self.gui_manager,
            anchors={"center": "center"},
            container=self.main_menu,
            object_id=NUM_ESTABLISHMENTS,
            click_increment=100,
        )
        self.establishments_label = pygame_gui.elements.UILabel(
            text="x establishments",
            relative_rect=pygame.Rect(0, 480, 1024, 32),
            manager=self.gui_manager,
            anchors={"center": "center"},
            container=self.main_menu,
        )
        self.main_menu.hide()

    def setup_simulation(self):
        """
        Sets up the simulation
        """

        self.simulation = Simulation.setup()
        self.visualization.redraw(self.simulation)
        self.loading.hide()
        self.main_menu.show()
        self.establishments_slider.value_range = (
            0,
            len(self.simulation.establishments),
        )
        self.establishments_slider.set_current_value(self.simulation.num_establishments)
        self.establishments_label.set_text(
            f"{self.simulation.num_establishments} establishments"
        )

    def loop(self):
        """
        The pygame visualization's event loop
        """
        while self.running:
            self.delta_t = self.clock.tick() / 1000.0
            self.gui_manager.update(self.delta_t)

            print(f"{self.clock.get_fps():.2f} FPS      ", end="\r")

            handle_events(self)

            self.visualization.draw(self.screen)
            self.gui_manager.draw_ui(self.screen)
            pygame.display.flip()

    @event(pygame_gui.UI_BUTTON_PRESSED, ui_object_id=f"panel.{QUIT}")
    @event(constants.QUIT, constants.K_q)
    def on_quit(self, _event: pygame.event.Event):
        """
        Handler called when quitting the visualization
        """
        self.running = False

    @event(pygame_gui.UI_BUTTON_PRESSED, ui_object_id=f"panel.{START_SIMULATION}")
    def on_start_simulation(self, event: pygame.event.Event):
        """
        Handler called when a button is pressed
        """

        self.main_menu.hide()
        self.loading.show()
        threading.Thread(target=self.initial_state).start()

    def initial_state(self):
        if self.simulation is not None:
            self.simulation.state = State.initial_state(
                self.simulation.establishments,
                self.simulation.network,
                self.simulation.get_num_carriers(),
                ClosestGenerator,
            )
            self.visualization.redraw(self.simulation)
        self.loading.hide()

    @event(
        pygame_gui.UI_HORIZONTAL_SLIDER_MOVED,
        ui_object_id=f"panel.{NUM_ESTABLISHMENTS}",
    )
    def on_num_establishments(self, event: pygame.event.Event):
        """
        Handler called when the number of establishments is changed
        """

        if self.simulation is not None:
            self.simulation.num_establishments = event.value
        self.establishments_label.set_text(f"{event.value} establishments")
