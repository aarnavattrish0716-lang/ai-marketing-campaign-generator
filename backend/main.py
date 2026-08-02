from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from backend.models.api_models import CampaignRecord,MarketingRequest,CampaignResponse, MessageResponse, ResearchResponse
from backend.services.database import get_db,Base,engine
from backend.services.gemini_service import generate_campaign, generate_research
from backend.services.campaign_service import delete_campaign_record, get_campaign_by_id, save_campaign,get_all_campaigns, update_campaign_record
from pydantic import ValidationError
from google.genai import errors
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)
app=FastAPI()

@app.get("/")
def home():
    return {
        "message":"hello"
    }

@app.get("/campaigns",response_model=list[CampaignRecord])
def get_campaigns(db: Session = Depends(get_db)):
    campaigns = get_all_campaigns(db)
    return campaigns

@app.get("/campaigns/{id}",response_model=CampaignRecord)
def get_campaign(Campaign_id:int,db:Session=Depends(get_db)):
    logger.info("Fetching campaign ID=%s", Campaign_id)
    campaign=get_campaign_by_id(db,Campaign_id)
    if campaign is None:
        logger.warning("Campaign ID=%s not found", Campaign_id)
        raise HTTPException(
            status_code=404,
            detail="Campaign not found"
        )
    return campaign
@app.post("/campaigns",response_model=CampaignResponse)
def create_campaign(request:MarketingRequest,db:Session=Depends(get_db)):
    try:
        campaign = generate_campaign(
            request.product,
            request.audience,
            request.platform
        )
        save_campaign(db,request,campaign)

        return campaign
    except ValidationError:
        logger.exception("Invalid response received from Gemini.")
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an invalid response"
        )
    except errors.APIError as e:
        logger.exception("Gemini API error.")
        if e.code==429:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later."
            )

        elif e.code==401:
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key."
            )

        else:
            raise HTTPException(
                status_code=e.code,
                detail=e.message
            )
    except Exception:
        logger.exception("Unexpected error.")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
@app.put( "/campaigns/{campaign_id}",response_model=CampaignRecord,)
def update_campaign(
    campaign_id: int,
    request: CampaignResponse,
    db: Session = Depends(get_db),
):
    try:
        logger.info(
            "Updating campaign ID=%s",
            campaign_id,
        )

        updated_campaign = update_campaign_record(
            db,
            campaign_id,
            request,
        )

        if updated_campaign is None:
            logger.warning(
                "Campaign ID=%s not found",
                campaign_id,
            )
            raise HTTPException(
                status_code=404,
                detail="Campaign not found",
            )

        logger.info(
            "Campaign ID=%s updated successfully",
            campaign_id,
        )

        return updated_campaign

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected error while updating campaign."
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )
@app.delete("/deletecampaign/{id}",response_model=MessageResponse)
def delete_campaign(campaign_id:int,db:Session=Depends(get_db)):
    try:
        logger.info(
            "Deleting campaign ID=%s",
            campaign_id
        )
        delete_campaign=delete_campaign_record(
            db,
            campaign_id
        )
        if delete_campaign is None:
            logger.warning(
                "Campaign ID=%s not found",
                campaign_id
            )
            raise HTTPException(
                status_code=404,
                detail="Campaign not found"
            )
        logger.info(
            "Campaign ID=%s deleted successfully",
            campaign_id
        )
        return {
            "message":"Campaign deleted successfully"
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception(
            "Unexpected error while deleting campaign."
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
@app.post("/research", response_model=ResearchResponse)
def generate_research_endpoint(
    request: MarketingRequest,
):
    try:
        logger.info(
        "Generating market research for product=%s on platform=%s",
        request.product,
        request.platform,
    )
        research=generate_research(request.product,request.audience,request.platform)
        logger.info(
        "Market research generated successfully."
    )
        return research
    except ValidationError:
        logger.exception("Invalid response received from Gemini.")
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an invalid response"
        )
    except errors.APIError as e:
        logger.exception("Gemini API error.")
        if e.code==429:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later."
            )

        elif e.code==401:
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key."
            )

        else:
            raise HTTPException(
                status_code=e.code,
                detail=e.message
            )
    except Exception:
        logger.exception("Unexpected Error")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )