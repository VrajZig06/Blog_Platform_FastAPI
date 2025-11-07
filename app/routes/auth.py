from fastapi import APIRouter,status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import LoginData,TokenData
from app.schemas.response import APIResponse
from app.db import models
from app.utils.hash import verify_user_password
from app.core.jwt_config import create_access_token

auth_router = APIRouter(
    prefix="/auth"
)

@auth_router.post("/login")
def login_user(login_data:LoginData,db:Session = Depends(get_db)):
    
    user_query = db.query(models.User).filter(models.User.email == login_data.email)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found!")
    
    is_password_correct = verify_user_password(login_data.password,user.password)

    if not is_password_correct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Credentials are Wrong!!")
    
    payload = {
        "id" : user.id,
        "type" : user.user_type,
        "email" : user.email
    }
    
    # Create Access Token for Above Paylaod
    access_token = create_access_token(payload)
    
    return APIResponse(
        msg="User Logged in Successfully!!",
        status=status.HTTP_200_OK,
        data=TokenData(access_token=access_token,token_type="bearer")
    )