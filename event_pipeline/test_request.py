import asyncio
import httpx
import time

# Cấu hình
URL = "http://localhost:8000/ingest"
TOTAL_REQUESTS = 1_000_000
CONCURRENCY = 200  # Số lượng request gửi đồng thời (điều chỉnh tùy sức mạnh CPU)
BATCH_SIZE = 1000  # Cập nhật tiến độ sau mỗi 1000 requests


async def send_request(client, semaphore):
    payload = {
        "endpoint": "/events",
        "status": 200,
        "latency_ms": 123
    }

    async with semaphore:  # Giới hạn số lượng request đồng thời
        try:
            response = await client.post(URL, json=payload, timeout=10.0)
            return response.status_code
        except Exception as e:
            return None


async def main():
    # Semaphore giúp kiểm soát concurrency để không làm sập OS socket
    semaphore = asyncio.Semaphore(CONCURRENCY)

    limits = httpx.Limits(max_keepalive_connections=CONCURRENCY, max_connections=CONCURRENCY)

    async with httpx.AsyncClient(limits=limits) as client:
        start_time = time.time()
        tasks = []
        completed = 0

        print(f"🚀 Bắt đầu gửi {TOTAL_REQUESTS} requests tới {URL}...")

        for i in range(1, TOTAL_REQUESTS + 1):
            tasks.append(send_request(client, semaphore))

            # Khi gom đủ 1 đợt hoặc đến cuối cùng
            if len(tasks) >= CONCURRENCY or i == TOTAL_REQUESTS:
                results = await asyncio.gather(*tasks)
                tasks = []
                completed += len(results)

                if completed % BATCH_SIZE == 0:
                    elapsed = time.time() - start_time
                    rps = completed / elapsed
                    print(f"✅ Đã xong: {completed}/{TOTAL_REQUESTS} | Tốc độ: {rps:.2f} req/sec")

        end_time = time.time()
        total_duration = end_time - start_time
        print("-" * 30)
        print(f"🏁 Hoàn thành 1 triệu request trong {total_duration:.2f} giây")
        print(f"📊 Tốc độ trung bình: {TOTAL_REQUESTS / total_duration:.2f} req/sec")


if __name__ == "__main__":
    asyncio.run(main())
