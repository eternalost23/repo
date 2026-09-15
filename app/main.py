import logging
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routers.categories import router as category_router
from app.api.routers.task import router as task_router
from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.core.logging import configure_logging

configure_logging()

app = FastAPI()


logger = logging.getLogger("app.middleware")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
request_count: int = 0


@app.middleware("http")  # log_requests выполнится до и после обработки каждого HTTP-запроса
async def log_requests(request: Request, call_next) -> Response:
    started_at = perf_counter()
    try:
        response: Response = await call_next(request)  # Работа самого эндпоинта
    except Exception:
        duration_ms = (perf_counter() - started_at) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started_at) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


@app.middleware("http")
async def log_requests_counter(request: Request, call_next) -> Response:
    global request_count
    request_count += 1
    response: Response = await call_next(request)
    response.headers["X-Request-Number"] = str(request_count)
    return response


@app.exception_handler(NotFoundError)
def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(router=task_router)
app.include_router(router=category_router)
