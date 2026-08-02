from google import genai
from dotenv import load_dotenv
import os
import json
from backend.models.api_models import CampaignResponse, ResearchResponse
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_campaign(product, audience, platform):
    with open("prompts/campaign.txt","r",encoding="utf-8") as file:
        prompt=file.read()
    prompt=prompt.format(
        product=product,
        audience=audience,
        platform=platform)
    
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
def generate_research(product, audience, platform):
    with open("prompts/research.txt", "r", encoding="utf-8") as file:
        prompt = file.read()

    prompt = prompt.format(
        product=product,
        audience=audience,
        platform=platform,
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ResearchResponse,
        },
    )

    research = ResearchResponse.model_validate_json(response.text)

    return research
