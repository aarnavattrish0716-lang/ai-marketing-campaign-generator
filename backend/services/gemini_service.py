from google import genai
from dotenv import load_dotenv
import os

from backend.models.api_models import (
    MarketingRequest,
    ResearchResponse,
    CampaignResponse,
    CampaignRevisionRequest,
)
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_campaign( request: MarketingRequest,
    research: ResearchResponse,):
    with open("backend/prompts/campaign.txt","r",encoding="utf-8") as file:
        prompt=file.read()
    prompt = prompt.format(
    product=request.product,
    audience=request.audience,
    platform=request.platform,

    seo_keywords=", ".join(research.seo_keywords),
    competitors=", ".join(research.competitors),
    audience_insights="\n".join(research.audience_insights),
    marketing_suggestions="\n".join(research.marketing_suggestions),
)   
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type":"application/json",
            "response_schema":CampaignResponse
        }
    )  
    campaign=CampaignResponse.model_validate_json(response.text)  
    return campaign
def generate_research(
    request: MarketingRequest,
):
    with open(
        "backend/prompts/research.txt",
        "r",
        encoding="utf-8",
    ) as file:
        prompt = file.read()

    prompt = prompt.format(
        product=request.product,
        audience=request.audience,
        platform=request.platform,
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ResearchResponse,
        },
    )

    research = ResearchResponse.model_validate_json(
        response.text
    )

    return research
def regenerate_campaign(
    request: CampaignRevisionRequest,
):
    with open(
        "backend/prompts/regenerate_campaign.txt",
        "r",
        encoding="utf-8",
    ) as file:
        prompt = file.read()

    prompt = prompt.format(
        product=request.marketing_request.product,
        audience=request.marketing_request.audience,
        platform=request.marketing_request.platform,

        seo_keywords=", ".join(request.research.seo_keywords),
        competitors=", ".join(request.research.competitors),
        audience_insights="\n".join(
            request.research.audience_insights
        ),
        marketing_suggestions="\n".join(
            request.research.marketing_suggestions
        ),

        title=request.previous_campaign.title,
        tagline=request.previous_campaign.tagline,
        cta=request.previous_campaign.cta,
        hashtags=", ".join(request.previous_campaign.hashtags),

        feedback=request.feedback,
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": CampaignResponse,
        },
    )

    campaign = CampaignResponse.model_validate_json(
        response.text
    )

    return campaign