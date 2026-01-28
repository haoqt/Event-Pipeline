import time


class RateLimiter:
    def __init__(self, rate_per_sec):
        self.rate = rate_per_sec
        self.allowance = rate_per_sec
        self.last_check = time.time()

    def allow(self):
        now = time.time()
        elapsed = now - self.last_check
        self.last_check = now

        self.allowance += elapsed * self.rate
        if self.allowance > self.rate:
            self.allowance = self.rate

        if self.allowance < 1:
            return False

        self.allowance -= 1
        return True