import time
from collections import defaultdict


class Metrics:
    def __init__(self):
        self.counters = defaultdict(int)
        self.last_log = time.time()

    def inc(self, key: str, value: int = 1):
        self.counters[key] += value

    def maybe_log(self, interval: int):
        now = time.time()
        if now - self.last_log >= interval:
            print("📊 METRICS")
            for k, v in self.counters.items():
                print(f"  {k}: {v}")
            print("-" * 30)
            self.last_log = now