from sqlalchemy import Column, Integer, String
from backend.services.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True,autoincrement=True)

    product = Column(String, nullable=False)
    audience = Column(String, nullable=False)
    platform = Column(String, nullable=False)

    title = Column(String, nullable=False)
    tagline = Column(String, nullable=False)
    cta = Column(String, nullable=False)
    hashtags=Column(String,nullable=False)