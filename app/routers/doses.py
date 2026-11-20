from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import DoseLog, Medication
from ..schemas import DoseLogCreate, DoseLogUpdate, DoseLogResponse

router = APIRouter(prefix="/api/doses", tags=["doses"])


@router.get("/", response_model=List[DoseLogResponse])
def list_doses(
    medication_id: Optional[int] = None,
    days: int = Query(default=7, ge=1, le=365),
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(days=days)
    query = db.query(DoseLog).filter(DoseLog.scheduled_time >= since)
    if medication_id:
        query = query.filter(DoseLog.medication_id == medication_id)
    return query.order_by(DoseLog.scheduled_time.desc()).all()


@router.get("/today", response_model=List[DoseLogResponse])
def list_todays_doses(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(days=1)
    return (
        db.query(DoseLog)
        .filter(DoseLog.scheduled_time >= start, DoseLog.scheduled_time < end)
        .order_by(DoseLog.scheduled_time)
        .all()
    )


@router.post("/", response_model=DoseLogResponse, status_code=status.HTTP_201_CREATED)
def log_dose(payload: DoseLogCreate, db: Session = Depends(get_db)):
    med = db.query(Medication).filter(Medication.id == payload.medication_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    dose = DoseLog(**payload.model_dump())
    db.add(dose)
    db.commit()
    db.refresh(dose)
    return dose


@router.patch("/{dose_id}", response_model=DoseLogResponse)
def update_dose(dose_id: int, payload: DoseLogUpdate, db: Session = Depends(get_db)):
    dose = db.query(DoseLog).filter(DoseLog.id == dose_id).first()
    if not dose:
        raise HTTPException(status_code=404, detail="Dose log not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(dose, field, value)
    db.commit()
    db.refresh(dose)
    return dose


@router.post("/{dose_id}/take", response_model=DoseLogResponse)
def mark_dose_taken(dose_id: int, db: Session = Depends(get_db)):
    dose = db.query(DoseLog).filter(DoseLog.id == dose_id).first()
    if not dose:
        raise HTTPException(status_code=404, detail="Dose log not found")
    dose.was_taken = True
    dose.taken_at = datetime.utcnow()
    db.commit()
    db.refresh(dose)
    return dose
