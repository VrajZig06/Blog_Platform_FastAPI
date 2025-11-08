import os
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timezone,timedelta
from dotenv import load_dotenv
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))
    return encoded_jwt


def verify_token(token:str,credentials_exception):
    try:
        decoded_payload = jwt.decode(token,key=os.getenv('SECRET_KEY'),algorithms=os.getenv('ALGORITHM'))
    
        id = decoded_payload.get('id')
        email = decoded_payload.get('email')
        type  = decoded_payload.get('type')

        data = {
            "id" : id,
            "email" : email,
            "type" : type
        }

        if not id:
            raise credentials_exception
        
        return data   
    except InvalidTokenError:
        raise credentials_exception
        
        
def get_curent_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Credentials are not authenticated!")
    
    return  verify_token(token,credential_exception)

