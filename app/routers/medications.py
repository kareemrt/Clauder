from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Medication
from ..schemas import MedicationCreate, MedicationUpdate, MedicationResponse

router = APIRouter(prefix="/api/medications", tags=["medications"])


@router.get("/", response_model=List[MedicationResponse])
def list_medications(active_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Medication)
    if active_only:
        query = query.filter(Medication.is_active == True)
    return query.order_by(Medication.created_at.desc()).all()


@router.post("/", response_model=MedicationResponse, status_code=status.HTTP_201_CREATED)
def create_medication(payload: MedicationCreate, db: Session = Depends(get_db)):
    med = Medication(**payload.model_dump())
    db.add(med)
    db.commit()
    db.refresh(med)
    return med


@router.get("/{medication_id}", response_model=MedicationResponse)
def get_medication(medication_id: int, db: Session = Depends(get_db)):
    med = db.query(Medication).filter(Medication.id == medication_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    return med


@router.patch("/{medication_id}", response_model=MedicationResponse)
def update_medication(medication_id: int, payload: MedicationUpdate, db: Session = Depends(get_db)):
    med = db.query(Medication).filter(Medication.id == medication_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(med, field, value)
    db.commit()
    db.refresh(med)
    return med


@router.delete("/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medication(medication_id: int, db: Session = Depends(get_db)):
    med = db.query(Medication).filter(Medication.id == medication_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication not found")
    db.delete(med)
    db.commit()
