import os
import subprocess
import sys


def num_workers() -> str:
    if "WEB_CONCURRENCY" in os.environ:
        return os.environ["WEB_CONCURRENCY"]
    try:
        n = (
            len(os.sched_getaffinity(0))
            if hasattr(os, "sched_getaffinity")
            else os.cpu_count() or 1
        )
        return str(max(1, 2 * n + 1))
    except Exception:
        return "1"


workers = num_workers()

subprocess.run(
    [
        sys.executable,
        "-m",
        "gunicorn",
        "src.server:app",
        "-w",
        workers,
        "-k",
        "uvicorn.workers.UvicornWorker",
        "--bind",
        "0.0.0.0:3000",
    ]
)
