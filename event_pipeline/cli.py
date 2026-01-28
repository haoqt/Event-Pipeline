from event_pipeline.queue import BoundedQueue
from event_pipeline.producer import generate_event
from event_pipeline.consumer import CounterConsumer
import psutil, os

def main():
    queue = BoundedQueue(max_size=100_000)
    consumer = CounterConsumer()

    TOTAL = 1000000

    for _ in range(TOTAL):
        event = generate_event()
        queue.put(event)

        ev = queue.get()
        if ev:
            consumer.process(ev)
    p = psutil.Process(os.getpid())
    print("RSS MB:", p.memory_info().rss / 1024 / 1024)
    print("Processed:", consumer.count)
    print("Dropped:", queue.dropped)
    print("Queue size:", queue.size())


if __name__ == "__main__":
    main()
