from fastapi import FastAPI
from pydantic import ValidationError
from starlette.responses import JSONResponse

from repetitor_backend.settings.app import app_settings
from repetitor_backend import api


def create_app(settings) -> FastAPI:
    """Create fastAPI app."""
    app = FastAPI(
        docs_url=f"{app_settings.URL_API_PREFIX}/docs"
        if not app_settings.is_prod()
        else None,
        openapi_url=f"{settings.URL_API_PREFIX}/openapi.json"
        if not app_settings.is_prod()
        else None,
    )
    app.include_router(api.router, prefix=settings.URL_API_PREFIX)

    async def http422_error_handler(_, exc) -> JSONResponse:
        return JSONResponse({"detail": exc.errors()}, status_code=422)

    app.add_exception_handler(ValidationError, http422_error_handler)
    return app


app = create_app(app_settings)
