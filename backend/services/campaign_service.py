from sqlalchemy.orm import Session

from backend.models.api_models import CampaignRequest, CampaignResponse
from backend.models.db_models import Campaign


def save_campaign(
    db: Session,
    request: CampaignRequest,
    response: CampaignResponse,
):
    record = Campaign(
        product=request.product,
        audience=request.audience,
        platform=request.platform,
        title=response.title,
        tagline=response.tagline,
        cta=response.cta,
        hashtags=", ".join(response.hashtags),
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record

def get_all_campaigns(db:Session):
    campaigns=db.query(Campaign).all()
    return campaigns

def get_campaign_by_id(
    db: Session,
    campaign_id: int
):
    return (
        db.query(Campaign)
        .filter(Campaign.id == campaign_id)
        .first()
    )
def update_campaign_record(
    db: Session,
    campaign_id: int,
    request: CampaignResponse,
):
    campaign = get_campaign_by_id(db, campaign_id)

    if campaign is None:
        return None

    campaign.title = request.title
    campaign.tagline = request.tagline
    campaign.cta = request.cta
    campaign.hashtags = ", ".join(request.hashtags)

    db.commit()
    db.refresh(campaign)

    return campaign
def delete_campaign_record(db:Session,campaign_id:int):
    campaign=get_campaign_by_id(db,campaign_id)
    if campaign is None:
        return None
    db.delete(campaign)
    db.commit()
    return campaign