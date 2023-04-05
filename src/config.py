"""
Configuration related methods and classes go here
"""

import os
from typing import Optional

from dotenv import dotenv_values


class _Config:
    """
    App wide configuration values
    """

    def __init__(self) -> None:
        configs = {
            **os.environ,
            **dotenv_values(".env", verbose=True),  # load shared development variables
            **dotenv_values(".env.secret", verbose=True),  # load sensitive variables
        }

        self.__slots__ = list(configs.keys())
        self.__dict__.update(configs)

    def get(self, key: str, default: Optional[str] = None) -> str:
        """
        Gets the value associated with the given config key
        """
        return self.__dict__.get(key, default)

    def set(self, key: str, value: str):
        """
        Sets the given value associated to the given config key
        """
        self.__dict__[key] = value


Config = _Config()
