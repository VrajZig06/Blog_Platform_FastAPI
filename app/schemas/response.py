from pydantic import BaseModel,Field
from typing import Annotated
from app.schemas.user import UserCreate

class APIResponse(BaseModel):
    msg : str = Field(max_length=100,description="This is Message for API Response")
    status : str
    data : UserCreate
    
    class config:
        orm_mode = True
    
