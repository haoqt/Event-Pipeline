from event_pipeline.ingest.server import queue
from event_pipeline.consumer import CounterConsumer
import time
import psutil, os

consumer = CounterConsumer()

def run():
    while True:
        ev = queue.get()
        if ev:
            consumer.process(ev)
        else:
            time.sleep(0.001)
