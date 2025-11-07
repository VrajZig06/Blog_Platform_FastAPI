from pydantic import BaseModel, Field,EmailStr,ConfigDict
from typing import  Literal

class UserCreate(BaseModel):
    first_name : str = Field(description="This is First Name of User")
    last_name : str = Field(description="This is Last Name of User")
    email : EmailStr = Field(description="Email of User")
    password : str = Field(description="Hash Password")
    age : int = Field(gt=0,le=100,description="This is Age of User")
    gender : Literal['male','female','other'] = Field(description="Gender of User")
    profile_photo : str = Field(description="This is profile Photo of user",default=None)
    user_type : Literal['admin','author',"reader"] = Field(description="This is User Type")

    
class UserCreateResponse(BaseModel):
    id: str 
    first_name: str
    last_name : str
    email : str
    age : int
    gender : str
    user_type :str
    
    model_config = ConfigDict(from_attributes=True)
    

