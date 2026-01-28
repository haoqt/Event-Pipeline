class CounterConsumer:
    def __init__(self):
        self.count = 0

    def process(self, event):
        self.count += 1
