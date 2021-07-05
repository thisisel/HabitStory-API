from typing import Optional
from pydantic.main import BaseModel
from . import pydantic_model_creator
from app.db.models import PageModel
from .common_models import ApiBaseResponse

BasePage_Pydantic = pydantic_model_creator(
    PageModel, name="JournalPageBase", exclude=("journal",)
)

PageInList_Pydantic = pydantic_model_creator(
    PageModel,
    name="JournalPageList",
    exclude=(
        "note","journal", "journal_id",
    ),
    computed = ("page_url",)
)


class SingleJournalPage(BasePage_Pydantic):
    story: Optional[str]=None


class SingleJournalPageResponse(ApiBaseResponse):
    data: SingleJournalPage


class AddPage(BaseModel):
    journal_id: int
    note: str


class JournalPageAddedResponse(ApiBaseResponse):
    data: BasePage_Pydantic
