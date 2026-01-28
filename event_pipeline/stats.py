class WorkerStats:
    __slots__ = ("count", "error", "latency_sum")

    def __init__(self):
        self.count = 0
        self.error = 0
        self.latency_sum = 0.0

    def update(self, event):
        self.count += 1
        if event.status >= 500:
            self.error += 1
        self.latency_sum += event.latency

    def snapshot_and_reset(self):
        snap = (self.count, self.error, self.latency_sum)
        self.count = 0
        self.error = 0
        self.latency_sum = 0.0
        return snap