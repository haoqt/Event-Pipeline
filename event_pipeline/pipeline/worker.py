import asyncio
from event_pipeline.pipeline.processor import process
from event_pipeline.pipeline.reducer import reduce


class Worker:
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    async def run(self):
        while True:
            event = await self.queue.get()
            processed = process(event)
            reduce(processed)
            self.queue.task_done()
