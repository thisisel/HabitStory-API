from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse


class InternalError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.status: bool = False
        self.message: str = "Internal server error"



# @app.exception_handler(InternalError)
async def internal_error_handler(_: Request, exc: InternalError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": exc.status, "message": exc.message},
    )
