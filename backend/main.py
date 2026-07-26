from fastapi import FastAPI
from backend.models import CampaignRequest
from backend.services.gemini_service import generate_campaign
app=FastAPI()
@app.get("/")
def home():
    return {
        "message":"hello"
    }
@app.get("/campaigns")
def get_campaigns():
    return []
@app.post("/campaigns")
def create_campaign(request:CampaignRequest):
    campaign = generate_campaign(
        request.product,
        request.audience,
        request.platform
    )

    return{
        "campaign": campaign
    }