import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "event_pipeline.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
