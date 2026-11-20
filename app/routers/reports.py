from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Medication, DoseLog, SymptomLog
from ..schemas import AdherenceReport, HealthSummary

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _adherence_for_medication(med: Medication, doses: List[DoseLog], period_days: int) -> AdherenceReport:
    total = len(doses)
    taken = sum(1 for d in doses if d.was_taken)
    rate = round((taken / total * 100) if total > 0 else 0.0, 1)
    return AdherenceReport(
        medication_id=med.id,
        medication_name=med.name,
        total_scheduled=total,
        total_taken=taken,
        adherence_rate=rate,
        period_days=period_days,
    )


@router.get("/adherence", response_model=List[AdherenceReport])
def adherence_report(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(days=days)
    medications = db.query(Medication).filter(Medication.is_active == True).all()
    reports = []
    for med in medications:
        doses = (
            db.query(DoseLog)
            .filter(DoseLog.medication_id == med.id, DoseLog.scheduled_time >= since)
            .all()
        )
        reports.append(_adherence_for_medication(med, doses, days))
    return reports


@router.get("/summary", response_model=HealthSummary)
def health_summary(db: Session = Depends(get_db)):
    today = datetime.utcnow().date()
    day_start = datetime(today.year, today.month, today.day)
    day_end = day_start + timedelta(days=1)
    month_ago = datetime.utcnow() - timedelta(days=30)

    all_meds = db.query(Medication).all()
    active_meds = [m for m in all_meds if m.is_active]

    today_doses = (
        db.query(DoseLog)
        .filter(DoseLog.scheduled_time >= day_start, DoseLog.scheduled_time < day_end)
        .all()
    )
    doses_today = sum(1 for d in today_doses if d.was_taken)
    scheduled_today = len(today_doses)

    all_doses_month = (
        db.query(DoseLog).filter(DoseLog.scheduled_time >= month_ago).all()
    )
    total = len(all_doses_month)
    taken = sum(1 for d in all_doses_month if d.was_taken)
    overall_rate = round((taken / total * 100) if total > 0 else 0.0, 1)

    recent_symptoms = (
        db.query(SymptomLog)
        .filter(SymptomLog.logged_at >= month_ago)
        .order_by(SymptomLog.logged_at.desc())
        .limit(10)
        .all()
    )

    med_reports = []
    for med in active_meds:
        doses = (
            db.query(DoseLog)
            .filter(DoseLog.medication_id == med.id, DoseLog.scheduled_time >= month_ago)
            .all()
        )
        med_reports.append(_adherence_for_medication(med, doses, 30))

    return HealthSummary(
        total_medications=len(all_meds),
        active_medications=len(active_meds),
        overall_adherence_rate=overall_rate,
        doses_taken_today=doses_today,
        doses_scheduled_today=scheduled_today,
        recent_symptoms=recent_symptoms,
        medication_reports=med_reports,
    )
