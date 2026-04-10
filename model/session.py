from sqlalchemy import Column, String, Integer, ForeignKey, Time
from model.base import Base


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True)

    # name = Column(String(140))  # optional

    weekday = Column(String(10), nullable=False)
    time = Column(String(5), nullable=False)  # keep simple for MVP (e.g. "18:00")

    provider_id = Column(Integer, ForeignKey("provider.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activity.id"), nullable=False)

    def __init__(
        self, weekday: str, time: str, provider_id: int, activity_id: int, name=None
    ):
        self.weekday = weekday
        self.time = time
        self.provider_id = provider_id
        self.activity_id = activity_id
        self.name = name
