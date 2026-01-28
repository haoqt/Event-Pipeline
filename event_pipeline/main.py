from multiprocessing import Process
from event_pipeline.queues import WORKER_QUEUES
from event_pipeline.worker import worker_loop
from event_pipeline.ingest.server import app as fastapi_app
import uvicorn

def start_workers():
    processes = []
    for i, q in enumerate(WORKER_QUEUES):
        p = Process(target=worker_loop, args=(q, i))
        p.start()
        processes.append(p)
    return processes

if __name__ == "__main__":
    workers = start_workers()
    print(f"{len(workers)} workers started.")

    print("Starting API Server on http://0.0.0.0:8000")
    try:
        uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
    finally:
        for q in WORKER_QUEUES:
            q.put(None)

        for p in workers:
            p.join()