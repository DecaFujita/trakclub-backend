from sqlalchemy import Column, String, Integer
from model import Base

class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name