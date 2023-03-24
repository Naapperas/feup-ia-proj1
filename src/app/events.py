from collections import defaultdict
from typing import Callable, Any
import pygame

events: defaultdict[
    int, list[tuple[dict, Callable[[Any, pygame.event.Event], Any]]]
] = defaultdict(list)

listeners: defaultdict[str, list[Any]] = defaultdict(list)


def listener(var: Any):
    listeners[var.__class__.__name__].append(var)
    return var


def event(*e: int, **kwargs):
    """
    Decorator for event functions
    """

    def decorator(func: Callable[[Any, pygame.event.Event], Any]):
        global events
        for event in e:
            events[event].append((kwargs, func))

        return func

    return decorator


def handle_events(app):
    """
    Process pending events
    """
    for event in pygame.event.get():
        app.gui_manager.process_events(event)

        for filter, fun in events[event.type]:
            if filter.items() <= event.dict.items():
                for type in listeners[fun.__qualname__.split(".")[0]]:
                    fun(type, event)
