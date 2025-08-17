from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    is_admin: bool = False
    subscription_expires_at: Optional[datetime] = None


class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: str = Field(index=True, unique=True)
    match_date_utc: str
    league: str
    home_team: str
    away_team: str
    kickoff_utc: str
    is_premium: bool = False

    prediction: Optional["Prediction"] = Relationship(
        back_populates="match",
        sa_relationship_kwargs={"uselist": False},
    )


class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    match_ref_id: int = Field(foreign_key="match.id", unique=True)
    tip_type: str
    tip_value: str
    confidence_percent: int
    odds_decimal: float
    analysis_note: Optional[str] = None

    match: Optional[Match] = Relationship(back_populates="prediction")
