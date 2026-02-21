from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    suggested_price = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)