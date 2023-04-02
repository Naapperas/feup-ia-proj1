"""
Classes and methods related to generating neighboring states
"""

from simulation.state import State


class Generator:  # pylint: disable=too-few-public-methods
    """
    A class for generating neighboring states given a specific one.
    """

    def apply(self, state: State) -> State:
        """Generates a neighboring state from the specified one.

        The default implementation simply returns a copy of the old state.

        Args:
            state (State): the old state

        Returns:
            State:  new state, which should be a "neighbor" of the old one
        """
        return state.copy()
