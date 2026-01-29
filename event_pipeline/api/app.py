import asyncio
from fastapi import FastAPI
from pydantic import BaseModel


from event_pipeline.pipeline.producer import produce
from event_pipeline.pipeline.worker import Worker
from event_pipeline.registry import registry


app = FastAPI(title="Event Pipeline API")
queue: asyncio.Queue = asyncio.Queue()
worker = Worker(queue)


class EventIn(BaseModel):
    type: str
    payload: dict


@app.on_event("startup")
async def startup():
    asyncio.create_task(worker.run())

@app.post("/events")
async def create_event(data: EventIn):
    event = produce(data.type, data.payload)
    await queue.put(event)
    return {"status": "queued", "event_id": event.id}

@app.get("/events")
def list_events():
    return registry.all()
