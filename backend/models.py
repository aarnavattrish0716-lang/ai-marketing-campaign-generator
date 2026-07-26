from pydantic import BaseModel

class CampaignRequest(BaseModel):
    product: str
    audience: str
    platform: str
