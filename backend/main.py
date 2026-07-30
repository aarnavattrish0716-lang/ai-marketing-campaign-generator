from fastapi import FastAPI, HTTPException
from models import CampaignRequest,CampaignResponse
from services.gemini_service import generate_campaign
from pydantic import ValidationError
app=FastAPI()
@app.get("/")
def home():
    return {
        "message":"hello"
    }
@app.get("/campaigns")
def get_campaigns():
    return []
@app.post("/campaigns",response_model=CampaignResponse)
def create_campaign(request:CampaignRequest):
    try:
        campaign = generate_campaign(
            request.product,
            request.audience,
            request.platform
        )

        return campaign
    except ValidationError:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an invalid response"
        )
    except Exception as e:
        error = str(e)

        if "RESOURCE_EXHAUSTED" in error or "429" in error:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later."
            )

        elif "API_KEY" in error or "401" in error:
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key."
            )

        else:
            raise HTTPException(
                status_code=500,
                detail="Internal server error."
            )