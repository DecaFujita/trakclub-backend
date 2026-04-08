from sqlalchemy import Column, Integer, ForeignKey
from model import Base

class ProviderActivity(Base):
    __tablename__ = 'provider_activity'

    provider_id = Column(Integer, ForeignKey('provider.id'), primary_key=True)
    activity_id = Column(Integer, ForeignKey('activity.id'), primary_key=True)

    def __init__(self, provider_id: int, activity_id: int):
        self.provider_id = provider_id
        self.activity_id = activity_id