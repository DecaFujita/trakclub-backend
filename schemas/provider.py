from pydantic import BaseModel
from typing import Optional, List
from model.provider import Provider


class ProviderSchema(BaseModel):
    """ Defines how a new provider (club) should be represented """
    name: str = "My Club"
    address: Optional[str] = "Street 123"
    city: Optional[str] = "São Paulo"
    state: Optional[str] = "SP"
    phone: Optional[str] = "999999999"
    website: Optional[str] = "www.club.com"
    instagram: Optional[str] = "@club"
    description: Optional[str] = "Best club in town"


class ProviderSearchSchema(BaseModel):
    """ Defines search structure (by name) """
    name: str = "My Club"


class ProviderListSchema(BaseModel):
    """ Defines how a list of providers is returned """
    providers: List[ProviderSchema]


class ProviderDeleteSchema(BaseModel):
    message: str
    name: str


def present_providers(providers: List[Provider]):
    result = []
    for provider in providers:
        result.append({
            "id": provider.id,
            "name": provider.name,
            "city": provider.city
        })
    return {"providers": result}


class ProviderViewSchema(BaseModel):
    """ Defines how a provider is returned """
    id: int
    name: str
    city: Optional[str]
    state: Optional[str]
    active: bool


def present_provider(provider: Provider):
    return {
        "id": provider.id,
        "name": provider.name,
        "city": provider.city,
        "state": provider.state,
        "active": provider.active
    }