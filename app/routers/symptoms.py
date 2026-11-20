from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import SymptomLog
from ..schemas import SymptomLogCreate, SymptomLogResponse

router = APIRouter(prefix="/api/symptoms", tags=["symptoms"])


@router.get("/", response_model=List[SymptomLogResponse])
def list_symptoms(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(days=days)
    return (
        db.query(SymptomLog)
        .filter(SymptomLog.logged_at >= since)
        .order_by(SymptomLog.logged_at.desc())
        .all()
    )


@router.post("/", response_model=SymptomLogResponse, status_code=status.HTTP_201_CREATED)
def log_symptom(payload: SymptomLogCreate, db: Session = Depends(get_db)):
    symptom = SymptomLog(**payload.model_dump())
    db.add(symptom)
    db.commit()
    db.refresh(symptom)
    return symptom


@router.delete("/{symptom_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_symptom(symptom_id: int, db: Session = Depends(get_db)):
    symptom = db.query(SymptomLog).filter(SymptomLog.id == symptom_id).first()
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom log not found")
    db.delete(symptom)
    db.commit()
