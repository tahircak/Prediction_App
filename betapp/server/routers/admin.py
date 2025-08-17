import csv
from io import StringIO

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session, select

from db import get_session
from models import Match, Prediction, User
from auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(user: User):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")


@router.post("/import")
async def import_csv(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    require_admin(current_user)

    content = await file.read()
    text = content.decode("utf-8")
    reader = csv.DictReader(StringIO(text))
    required_cols = [
        "match_id",
        "match_date_utc",
        "league",
        "home_team",
        "away_team",
        "kickoff_utc",
        "tip_type",
        "tip_value",
        "confidence_percent",
        "odds_decimal",
        "analysis_note",
        "is_premium",
    ]
    for col in required_cols:
        if col not in reader.fieldnames:
            raise HTTPException(status_code=400, detail=f"Missing column: {col}")

    created = 0
    for row in reader:
        existing = session.exec(select(Match).where(Match.match_id == row["match_id"])).first()
        if existing:
            m = existing
        else:
            m = Match(
                match_id=row["match_id"],
                match_date_utc=row["match_date_utc"],
                league=row["league"],
                home_team=row["home_team"],
                away_team=row["away_team"],
                kickoff_utc=row["kickoff_utc"],
                is_premium=str(row.get("is_premium", "")).strip().lower() in ("true", "1", "yes"),
            )
            session.add(m)
            session.commit()
            session.refresh(m)

        p_existing = session.exec(select(Prediction).where(Prediction.match_ref_id == m.id)).first()
        if p_existing:
            p = p_existing
            p.tip_type = row["tip_type"]
            p.tip_value = row["tip_value"]
            p.confidence_percent = int(row["confidence_percent"]) if row["confidence_percent"] else 0
            p.odds_decimal = float(row["odds_decimal"]) if row["odds_decimal"] else 0.0
            p.analysis_note = row.get("analysis_note") or None
        else:
            p = Prediction(
                match_ref_id=m.id,
                tip_type=row["tip_type"],
                tip_value=row["tip_value"],
                confidence_percent=int(row["confidence_percent"]) if row["confidence_percent"] else 0,
                odds_decimal=float(row["odds_decimal"]) if row["odds_decimal"] else 0.0,
                analysis_note=row.get("analysis_note") or None,
            )
            session.add(p)
        session.commit()
        created += 1

    return {"status": "ok", "rows": created}
