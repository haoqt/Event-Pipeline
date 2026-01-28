from enum import Enum
import random

class Policy(Enum):
    DROP = "drop"
    SAMPLE = "sample"
    SHED = "shed"

class BackpressureController:
    def __init__(self, policy, sample_rate=1.0):
        self.policy = policy
        self.sample_rate = sample_rate

    def should_accept(self, queue_usage: float, event) -> bool:
        if queue_usage < 0.8:
            return True

        if self.policy == Policy.DROP:
            return False

        if self.policy == Policy.SAMPLE:
            return random.random() < self.sample_rate

        if self.policy == Policy.SHED:
            return event.priority >= event.HIGH

        return True