from pydantic import BaseModel, Field, RootModel
from typing import List
from model.activity import Activity


class ActivityIdPath(BaseModel):
    """ Path parameter for GET/DELETE /activity/<activity_id> """
    activity_id: int = Field(..., description="Activity primary key")


class ActivitySchema(BaseModel):
    name: str = "Yoga"


class ActivityViewSchema(BaseModel):
    """Single activity as returned by GET /activities and GET /activity/<id>."""
    id: int
    name: str


class ActivityListSchema(RootModel[List[ActivityViewSchema]]):
    """Top-level JSON array for GET /activities."""


class ActivityDeleteSchema(BaseModel):
    message: str
    id: int


def present_activities(activities: List[Activity]):
    result = []
    for activity in activities:
        result.append({
            "id": activity.id,
            "name": activity.name
        })
    return result