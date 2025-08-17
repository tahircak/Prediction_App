from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    subscription_expires_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PredictionOut(BaseModel):
    tip_type: str
    tip_value: str
    confidence_percent: int
    odds_decimal: float
    analysis_note: Optional[str] = None


class MatchOut(BaseModel):
    match_id: str
    match_date_utc: str
    league: str
    home_team: str
    away_team: str
    kickoff_utc: str
    is_premium: bool
    prediction: Optional[PredictionOut] = None
