from pydantic import BaseModel, EmailStr
from typing import Any, Dict, List, Optional


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Optional[Dict[str, Any]]

