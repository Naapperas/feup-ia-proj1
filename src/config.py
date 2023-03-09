"""
Configuration related methods and classes go here
"""

import os
from dotenv import dotenv_values


class Config:
    """
    App wide configuration values
    """

    def __init__(self) -> None:
        configs = {
            **os.environ,
            **dotenv_values(".env", verbose=True),  # load shared development variables
            **dotenv_values(".env.secret", verbose=True),  # load sensitive variables
        }

        self.__slots__ = configs.keys()
        self.__dict__.update(configs)
