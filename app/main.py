import os 
import sys

# Add File Path to System Variables
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from fastapi import FastAPI

from app.db import session,base,models

# Create Fast API App
app = FastAPI()

# Create All Tables if Not created in database
base.Base.metadata.create_all(bind=session.engine)