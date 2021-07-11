from app.api.errors.error_categories import PAGE_404
from app.api.errors.not_found_error import NotFound
from app.schemas.common_models import ApiBaseResponse, ApiErrorResponse
from app.crud.journal import RetriveJournal
from tortoise.fields import data
from app.crud.page import CreatePage, RetrivePage

from app.schemas.page import (
    AddPage,
    JournalPageAddedResponse,
    PageInList_Pydantic,
    SingleJournalPage,
    SingleJournalPageResponse,
)
from app.schemas.user import UserDB
from fastapi import Body, Depends, Path, Response, status
from fastapi.routing import APIRouter
from fastapi_pagination import paginate, Page, Params

from .dependencies import PageFilters, current_active_user

router = APIRouter()


@router.get("/{id}/pages", responses={200: {"model": Page[PageInList_Pydantic]}})
async def retrive_journal_pages(
    id: int = Path(..., description="journal id"),
    page_filters: PageFilters = Depends(),
    params: Params = Depends(),
    user: UserDB = Depends(current_active_user),
):
    pages_qset = await RetrivePage.fetch_all_journal_pages(journal_id=id)

    return paginate(await PageInList_Pydantic.from_queryset(pages_qset), params=params)


@router.post(
    "/{id}/pages",
    status_code=201,
    response_description="Page added",
    responses={201: {"model": JournalPageAddedResponse}},
)
async def add_page(
    response: Response,
    id: int = Path(..., description="journal id"),
    body: AddPage = Body(...),
    user: UserDB = Depends(current_active_user),
):

    if await RetriveJournal.journal_is_over():

        response.status_code = status.HTTP_200_OK
        return ApiBaseResponse(status=False, message="Journal is over")

    return await CreatePage.add_new_page(data=body, journal_id=id, author_id=user.id)


# TODO story
@router.get(
    "/{id}/pages/{page_id}",
    responses={
        200: {"model": SingleJournalPageResponse},
        404: {"model": ApiErrorResponse},
    },
)
async def retrieve_journal_single_page(
    id: int = Path(..., description="journal id"),
    page_id: int = Path(..., description="page id"),
    user: UserDB = Depends(current_active_user),
):
    page_qset = await RetrivePage.fetch_single_page(journal_id=id, page_id=page_id)

    if not (page := await page_qset):
        raise NotFound(category=PAGE_404)

    page_data = await SingleJournalPage.from_tortoise_orm(page)

    return SingleJournalPageResponse(
        status=True, message="Page retrived Successfully", data=page_data
    )


# TODO
@router.patch(
    "/{id}/pages/{page_id}",
    status_code=200,
    response_description="Page updated",
    responses={200: {"model": JournalPageAddedResponse}},
)
async def update_page_note(
    id: int = Path(..., description="journal id"),
    body: AddPage = Body(...),
    page_id: int = Path(..., description="page id"),
    user: UserDB = Depends(current_active_user),
):
    pass
