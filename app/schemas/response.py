from pydantic import BaseModel,Field,ConfigDict
from typing import Annotated,Any,Optional
from app.schemas.user import UserCreate

class Pagination(BaseModel):
    total : int
    limit : int
    skip : int

class APIResponse(BaseModel):
    msg : str = Field(max_length=100,description="This is Message for API Response")
    status : int
    data : Any
    pagination : Optional[Pagination] = None
    
    model_config = ConfigDict(from_attributes=True)
    
