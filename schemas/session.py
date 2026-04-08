from pydantic import BaseModel
from typing import List, Optional

from model.session import Session


class SessionSchema(BaseModel):
    weekday: str = "Tue"
    time: str = "18:00"
    provider_id: int = 1
    activity_id: int = 1
    name: Optional[str] = "Yoga Evening"


class SessionViewSchema(BaseModel):
    id: int
    weekday: str
    time: str
    provider_id: int
    activity_id: int
    name: Optional[str] = None


class SessionListSchema(BaseModel):
    sessions: List[SessionViewSchema]


class SessionDeleteSchema(BaseModel):
    message: str
    id: int


def present_sessions(sessions: List[Session]):
    result = []
    for s in sessions:
        result.append({
            "id": s.id,
            "weekday": s.weekday,
            "time": s.time,
            "provider_id": s.provider_id,
            "activity_id": s.activity_id,
            "name": s.name,
        })
    return {"sessions": result}


def present_session(s: Session):
    return {
        "id": s.id,
        "weekday": s.weekday,
        "time": s.time,
        "provider_id": s.provider_id,
        "activity_id": s.activity_id,
        "name": s.name,
    }