# Project 2 – High Throughput Event Pipeline

## Phases implemented
- Phase 0: Event model + bounded queue
- Phase 1: Ingest & validation
- Phase 2: Backpressure & drop strategy
- Phase 3: Process-based worker pool with partitioning

## Guarantees
- Streaming-first
- Memory bounded
- CPU scalable
- At-least-once-ish
- Kafka-ready design

## Next phases
- Phase 3.5: batching & tuning
- Phase 4: fault handling & snapshots
- Phase 5: benchmarking