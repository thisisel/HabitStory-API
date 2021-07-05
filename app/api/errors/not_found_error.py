from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse


class NotFound(HTTPException):
    def __init__(self, category: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND)
        self.category: str = category
        self.status: bool = False
        self.message: str = "Not Found"


# @app.exception_handler(NotFound)
async def notfound_error_handler(_: Request, exc: NotFound) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "status": exc.status,
            "category": exc.category,
            "message": exc.message,
        },
    )
