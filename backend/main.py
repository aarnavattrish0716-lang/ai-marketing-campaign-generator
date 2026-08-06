from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import ValidationError
from google.genai import errors
import logging

from backend.models.api_models import (
    MarketingRequest,
    CampaignGenerationRequest,
    CampaignResponse,
    CampaignRecord,
    MessageResponse,
    ResearchResponse,
    CampaignRevisionRequest,
    SaveCampaignRequest,
)

from backend.services.database import (
    Base,
    engine,
    get_db,
)

from backend.services.gemini_service import (
    generate_research,
    generate_campaign,
    regenerate_campaign,
)

from backend.services.campaign_service import (
    save_campaign,
    get_all_campaigns,
    get_campaign_by_id,
    update_campaign_record,
    delete_campaign_record,
)
import inspect
print(inspect.signature(generate_research))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello"}


@app.post("/research", response_model=ResearchResponse)
def generate_research_endpoint(
    request: MarketingRequest,
):
    try:
        logger.info(
            "Generating research for product=%s",
            request.product,
        )

        research = generate_research(request)

        logger.info("Research generated successfully.")

        return research

    except ValidationError:
        logger.exception("Invalid Gemini response.")
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an invalid response",
        )

    except errors.APIError as e:
        logger.exception("Gemini API error.")

        if e.code == 429:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded.",
            )

        elif e.code == 401:
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key.",
            )

        raise HTTPException(
            status_code=e.code,
            detail=e.message,
        )

    except Exception:
        logger.exception("Unexpected error.")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@app.post(
    "/campaign",
    response_model=CampaignResponse,
)
def generate_campaign_endpoint(
    request: CampaignGenerationRequest,
):
    try:
        logger.info(
            "Generating campaign for product=%s",
            request.marketing_request.product,
        )

        campaign = generate_campaign(
            request.marketing_request,
            request.research,
        )

        logger.info(
            "Campaign generated successfully."
        )

        return campaign

    except ValidationError:
        logger.exception(
            "Invalid Gemini response."
        )
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an invalid response",
        )

    except errors.APIError as e:
        logger.exception(
            "Gemini API error."
        )

        if e.code == 429:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded.",
            )

        elif e.code == 401:
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key.",
            )

        raise HTTPException(
            status_code=e.code,
            detail=e.message,
        )

    except Exception:
        logger.exception(
            "Unexpected error."
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


@app.get(
    "/campaigns",
    response_model=list[CampaignRecord],
)
def get_campaigns(
    db: Session = Depends(get_db),
):
    return get_all_campaigns(db)


@app.get(
    "/campaigns/{campaign_id}",
    response_model=CampaignRecord,
)
def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
):
    campaign = get_campaign_by_id(
        db,
        campaign_id,
    )

    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Campaign not found",
        )

    return campaign

@app.post(
    "/campaign/regenerate",
    response_model=CampaignResponse,
)
def regenerate_campaign_endpoint(
    request: CampaignRevisionRequest,
):
    try:
        logger.info("Regenerating campaign.")

        campaign = regenerate_campaign(request)

        logger.info(
            "Campaign regenerated successfully."
        )

        return campaign

    except ValidationError:
        logger.exception(
            "Invalid response received from Gemini."
        )
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an invalid response",
        )

    except errors.APIError as e:
        logger.exception("Gemini API error.")

        if e.code == 429:
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded.",
            )

        elif e.code == 401:
            raise HTTPException(
                status_code=401,
                detail="Invalid Gemini API key.",
            )

        raise HTTPException(
            status_code=e.code,
            detail=e.message,
        )

    except Exception:
        logger.exception(
            "Unexpected error."
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )
@app.post(
    "/campaigns",
    response_model=CampaignRecord,
)
def save_campaign_endpoint(
    request: SaveCampaignRequest,
    db: Session = Depends(get_db),
):
    try:
        logger.info(
            "Saving approved campaign."
        )

        campaign = save_campaign(
            db,
            request.marketing_request,
            request.campaign,
        )

        logger.info(
            "Campaign saved successfully."
        )

        return campaign

    except Exception:
        logger.exception(
            "Unexpected error while saving campaign."
        )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )
@app.put(
    "/campaigns/{campaign_id}",
    response_model=CampaignRecord,
)
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

        campaign = update_campaign_record(
            db,
            campaign_id,
            request,
        )

        if campaign is None:
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

        return campaign

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
@app.delete(
    "/campaigns/{campaign_id}",
    response_model=MessageResponse,
)
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
):
    try:
        logger.info(
            "Deleting campaign ID=%s",
            campaign_id,
        )

        campaign = delete_campaign_record(
            db,
            campaign_id,
        )

        if campaign is None:
            logger.warning(
                "Campaign ID=%s not found",
                campaign_id,
            )
            raise HTTPException(
                status_code=404,
                detail="Campaign not found",
            )

        logger.info(
            "Campaign ID=%s deleted successfully",
            campaign_id,
        )

        return {
            "message": "Campaign deleted successfully"
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Unexpected error while deleting campaign."
        )
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )