from pydantic import BaseModel,Field,ConfigDict
from typing import Annotated,Any
from app.schemas.user import UserCreate

class APIResponse(BaseModel):
    msg : str = Field(max_length=100,description="This is Message for API Response")
    status : int
    data : Any
    
    model_config = ConfigDict(from_attributes=True)
    
