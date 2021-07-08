from fastapi_users.db import TortoiseBaseUserModel
from tortoise import fields, models
from tortoise.exceptions import NoValuesFetched
from tortoise.fields.base import CASCADE, RESTRICT, SET_NULL
from app.core.config import API_PREFIX


class UserModel(TortoiseBaseUserModel):

    username = fields.CharField(max_length=20, index=True, unique=True, null=False)
    joined_date = fields.DatetimeField(auto_now_add=True, null=False)

    my_challenges: fields.ReverseRelation["ChallengeModel"]
    journals: fields.ReverseRelation["JournalModel"]

    class Meta:
        app = "models"
        table = "users"

    class PydanticMeta:
        exclude = ("hashed_password", "is_active", "is_superuser", "is_verified", "joined_date",)


class RewardModel(models.Model):

    id = fields.IntField(pk=True)
    tag = fields.TextField()

    journals: fields.ReverseRelation["JournalModel"]

    class Meta:
        app = "models"
        table = "rewards"
        # abstract = True
    
    class PydanticMeta:
        exclude=("content",)


class StoryReward(RewardModel):

    author = fields.CharField(max_length=100)
    title = fields.CharField(max_length=100)
    content = fields.TextField()
    word_count = fields.IntField(null=True, index=True)

    pieces: fields.ReverseRelation["StoryPieceModel"]
    class Meta:
        app = "models"
        table = "stories"

    class PydanticMeta:
        exclude=("content",)


class StoryPieceModel(models.Model):
   
    id = fields.IntField(pk=True)
    content = fields.TextField(null=False)
    word_count = fields.IntField(null=False)
    piece_num = fields.IntField(null=False, index=True)


    story: fields.ForeignKeyRelation[StoryReward] = fields.ForeignKeyField(
        "models.StoryReward", related_name="pieces", on_delete=CASCADE
    ) 
    class Meta:
        app = "models"
        table = "story_pieces"
        unique_together = ("id", "piece_num",)
        ordering = ["story_id", "piece_num"]
        

class ChallengeModel(models.Model):

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=100, default="misc")
    description = fields.TextField()
    duration = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

    created_by: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        "models.UserModel", related_name="my_challenges", null=True, on_delete=SET_NULL
    )
    participants: fields.ReverseRelation["JournalModel"]

    def count_participants(self) -> int:
        """
        Computed total number of participants (hidden and public)
        """
        try:
            return len(self.participants)

        except NoValuesFetched:
            return 0

    class Meta:
        app = "models"
        table = "challenges"
    

class JournalModel(models.Model):

    id = fields.IntField(pk=True)
    is_public = fields.BooleanField(default=False)
    streak = fields.IntField(default=0)
    started = fields.DatetimeField(auto_now_add=True)
    finished = fields.DatetimeField(null=True)
    active = fields.BooleanField(default=True)
    last_modified = fields.DatetimeField(auto_now=True)

    author: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField(
        "models.UserModel", related_name="journals", on_delete=CASCADE
    )
    challenge: fields.ForeignKeyRelation[ChallengeModel] = fields.ForeignKeyField(
        "models.ChallengeModel", related_name="participants", on_delete=RESTRICT
    )
    reward: fields.ForeignKeyRelation[StoryReward] = fields.ForeignKeyField(
        "models.StoryReward", related_name="journals", on_delete=RESTRICT
    )

    pages: fields.ReverseRelation["PageModel"]

    def count_pages(self) -> int:
        """
        Computed total number of pages in this journal
        """
        try:
            return len(self.pages)

        except NoValuesFetched:
            return -1

    def journal_url(self) -> str:
        return f"{API_PREFIX}/profile/journals/{self.id}"
    
    #def count_remains(self) -> int:
    #     e = await self.challenge.

    class Meta:
        app = "models"
        table = "journals"
        unique_together = ("author", "challenge")
        ordering = ["last_modified"]

    #TODO move to pydantic models
    class PydanticMeta:
        computed = ("count_pages","journal_url")


class PageModel(models.Model):

    id = fields.IntField(pk=True)
    page_num = fields.IntField(null=False, default=0, index=True)
    submitted = fields.DatetimeField(auto_now_add=True, index=True)
    last_modified = fields.DatetimeField(auto_now=True)
    note = fields.TextField(null=True)

    journal: fields.ForeignKeyRelation[JournalModel] = fields.ForeignKeyField(
        "models.JournalModel", related_name="pages", on_delete=CASCADE
    )

    def page_url(self) -> str:
        try:
            return f"{API_PREFIX}/profile/journals/{self.journal.id}/pages/{self.id}"
        except AttributeError:
            print()


    class Meta:
        app = "models"
        table = "pages"
        ordering = ["journal_id", "submitted", "page_num"]