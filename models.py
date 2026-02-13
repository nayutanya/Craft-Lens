from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    suggested_price = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)