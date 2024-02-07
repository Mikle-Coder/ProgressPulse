import asyncio
from datetime import datetime
from typing import Callable


class TaskTimer:
    def __init__(self, max_period_seconds=3*60*60, call_func: Callable[[int], None] = None) -> None:
        self.cache = {}
        self.max_period_seconds = max_period_seconds
        self.call_func = call_func

    async def add_task(self, task_id: int, started_at: datetime):
        self.cache[task_id] = started_at

    async def remove_task(self, task_id: int):
        self.cache.pop(task_id, None)

    async def check_timeout(self, interval_seconds=59):
        while True:
            await asyncio.sleep(interval_seconds)
            await self._process_timeouts()

    async def _process_timeouts(self):
        now = datetime.utcnow()
        tasks_to_remove = []

        for task_id, started_at in self.cache.items():
            elapsed_seconds = (now - started_at).total_seconds()

            if elapsed_seconds > self.max_period_seconds:
                tasks_to_remove.append(task_id)
                if self.call_func:
                    await self.call_func(task_id)

        for task_id in tasks_to_remove:
            self.cache.pop(task_id, None)


task_timer = TaskTimer()
