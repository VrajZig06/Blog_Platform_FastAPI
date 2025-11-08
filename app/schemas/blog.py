from pydantic import BaseModel,Field,ConfigDict
from typing import Optional


class BlogCreate(BaseModel):
  title: str = Field(...,description="Blog Title")
  description : str = Field(default=None,description="Blog Description")
  tags : list = Field(default=list(),description="This is list of tags")

class BlogQueryParams(BaseModel):
  search : Optional[str] = None
  skip : Optional[int] = 0
  limit : Optional[int] = 10 

class AuthorData(BaseModel):
  id:str
  email : str

  model_config = ConfigDict(from_attributes=True)

class BlogListResponse(BaseModel):
  id: str
  title : str
  description : str
  tags : list
  owner : AuthorData

  model_config = ConfigDict(from_attributes=True)

class BlogCreateResponse(BaseModel):
  id:str
  title : str
  description : Optional[str] = None 
  tags : list

  model_config = ConfigDict(from_attributes=True)


class BlogUpdate(BaseModel):
  title:Optional[str] = None
  description : Optional[str] = None
  tags : Optional[list[str]] = None

  model_config = ConfigDict(from_attributes=True)

