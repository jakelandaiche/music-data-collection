import asyncio

class Hub:
    def __init__(self):
        self.subscriptions = set()

    def pub(self, message):
        for queue in self.subscriptions:
            queue.put_nowait(message)

class Sub:
    def __init__(self, hub):
        self.hub = hub
        self.queue = asyncio.Queue()

    def __enter__(self):
        self.hub.subscriptions.add(self.queue)
        return self.queue 

    def __exit__(self, type, value, traceback):
        self.hub.subscriptions.remove(self.queue)

seed = 68648
i = 0

def generate_code():
    """Basic linear congruential generator"""
    global i 
    n = seed + 41055 * i 
    i += 1 
    g = [7, 5, 15, 19]
    d = []
    for _ in range(4):
        d.append(int(n % 26))
        n //= 26 
    return ''.join(chr(((g[i]*d[i]) % 26) + 65) for i in range(4))


import json
from websockets.server import WebSocketServerProtocol as Socket
async def send(websocket: Socket, message: dict):
    await websocket.send(json.dumps(message))

from typing import Callable, Coroutine
def anonymous_task(f: Callable[..., Coroutine]) -> asyncio.Task:
    return asyncio.create_task(f())
