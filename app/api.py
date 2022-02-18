from fastapi import APIRouter
from app.user.router import router as user
from app.store.store_service import router as store
from app.test.dummy.favorite_dummy import router as favorite
from app.test.dummy.review_dummy import router as review
from app.test.dummy.user_dummy import router as user_dummy

router = APIRouter()

router.include_router(user, prefix="/users", tags=["users"])
router.include_router(store, prefix="/store", tags=["stores"])
router.include_router(favorite)
router.include_router(review)
router.include_router(user_dummy)
