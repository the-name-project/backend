from sqlmodel import Session
from app.base import Service

from app.review.model import Review, ReviewCreate, ReviewUpdate


class ReviewService(Service[Review, ReviewCreate, ReviewUpdate]):
    def review_store(self,
                     session: Session,
                     *,
                     object_data: ReviewCreate,
                     store_id: int,
                     user_id: int
                     ) -> Review:
        review_data = object_data.dict(exclude_unset=True)

        review = Review(
            **review_data,
            store_id=store_id,
            user_id=user_id,
        )

        session.add(review)
        session.commit()
        session.refresh(review)
        return review


service = ReviewService(Review)

