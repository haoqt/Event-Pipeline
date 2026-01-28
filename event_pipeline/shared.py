from event_pipeline.queue import BoundedQueue

# Khởi tạo duy nhất tại đây
queue = BoundedQueue(max_size=10)