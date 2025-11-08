from app.db.base import Base
from sqlalchemy import Integer,Column,String,Text,Enum,TIMESTAMP,text
from enum import Enum as PyEnum
import uuid

class UserType(str,PyEnum):
    ADMIN = "admin"
    AUTHOR = "author"
    READER = "reader"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String,default=lambda:str(uuid.uuid4()),primary_key=True,nullable=False)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    age = Column(Integer,nullable=False)
    gender = Column(String,nullable=False)
    profile_photo = Column(Text,nullable=True)  
    user_type = Column(Enum(UserType), nullable=False, default=UserType.READER)
    
    created_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default=text("CURRENT_TIMESTAMP"))

