from pydantic import BaseModel

class CampaignRequest(BaseModel):
    product: str
    audience: str
    platform: str
class CampaignResponse(BaseModel):
    title: str
    tagline: str
    cta: str
    hashtags: list[str]