import argparse

import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI Application with uvicorn")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes")
    args = parser.parse_args()

    uvicorn.run(
        "app.asgi:create_application",
        factory=True,
        host=args.host,
        port=args.port,
        workers=args.workers,
        log_config=None,
        log_level=None,
    )
