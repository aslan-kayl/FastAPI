

from src.db.models import Review
from src.auth.servise import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi import status
from .schemas import ReviewCreateModel
from sqlmodel import desc, select
import logging
from src.errors import ReviewNotFound


book_service = BookService()
user_service = UserService()

class ReviewService:

    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session:AsyncSession,
    ):
        try:
            book = await book_service.get_book(book_uid = book_uid, session = session)
            user = await user_service.get_user_by_email(email = user_email, session = session)
            review_data_dict = review_data.model_dump()

            if not book:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            new_review = Review(user=user, book=book,**review_data_dict)

            session.add(new_review)

            await session.commit()

            return new_review

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops ... something went wrong"
            )


    async def get_review(self, review_uid: str, session:AsyncSession):

        statement = select(Review).where(Review.uid == review_uid)

        result = await session.exec(statement)

        return result.first()

    async def get_all_reviews(self, session:AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))

        result = await session.exec(statement)

        return result.all()

    async def delete_reviews_to_from_book(self, review_uid: str, user_email: str, session:AsyncSession):
        user = await user_service.get_user_by_email(user_email, session)

        review = await self.get_review(review_uid, session)

        if not review or (review.user != user):
            raise HTTPException(
                detail="Cannot delete this review.",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        await session.delete(review)

        await session.commit()

    async def update_review(self, review_uid: str, review_update_data: ReviewCreateModel, session: AsyncSession):

        review = await self.get_review(review_uid, session)

        if not review:
            raise ReviewNotFound()

        update_data_dict = review_update_data.model_dump()

        for key, value in update_data_dict.items():
            setattr(review, key, value)

            await session.commit()

            await session.refresh(review)

        return review

    async def delete_review(self, review_uid: str, session:AsyncSession):

        review = await self.get_review(review_uid, session)

        if not review:
            raise ReviewNotFound()

        await session.delete(review)

        await session.commit()
