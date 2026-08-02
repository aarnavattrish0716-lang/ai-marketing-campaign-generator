from pydantic import BaseModel, ConfigDict
# Request Model
class MarketingRequest(BaseModel):
    product: str
    audience: str
    platform: str
#AI response models
class ResearchResponse(BaseModel):
    seo_keywords: list[str]
    competitors: list[str]
    audience_insights: list[str]
    marketing_suggestions: list[str]

class CampaignConcept(BaseModel):
    concept_id: int
    concept_name: str
    description: str
    title: str
    tagline: str
    cta: str
    hashtags: list[str]

class CampaignConceptResponse(BaseModel):
    recommended_concept_id: int
    concepts: list[CampaignConcept]
    
#Database Model
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

#Generic Model
class MessageResponse(BaseModel):
    message:str

class CampaignResponse(BaseModel):
    title: str
    tagline: str
    cta: str
    hashtags: list[str]



