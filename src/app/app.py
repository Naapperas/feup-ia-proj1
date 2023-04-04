# pylint: skip-file
# TODO: handle this

"""
Functions and classes related to the application
"""

import threading
from typing import Callable

import pygame
import pygame_gui
from pygame import constants

from config import Config
from simulation import Simulation, SimulationStatistics
from simulation.heuristics.initial_state.closest import ClosestGenerator
from simulation.heuristics.initial_state.generator import (
    Generator as InitialStateGenerator,
)
from simulation.heuristics.initial_state.random import (
    RandomGenerator as RandomInitialStateGenerator,
)
from simulation.heuristics.meta.metaheuristic import Metaheuristic
from simulation.heuristics.meta.simulated_annealing import SimulatedAnnealing
from simulation.heuristics.neighborhood.crossover import CrossoverGenerator
from simulation.heuristics.neighborhood.generator import (
    Generator as NeighborhoodGenerator,
)
from simulation.heuristics.neighborhood.multiple import MultiGenerator
from simulation.heuristics.neighborhood.mutation import MutationGenerator
from simulation.heuristics.neighborhood.random import (
    RandomGenerator as RandomNeighborhoodGenerator,
)
from simulation.heuristics.neighborhood.shuffle import ShuffleGenerator
from simulation.simulation import SimulationConfig
from simulation.state import State

from .constants import *
from .events import event, handle_events, listener
from .visualization import Visualization


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
                    "regular_path": "resources/fonts/font.ttf",
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
            object_id=MAIN_MENU_QUIT,
        )
        self.establishments_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(0, 480, 992, 32),
            start_value=65,
            value_range=(30, 100),
            manager=self.gui_manager,
            anchors={"center": "center"},
            container=self.main_menu,
            object_id=NUM_ESTABLISHMENTS,
            click_increment=10,
        )
        self.establishments_label = pygame_gui.elements.UILabel(
            text="x establishments",
            relative_rect=pygame.Rect(0, 480, 1024, 32),
            manager=self.gui_manager,
            anchors={"center": "center"},
            container=self.main_menu,
        )

        self.statistics = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(0, 0, 400, 400),
            manager=self.gui_manager,
            anchors={"center": "center"},
            object_id=STATISTICS_PANEL,
        )
        pygame_gui.elements.UILabel(
            text="Statistics",
            relative_rect=pygame.Rect(0, 0, 224, 45),
            manager=self.gui_manager,
            anchors={"top": "top", "centerx": "centerx"},
            container=self.statistics,
            object_id="#big",
        )
        self.total_iterations_label = pygame_gui.elements.UILabel(
            text="Total iterations: x",
            relative_rect=pygame.Rect(0, 70, 224, 32),
            manager=self.gui_manager,
            anchors={"centerx": "centerx"},
            container=self.statistics,
        )
        self.total_runtime = pygame_gui.elements.UILabel(
            text="Total runtime(s): x",
            relative_rect=pygame.Rect(0, 110, 1024, 32),
            manager=self.gui_manager,
            anchors={"centerx": "centerx"},
            container=self.statistics,
        )
        pygame_gui.elements.UILabel(
            text="Initial waiting time(/s):",
            relative_rect=pygame.Rect(0, 150, 1024, 32),
            manager=self.gui_manager,
            anchors={"centerx": "centerx"},
            container=self.statistics,
        )
        self.initial_value = pygame_gui.elements.UILabel(
            text="x",
            relative_rect=pygame.Rect(0, 175, 1024, 32),
            manager=self.gui_manager,
            anchors={"centerx": "centerx"},
            container=self.statistics,
        )
        pygame_gui.elements.UILabel(
            text="Best calculated waiting time(/s):",
            relative_rect=pygame.Rect(0, 215, 1024, 32),
            manager=self.gui_manager,
            anchors={"centerx": "centerx"},
            container=self.statistics,
        )
        self.final_value = pygame_gui.elements.UILabel(
            text="x",
            relative_rect=pygame.Rect(0, 240, 1024, 32),
            manager=self.gui_manager,
            anchors={"centerx": "centerx"},
            container=self.statistics,
        )
        self.improvement = pygame_gui.elements.UILabel(
            text="Improvement: x%",
            relative_rect=pygame.Rect(0, 280, 1024, 32),
            manager=self.gui_manager,
            anchors={"centerx": "centerx"},
            container=self.statistics,
        )

        self.main_menu.hide()
        self.statistics.hide()

    def setup_simulation(self):
        """
        Sets up the simulation
        """

        # HACK: due to time restrictions, this is done this way. However, this should be configured somewhere else
        # it should also be configurable through the GUI

        # could add support for more in the future
        fitness_function: Callable[[State], float] = lambda state: -state.value()

        neighborhood_generators = {
            "default": NeighborhoodGenerator(),
            "crossover": CrossoverGenerator(),
            "mutation": MutationGenerator(),
            "random": RandomNeighborhoodGenerator(
                [
                    CrossoverGenerator(),
                    MutationGenerator(),
                ],
                randomize=True,
            ),
            "multi": MultiGenerator(
                [
                    CrossoverGenerator(),
                    MutationGenerator(),
                ]
            ),
            "shuffle": ShuffleGenerator(),
        }
        neighborhood_generator: NeighborhoodGenerator = neighborhood_generators[
            Config.get("NEIGHBORHOOD_GENERATOR")
        ]

        metaheuristics = {
            "default": Metaheuristic(neighborhood_generator, fitness_function),
            "sa": SimulatedAnnealing(
                neighborhood_generator,
                fitness_function,
                float(Config.get("SA_INITIAL_TEMPERATURE")),
                float(Config.get("SA_COOLDOWN_RATE")),
                float(Config.get("SA_MIN_TEMPERATURE")),
            ),
        }
        metaheuristic: Metaheuristic = metaheuristics[Config.get("METAHEURISTIC")]

        simulation_config = SimulationConfig(
            metaheuristic, fitness_function, neighborhood_generator
        )

        self.simulation = Simulation.setup(simulation_config)

        self.visualization.redraw(self.simulation)

        self.loading.hide()
        self.main_menu.show()

        self.establishments_slider.value_range = (
            0,
            len(self.simulation.state.network.establishments),
        )
        self.establishments_slider.set_current_value(
            len(self.simulation.state.network.establishments)
        )
        self.establishments_label.set_text(
            f"{len(self.simulation.state.network.establishments)} establishments"
        )

    def loop(self):
        """
        The pygame visualization's event loop
        """
        while self.running:
            self.delta_t = self.clock.tick() / 1000.0
            self.gui_manager.update(self.delta_t)

            # print(f"{self.clock.get_fps():.2f} FPS      ", end="\r")

            handle_events(self)

            self.visualization.draw(self.screen)
            self.gui_manager.draw_ui(self.screen)
            pygame.display.flip()

    @event(pygame_gui.UI_BUTTON_PRESSED, ui_object_id=f"panel.{MAIN_MENU_QUIT}")
    @event(constants.QUIT, constants.KEYDOWN)
    def on_quit(self, _event: pygame.event.Event):
        """
        Handler called when quitting the visualization
        """

        if _event.type == constants.KEYDOWN:
            if _event.key == constants.K_q:
                self.running = False
        else:
            self.running = False

    @event(pygame_gui.UI_BUTTON_PRESSED, ui_object_id=f"panel.{START_SIMULATION}")
    def on_start_simulation(self, _event: pygame.event.Event):
        """
        Handler called when a button is pressed
        """

        self.main_menu.hide()
        self.loading.show()
        threading.Thread(target=self.run_simulation, daemon=True).start()

    def run_simulation(self):
        """
        Thread runner to run the simulation in parallel
        """

        initial_state_thread = threading.Thread(target=self.initial_state)
        initial_state_thread.start()
        initial_state_thread.join()

        assert self.simulation is not None, "Simulation is not set up"

        print("Running simulation...")

        for new_state in self.simulation.run():
            print("Got new state with value: ", new_state.cached_value)
            self.visualization.redraw(self.simulation)

        print("Finished running simulation")

        self.load_stats(self.simulation.stats)

    def load_stats(self, stats: SimulationStatistics):
        """
        Loads the statistics of the simulation
        """

        self.total_iterations_label.set_text(
            f"Total iterations: {stats.total_iterations}"
        )
        self.total_runtime.set_text(f"Total runtime(/s): {stats.runtime:.2f}")
        self.initial_value.set_text(f"{stats.values[0]:.2f}")
        self.final_value.set_text(f"{stats.values[-1]:.2f}")
        self.improvement.set_text(
            f"Improvement: {(((stats.values[0] - stats.values[-1]) / stats.values[0]) * 100):.2f}%"
        )
        self.statistics.show()

    def initial_state(self):
        """
        Thread runner to load the initial state in parallel
        """

        if self.simulation is not None:
            print("Loading initial state...")
            network = (
                self.simulation.state.network
            )  # Simulations start with a dummy state that already has the network loaded

            # HACK: same as above
            generators = {
                "random": InitialStateGenerator(),
                "closest": ClosestGenerator(),
                "default": RandomInitialStateGenerator(),
            }

            generator: InitialStateGenerator = generators[
                Config.get("INITIAL_STATE_GENERATOR")
            ]

            self.simulation.state = State.initial_state(
                network.depot,
                network.graph,
                network.establishments,
                self.simulation.get_num_carriers(),
                generator,
            )
            self.visualization.redraw(self.simulation)
        self.loading.hide()

    @event(
        pygame_gui.UI_HORIZONTAL_SLIDER_MOVED,
        ui_object_id=f"panel.{NUM_ESTABLISHMENTS}",
    )
    def on_num_establishments(self, _event: pygame.event.Event):
        """
        Handler called when the number of establishments is changed
        """

        if self.simulation is not None:
            self.simulation.num_establishments = _event.value
        self.establishments_label.set_text(f"{_event.value} establishments")
