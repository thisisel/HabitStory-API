from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse


class Forbidden(HTTPException):
    def __init__(self, category: str, message: str = "Forbidden request"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN)
        self.category: str = category
        self.status: bool = False
        self.message: str = message


# @app.exception_handler(NotFound)
async def forbidden_error_handler(_: Request, exc: Forbidden) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "status": exc.status,
            "category": exc.category,
            "message": exc.message,
        },
    )
