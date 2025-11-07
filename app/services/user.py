from fastapi import HTTPException,status
from app.db import models
from app.schemas.user import UserCreateResponse
from app.utils.hash import hash_user_password


def create_user(user_data,db):
    
    # check for current user is exist 
    user_find_query = db.query(models.User).filter(models.User.email == user_data.email)
    is_user_exist = user_find_query.first()

    # Raise Error if user already exist
    if is_user_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User Already Exist!")
    
    # Hash password before save 
    user_data.password = hash_user_password(user_data.password)

    # Create Database User Object
    new_user = models.User(**user_data.model_dump())

    # Add User 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "msg" : "User Created Successfully!",
        "status" : status.HTTP_201_CREATED,
        "data" : UserCreateResponse.model_validate(new_user)
    }
    