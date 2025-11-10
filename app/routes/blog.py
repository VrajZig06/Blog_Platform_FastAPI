from fastapi import APIRouter, Depends, Query, Form, UploadFile,File
from app.core.jwt_config import get_curent_user
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.db import models
from app.schemas.blog import BlogCreate,BlogQueryParams,BlogUpdate
from app.services import blog
from typing import Annotated
from app.utils.cloudinary import upload_file_to_cloudinary

blog_router = APIRouter(
  prefix="/blogs"
)

@blog_router.get("/")
def get_blogs(blog_query : Annotated[BlogQueryParams , Query()],db:Session = Depends(get_db),current_user = Depends(get_curent_user)):
  return blog.get_all_blogs(blog_query,db)

@blog_router.post("/")
def create_blog(file : UploadFile = File(default=None),title = Form(...),description= Form(...),tags = Form(...), db:Session = Depends(get_db),current_user = Depends(get_curent_user)):

  tag_list = tags.split("#")
  image_url = upload_file_to_cloudinary(file) 
  blog_data = BlogCreate(title=title,description=description,tags=tag_list,image_url = image_url)
  return blog.create_blog(blog_data=blog_data,db=db,current_user=current_user)

@blog_router.patch("/{blog_id}")
def update_blog(blog_id:str,new_blog_data:BlogUpdate,db:Session=Depends(get_db),current_user = Depends(get_curent_user)):
  return blog.update_blog(blog_id,new_blog_data,db,current_user)

@blog_router.delete("/{blog_id}")
def delete_blog(blog_id:str,db:Session=Depends(get_db),current_user= Depends(get_curent_user)):
  return blog.delete_blog(blog_id=blog_id,db=db,current_user=current_user)
  
@blog_router.get("/{blog_id}")
def get_blog(blog_id:str,db:Session=Depends(get_db),current_user= Depends(get_curent_user)):
  return blog.get_blog_by_id(blog_id,db,current_user)

@blog_router.patch("/update-image/{blog_id}/")
def update_blog_image(blog_id,db:Session = Depends(get_db),current_user = Depends(get_curent_user),file: UploadFile = File(None)):
  return blog.update_blog_image(blog_id=blog_id,db=db,current_user=current_user,file= file)