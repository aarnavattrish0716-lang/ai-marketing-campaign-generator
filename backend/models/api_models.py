from pydantic import BaseModel, ConfigDict

class CampaignRequest(BaseModel):
    product: str
    audience: str
    platform: str
class CampaignResponse(BaseModel):
    title: str
    tagline: str
    cta: str
    hashtags: list[str]
class CampaignRecord(BaseModel):
    id: int
    product: str
    audience: str
    platform: str
    title: str
    tagline: str
    cta: str
    hashtags: str

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message:str