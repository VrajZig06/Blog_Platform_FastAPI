from app.db.base import Base
from sqlalchemy import Integer,Column,String,Text, JSON,ForeignKey,TIMESTAMP,text
from sqlalchemy.orm import relationship
import uuid

class Blog(Base):
  __tablename__ = "blogs"

  id = Column(String,default=lambda:str(uuid.uuid4()),primary_key=True,nullable=False)
  title = Column(String,nullable=False)
  description = Column(Text,nullable=False)
  tags = Column(JSON,nullable=True)

  created_at = Column(TIMESTAMP(timezone=True),nullable=True,server_default=text("CURRENT_TIMESTAMP"))

  author_id = Column(String,ForeignKey('users.id',ondelete="CASCADE"),nullable=False)

  owner = relationship("User")


  class Config:
    orm_mode = True

