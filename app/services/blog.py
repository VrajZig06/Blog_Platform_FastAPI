from app.db import models
from app.schemas.response import APIResponse,Pagination
from fastapi import status,HTTPException
from app.schemas.blog import BlogCreateResponse,BlogListResponse
from app.utils.cloudinary import upload_file_to_cloudinary



def create_blog(blog_data,db,current_user):
    new_blog = models.Blog(**blog_data.model_dump(),author_id=current_user.get('id'))

    # Add To Database
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return APIResponse(
       msg="Blog Created Successfully!",
       status=status.HTTP_201_CREATED,
       data = BlogCreateResponse.model_validate(new_blog)
    )

# Update Blog
def update_blog(blog_id,new_blog_data,db,current_user):
  
  # Check Blog Exist with given Blog id
  blog_exist_query = db.query(models.Blog).filter(models.Blog.id == blog_id)

  blog = blog_exist_query.first()

  if not blog:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog Not Found!!")

  if blog.author_id != current_user.get("id"):
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not Authorize to Update this Blog!")
  
  # Update fields dynamically
  for key, value in new_blog_data.model_dump(exclude_unset=True).items():
      setattr(blog, key, value)
  
  db.commit()
  db.refresh(blog)

  return APIResponse(
     msg="Blog Updated Successfully!",
     status=status.HTTP_200_OK,
     data=BlogCreateResponse.model_validate(blog)
  )

def get_blog_by_id(blog_id,db,current_user):
   # Check Blog Exist with given Blog id
   blog_exist_query = db.query(models.Blog).filter(models.Blog.id == blog_id)

   blog = blog_exist_query.first()

   if not blog:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog Not Found!!")
   
   return APIResponse(
      msg="Blog Fetched Successfully with given Blog Id!!",
      status= status.HTTP_200_OK,
      data=BlogListResponse.model_validate(blog)
   )



def delete_blog(blog_id,db,current_user):
   # Check Blog Exist with given Blog id
   blog_exist_query = db.query(models.Blog).filter(models.Blog.id == blog_id)

   blog = blog_exist_query.first()

   if not blog:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog Not Found!!")

   if blog.author_id != current_user.get("id"):
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not Authorize to Update this Blog!")
   
   blog_exist_query.delete()
   db.commit()

   return APIResponse(
      msg="Blog Deleted Successfully!",
      status=status.HTTP_200_OK,
      data= None
   )


def get_all_blogs(blog_query,db):
  
  # Base Query
  blogs_query = db.query(models.Blog)
  total_blogs = blogs_query.count()

  # Apply search filter (if any)
  if blog_query.search:
      blog_search_text = f"%{blog_query.search}%"
      blogs_query = blogs_query.filter(models.Blog.title.ilike(blog_search_text))

  # Apply pagination
  blogs_query = blogs_query.limit(blog_query.limit).offset(blog_query.skip)

  # Fetch all blogs
  blogs = blogs_query.all()

  # Map ORM objects -> Pydantic response
  blog_responses = [BlogListResponse.model_validate(blog) for blog in blogs]

  return APIResponse(
    msg= "All Blogs Fetched Successfully!",
    status=status.HTTP_200_OK,
    data=blog_responses,
    pagination=Pagination(total=total_blogs,limit=blog_query.limit,skip=blog_query.skip)
  )
  
  
def update_blog_image(blog_id,db,current_user,file):
   
  # Check Blog Exist with given Blog id
  blog_exist_query = db.query(models.Blog).filter(models.Blog.id == blog_id)

  blog = blog_exist_query.first()

  if not blog:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog Not Found!!")

  if blog.author_id != current_user.get("id"):
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not Authorize to Update this Blog!")
  
  image_url = upload_file_to_cloudinary(file)

  blog.image_url = image_url

  db.commit()
  db.refresh(blog)
  return APIResponse(
     msg="Blog Image Updated Successfully!",
     status=status.HTTP_200_OK,
     data=BlogCreateResponse.model_validate(blog)
  )
  

   