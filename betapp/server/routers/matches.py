from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db import get_session
from models import Match
from schemas import MatchOut, PredictionOut
from auth import get_current_user_optional, is_active_member

router = APIRouter(prefix="/matches", tags=["matches"])


def serialize_match(match: Match, include_prediction: bool) -> MatchOut:
    pred = None
    if include_prediction and match.prediction:
        p = match.prediction
        pred = PredictionOut(
            tip_type=p.tip_type,
            tip_value=p.tip_value,
            confidence_percent=p.confidence_percent,
            odds_decimal=p.odds_decimal,
            analysis_note=p.analysis_note,
        )
    return MatchOut(
        match_id=match.match_id,
        match_date_utc=match.match_date_utc,
        league=match.league,
        home_team=match.home_team,
        away_team=match.away_team,
        kickoff_utc=match.kickoff_utc,
        is_premium=match.is_premium,
        prediction=pred,
    )


@router.get("", response_model=List[MatchOut])
def list_matches(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user_optional),
):
    member = is_active_member(current_user)
    matches = session.exec(select(Match)).all()
    output: List[MatchOut] = []
    for m in matches:
        include_pred = (not m.is_premium) or member
        output.append(serialize_match(m, include_pred))
    return output


@router.get("/{match_id}", response_model=MatchOut)
def get_match(
    match_id: str,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user_optional),
):
    m = session.exec(select(Match).where(Match.match_id == match_id)).first()
    if not m:
        raise HTTPException(status_code=404, detail="Match not found")
    member = is_active_member(current_user)
    include_pred = (not m.is_premium) or member
    return serialize_match(m, include_pred)
