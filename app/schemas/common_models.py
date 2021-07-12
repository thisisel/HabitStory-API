from typing import List, Optional
from pydantic import BaseModel


class ApiBaseResponse(BaseModel):
    status: bool
    message: str


# TODO Document example for 500 and 404
class ApiErrorResponse(BaseModel):
    status: bool = False
    category: str
    message: Optional[str]


class CreateUpdateDictModel(BaseModel):
    def create_dict(self):
        return self.dict(
            exclude_unset=True,  # exclude pydantic model default fields
            exclude=("id"),  # exclude db generated or db default fields
        )
