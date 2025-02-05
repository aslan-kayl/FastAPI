from fastapi import APIRouter, status, Depends
from .schemas import Book, BookUpdateModel, BookCreateModel, BookDetailModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.errors import BookNotFound
from src.db.main import get_session
from typing import List
from src.auth.dependecies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin","user"]))


@book_router.get("/", response_model=List[Book], dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session), _: dict = Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book, dependencies=[role_checker])
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), token_details: dict=Depends(access_token_bearer)) -> dict:
    user_id = token_details.get('user')['user_uid']
    new_book = await book_service.create_book(book_data, user_id,session)
    return new_book


@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(book_uid: str, session:AsyncSession = Depends(get_session), token_details: dict=Depends(access_token_bearer)) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:

        raise BookNotFound()


@book_router.patch("/{book_uid}", response_model=Book, dependencies=[role_checker])
async def update_book(book_uid: str, book_update_data: BookUpdateModel, session:AsyncSession = Depends(get_session), token_details: dict=Depends(access_token_bearer)) -> dict:

    update_book = await book_service.update_book(book_uid, book_update_data, session)

    if update_book is None:
        raise BookNotFound()

    else:

        return update_book

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(book_uid: str, session:AsyncSession = Depends(get_session), token_details: dict=Depends(access_token_bearer)):
    book_to_delete = await book_service.delete_book(book_uid,session)

    if book_to_delete is None:
        raise BookNotFound()
    else:
       return {}
