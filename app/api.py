from fastapi import APIRouter
from app.user.router import router as user
from app.store.router import router as store
from app.review.router import router as review
from app.favorite.router import router as favorite
from app.like.router import router as like

router = APIRouter()

router.include_router(user, tags=["users"])
router.include_router(store, prefix="/store", tags=["stores"])
router.include_router(review, prefix="/review", tags=["reviews"])
router.include_router(favorite, prefix="/favorite", tags=["favorite"])
router.include_router(like, prefix="/like", tags=["like"])