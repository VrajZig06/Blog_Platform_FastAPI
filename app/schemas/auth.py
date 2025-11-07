from pydantic import BaseModel,EmailStr

class LoginData(BaseModel):
    email : EmailStr
    password : str

class TokenData(BaseModel):
    access_token : str
    token_type : str