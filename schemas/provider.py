from pydantic import BaseModel, Field, RootModel, field_validator
from typing import Optional, List
from model.provider import Provider


class ProviderIdPath(BaseModel):
    """ Path parameter for GET/DELETE /provider/<provider_id> """
    provider_id: int = Field(..., description="Provider primary key")


class ProviderSchema(BaseModel):
    """ Defines how a new provider (club) should be represented """
    name: str = "My Club"
    address: Optional[str] = "Street 123"
    city: Optional[str] = "Rio de Janeiro"
    state: Optional[str] = "RJ"
    phone: Optional[str] = "999999999"
    website: Optional[str] = "www.club.com"
    instagram: Optional[str] = "@club"
    description: Optional[str] = "Best club in town"

    @field_validator("phone", mode="before")
    @classmethod
    def phone_to_str(cls, v):
        if v is None:
            return v
        return str(v)


class ProviderSearchSchema(BaseModel):
    """ Defines search structure (by name) """
    name: str = "My Club"


class ProviderViewSchema(BaseModel):
    """ Defines how a provider is returned """
    id: int
    name: str
    city: Optional[str]
    state: Optional[str]
    active: bool


class ProviderListSchema(RootModel[List[ProviderViewSchema]]):
    """Top-level JSON array for GET /providers."""


class ProviderDeleteSchema(BaseModel):
    message: str
    id: int


def present_providers(providers: List[Provider]):
    result = []
    for provider in providers:
        result.append({
            "id": provider.id,
            "name": provider.name,
            "city": provider.city,
            "state": provider.state,
            "active": provider.active,
        })
    return result


def present_provider(provider: Provider):
    return {
        "id": provider.id,
        "name": provider.name,
        "city": provider.city,
        "state": provider.state,
        "active": provider.active
    }