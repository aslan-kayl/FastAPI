from fastapi import APIRouter, Depends
from src.db.models import User, Review
from src.db.main import get_session
from src.auth.dependecies import get_current_user, AccessTokenBearer
from sqlmodel.ext.asyncio.session import AsyncSession
from src.reviews.schemas import ReviewCreateModel, ReviewModel
from .service import ReviewService


review_service = ReviewService()
review_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@review_router.get("/")
async def get_all_reviews(session: AsyncSession = Depends(get_session), _: dict = Depends(access_token_bearer)):
    reviews = await review_service.get_all_reviews(session=session)
    return reviews

@review_router.post('/book/{book_uid}')
async def add_review_to_books(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user:User =Depends(get_current_user),
    session:AsyncSession = Depends(get_session)
):

    new_review = await review_service.add_review_to_book(
        user_email= current_user.email,
        review_data=review_data,
        book_uid=book_uid,
        session=session,
    )

    return new_review

@review_router.get('/{review_uid}')
async def get_review_uid(
        review_uid: str,
        session: AsyncSession = Depends(get_session),
        _: dict = Depends(access_token_bearer)
):

    review = await review_service.get_review(review_uid=review_uid, session=session)

    return review

@review_router.patch('/{review_uid}')
async def update_review(
        review_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession = Depends(get_session),):

    update_review = await review_service.update_review(
        review_uid=review_uid,
        review_update_data=review_data ,
        session=session
    )
    return update_review

@review_router.delete('/{review_uid}')
async def delete_review(
        review_uid: str, session: AsyncSession = Depends(get_session),
        _: dict = Depends(access_token_bearer)
):
    await review_service.delete_review(review_uid=review_uid, session=session)

    return {}
