from typing import Union

from app.db.models import JournalModel
from pydantic import BaseModel

from . import pydantic_model_creator
from .common_models import ApiBaseResponse

NewJournalModel_Pydantic = pydantic_model_creator(
    JournalModel,
    name="NewJournalCreated",
    exclude=(
        "pages",
        "author.my_challenges",
        "author.journals",
        "challenge.participants",
        "reward",
    ),
)
PrivateJournal_Pydantic = pydantic_model_creator(
    JournalModel,
    name="PrivateJournal",
    exclude=(
        "author",
        "author_id",
        "challenge.created_by",
        "challenge.description",
        "challenge.participants",
        "pages",
        "reward",
    ),
)


class PrivateJournalResponse(ApiBaseResponse):
    data: Union[PrivateJournal_Pydantic, NewJournalModel_Pydantic]


class NewJournalCreatedResponse(ApiBaseResponse):
    data: NewJournalModel_Pydantic





class CloneChallenge(BaseModel):
    # TODO
    pass
