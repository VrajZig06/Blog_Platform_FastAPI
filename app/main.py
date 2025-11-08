import os 
import sys

# Add File Path to System Variables
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from fastapi import FastAPI

from app.db import session,base
from app.routes.user import user_router
from app.routes.auth import auth_router
from app.routes.blog import blog_router

# Create Fast API App
app = FastAPI()

# Create All Tables if Not created in database
base.Base.metadata.create_all(bind=session.engine)

# Add Routers
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(blog_router)
