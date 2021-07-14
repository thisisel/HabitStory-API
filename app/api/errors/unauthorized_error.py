from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse


class UnAuthorized(HTTPException):
    def __init__(self, category: str = "user_401", message: str = "User is not authorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED)
        self.category: str = category
        self.status: bool = False
        self.message: str = message


async def unauthorized_error_handler(_: Request, exc: UnAuthorized) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "status": exc.status,
            "category": exc.category,
            "message": exc.message,
        },
    )
