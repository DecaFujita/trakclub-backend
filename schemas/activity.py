from pydantic import BaseModel
from typing import List
from model.activity import Activity


class ActivitySchema(BaseModel):
    name: str = "Yoga"


class ActivityListSchema(BaseModel):
    activities: List[ActivitySchema]


class ActivityDeleteSchema(BaseModel):
    message: str
    name: str


def present_activities(activities: List[Activity]):
    result = []
    for activity in activities:
        result.append({
            "id": activity.id,
            "name": activity.name
        })
    return {"activities": result}