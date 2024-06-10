import logging

from asyncio import CancelledError
from typing import Callable, Coroutine

from .room import Room
from .utils import Sub

logger = logging.getLogger(__name__)

callback = Callable[[dict, Room], Coroutine]

class Subsystem:
    """
    This can be bound to a room
    """
    def __init__(self, name="Subsystem"):
        self.typed_callbacks: dict[str, callback] = dict()
        self.all_callbacks: set[callback] = set()
        self.name = name

        self.event_callbacks: dict[object, Callable] = dict()

    def on(self, message_type: str):
        def decorator(func: callback):
            self.typed_callbacks[message_type] = func
            return func
        return decorator

    def all(self, func: callback):
        self.all_callbacks.add(func)
        return func
        
    async def bind(self, room: Room):
        try:
            with Sub(room.messages) as queue:
                while True:
                    message = await queue.get()
                    if "type" not in message:
                        continue
                    message_type = message["type"]

                    if message_type in self.typed_callbacks:
                        try:
                            func = self.typed_callbacks[message["type"]]
                            await func(message, room)
                        except Exception:
                            logger.exception("")

                    for func in self.all_callbacks:
                        try:
                            await func(message, room)
                        except Exception:
                            logger.exception("")

        except CancelledError:
            raise

