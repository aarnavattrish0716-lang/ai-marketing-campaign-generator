from pydantic import BaseModel, ConfigDict

class MarketingRequest(BaseModel):
    product: str
    audience: str
    platform: str

class CampaignResponse(BaseModel):
    title: str
    tagline: str
    cta: str
    hashtags: list[str]


class ResearchResponse(BaseModel):
    seo_keywords: list[str]
    competitors: list[str]
    audience_insights: list[str]
    marketing_suggestions: list[str]

class CampaignGenerationRequest(BaseModel):
    marketing_request: MarketingRequest
    research: ResearchResponse


class CampaignRevisionRequest(BaseModel):
    marketing_request: MarketingRequest
    research: ResearchResponse
    previous_campaign: CampaignResponse
    feedback: str


class SaveCampaignRequest(BaseModel):
    marketing_request: MarketingRequest
    campaign: CampaignResponse

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
    message: str