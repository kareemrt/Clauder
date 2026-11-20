from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class MedicationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    dosage: str = Field(..., min_length=1, max_length=100)
    frequency: str = Field(..., min_length=1, max_length=100)
    times_per_day: int = Field(default=1, ge=1, le=24)
    instructions: Optional[str] = None
    end_date: Optional[datetime] = None


class MedicationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    dosage: Optional[str] = Field(None, min_length=1, max_length=100)
    frequency: Optional[str] = Field(None, min_length=1, max_length=100)
    times_per_day: Optional[int] = Field(None, ge=1, le=24)
    instructions: Optional[str] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None


class MedicationResponse(BaseModel):
    id: int
    name: str
    dosage: str
    frequency: str
    times_per_day: int
    instructions: Optional[str]
    start_date: datetime
    end_date: Optional[datetime]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DoseLogCreate(BaseModel):
    medication_id: int
    scheduled_time: datetime
    taken_at: Optional[datetime] = None
    was_taken: bool = False
    notes: Optional[str] = None


class DoseLogUpdate(BaseModel):
    taken_at: Optional[datetime] = None
    was_taken: Optional[bool] = None
    notes: Optional[str] = None


class DoseLogResponse(BaseModel):
    id: int
    medication_id: int
    scheduled_time: datetime
    taken_at: Optional[datetime]
    was_taken: bool
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SymptomLogCreate(BaseModel):
    symptom: str = Field(..., min_length=1, max_length=200)
    severity: int = Field(..., ge=1, le=10)
    notes: Optional[str] = None


class SymptomLogResponse(BaseModel):
    id: int
    symptom: str
    severity: int
    notes: Optional[str]
    logged_at: datetime

    class Config:
        from_attributes = True


class AdherenceReport(BaseModel):
    medication_id: int
    medication_name: str
    total_scheduled: int
    total_taken: int
    adherence_rate: float
    period_days: int


class HealthSummary(BaseModel):
    total_medications: int
    active_medications: int
    overall_adherence_rate: float
    doses_taken_today: int
    doses_scheduled_today: int
    recent_symptoms: List[SymptomLogResponse]
    medication_reports: List[AdherenceReport]
