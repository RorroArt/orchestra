import heapq
from dataclasses import dataclass, field
from itertools import count
from typing import Any

import trio


@dataclass(order=True)
class PriorityItem:
    priority: int
    index: int
    item: Any = field(compare=False)


class PriorityChannel:
    def __init__(self):
        self._heap = []
        self._counter = count()
        self._send, self._recv = trio.open_memory_channel(float("inf"))
        self._lock = trio.Lock()

    async def send(self, item: Any, priority: int = 0):
        async with self._lock:
            entry = PriorityItem(priority, next(self._counter), item)
            heapq.heappush(self._heap, entry)
        await self._send.send(None)

    async def receive(self) -> Any:
        await self._recv.receive()
        async with self._lock:
            return heapq.heappop(self._heap).item
