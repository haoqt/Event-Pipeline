import time

def reducer_loop(in_queues):
    total_count = 0
    total_error = 0
    total_latency = 0.0

    while True:
        for q in in_queues:
            try:
                count, error, latency = q.get_nowait()
                total_count += count
                total_error += error
                total_latency += latency
            except:
                pass

        if total_count:
            print({
                "count": total_count,
                "error_rate": total_error / total_count,
                "avg_latency": total_latency / total_count,
            })

        time.sleep(1)