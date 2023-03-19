from fastapi import APIRouter
from endpoints import users, login, posts, likes, analytics

api_router = APIRouter()

api_router.include_router(login.router, tags=['Login'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(posts.router, prefix='/posts', tags=['Posts'])
api_router.include_router(likes.router, prefix='/likes', tags=['Likes'])
api_router.include_router(analytics.router, prefix='/analytics', tags=['Analytics'])
