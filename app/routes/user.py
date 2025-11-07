from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user import create_user
from app.core.jwt_config import get_curent_user

user_router = APIRouter(
    prefix="/users"
)

@user_router.post("/create")
def crete_user(user_data:UserCreate,db: Session = Depends(get_db)):
    return create_user(user_data,db)
    