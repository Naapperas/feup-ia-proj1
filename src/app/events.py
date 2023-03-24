"""
Application events
"""

from collections import defaultdict
from typing import Any, Callable

import pygame

events: defaultdict[
    int, list[tuple[dict, Callable[[Any, pygame.event.Event], Any]]]
] = defaultdict(list)

listeners: defaultdict[str, list[Any]] = defaultdict(list)


def listener(var: Any):
    """
    Marks *var* as a possible event listener
    """

    listeners[var.__class__.__name__].append(var)
    return var


def event(*e: int, **kwargs):
    """
    Decorator for event functions
    """

    def decorator(func: Callable[[Any, pygame.event.Event], Any]):
        global events
        for _event in e:
            events[_event].append((kwargs, func))

        return func

    return decorator


def handle_events(app):
    """
    Process pending events
    """
    for _event in pygame.event.get():
        app.gui_manager.process_events(_event)

        for _filter, fun in events[_event.type]:
            if _filter.items() <= _event.dict.items():
                for _type in listeners[fun.__qualname__.split(".")[0]]:
                    fun(_type, _event)
