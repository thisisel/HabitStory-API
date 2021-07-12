from typing import Dict
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse


class NotAllowed(HTTPException):
    def __init__(self, allowed_methods: Dict, category: str, message: str = "Method not allowed"):
        super().__init__(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.allowed_methods: dict = allowed_methods
        self.category: str = category
        self.status: bool = False
        self.message: str = message


async def notallowed_error_handler(_: Request, exc: NotAllowed) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        content={
            "status": exc.status,
            "category": exc.category,
            "message": exc.message,
        },
        headers=exc.allowed_methods,
    )
