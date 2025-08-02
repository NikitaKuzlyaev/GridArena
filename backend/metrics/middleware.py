from prometheus_client import Counter, Histogram, Summary
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Duration of HTTP requests",
    ["method", "path", "status_code"]
)

REQUEST_SUMMARY = Summary(
    "http_request_summary",
    "Duration of HTTP requests",
    ["method", "path", "status_code"]
)

import re


def normalize_path(path: str) -> str:
    # Заменим числовые ID
    path = re.sub(r"/\d+", "/:id", path)

    # Заменим UUID
    path = re.sub(r"/[0-9a-fA-F-]{36}", "/:uuid", path)

    # Можно добавить кастомные правила по своему API
    return path


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        method = request.method
        raw_path = request.url.path
        path = normalize_path(raw_path)
        status_code = str(response.status_code)

        #REQUEST_COUNT.labels(method=method, path=path, status_code=status_code).inc()
        #REQUEST_LATENCY.labels(method=method, path=path, status_code=status_code).observe(duration)
        REQUEST_SUMMARY.labels(method=method, path=path, status_code=status_code).observe(duration)

        return response
