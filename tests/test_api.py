import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

TEST_DB_URL = "sqlite:///./test_meditrack.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


# --- Medications ---

def test_create_medication(client):
    resp = client.post("/api/medications/", json={
        "name": "Metformin",
        "dosage": "500mg",
        "frequency": "twice daily",
        "times_per_day": 2,
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Metformin"
    assert data["dosage"] == "500mg"
    assert data["is_active"] is True


def test_list_medications_empty(client):
    resp = client.get("/api/medications/")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_medications(client):
    client.post("/api/medications/", json={"name": "Aspirin", "dosage": "100mg", "frequency": "daily"})
    client.post("/api/medications/", json={"name": "Lisinopril", "dosage": "10mg", "frequency": "daily"})
    resp = client.get("/api/medications/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_medication(client):
    created = client.post("/api/medications/", json={
        "name": "Atorvastatin", "dosage": "20mg", "frequency": "nightly"
    }).json()
    resp = client.get(f"/api/medications/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Atorvastatin"


def test_get_medication_not_found(client):
    assert client.get("/api/medications/9999").status_code == 404


def test_update_medication(client):
    med = client.post("/api/medications/", json={
        "name": "OldName", "dosage": "5mg", "frequency": "daily"
    }).json()
    resp = client.patch(f"/api/medications/{med['id']}", json={"name": "NewName", "is_active": False})
    assert resp.status_code == 200
    assert resp.json()["name"] == "NewName"
    assert resp.json()["is_active"] is False


def test_delete_medication(client):
    med = client.post("/api/medications/", json={
        "name": "ToDelete", "dosage": "1mg", "frequency": "daily"
    }).json()
    assert client.delete(f"/api/medications/{med['id']}").status_code == 204
    assert client.get(f"/api/medications/{med['id']}").status_code == 404


# --- Doses ---

def test_log_dose(client):
    med = client.post("/api/medications/", json={
        "name": "Metformin", "dosage": "500mg", "frequency": "twice daily", "times_per_day": 2
    }).json()
    resp = client.post("/api/doses/", json={
        "medication_id": med["id"],
        "scheduled_time": datetime.utcnow().isoformat(),
        "was_taken": False,
    })
    assert resp.status_code == 201
    assert resp.json()["was_taken"] is False


def test_mark_dose_taken(client):
    med = client.post("/api/medications/", json={
        "name": "Aspirin", "dosage": "100mg", "frequency": "daily"
    }).json()
    dose = client.post("/api/doses/", json={
        "medication_id": med["id"],
        "scheduled_time": datetime.utcnow().isoformat(),
    }).json()
    resp = client.post(f"/api/doses/{dose['id']}/take")
    assert resp.status_code == 200
    assert resp.json()["was_taken"] is True
    assert resp.json()["taken_at"] is not None


def test_log_dose_invalid_medication(client):
    resp = client.post("/api/doses/", json={
        "medication_id": 9999,
        "scheduled_time": datetime.utcnow().isoformat(),
    })
    assert resp.status_code == 404


# --- Symptoms ---

def test_log_symptom(client):
    resp = client.post("/api/symptoms/", json={"symptom": "Headache", "severity": 7})
    assert resp.status_code == 201
    data = resp.json()
    assert data["symptom"] == "Headache"
    assert data["severity"] == 7


def test_symptom_severity_validation(client):
    assert client.post("/api/symptoms/", json={"symptom": "X", "severity": 0}).status_code == 422
    assert client.post("/api/symptoms/", json={"symptom": "X", "severity": 11}).status_code == 422


def test_list_symptoms(client):
    client.post("/api/symptoms/", json={"symptom": "Fatigue", "severity": 4})
    client.post("/api/symptoms/", json={"symptom": "Nausea", "severity": 6})
    resp = client.get("/api/symptoms/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


# --- Reports ---

def test_health_summary_empty(client):
    resp = client.get("/api/reports/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_medications"] == 0
    assert data["overall_adherence_rate"] == 0.0


def test_adherence_report(client):
    med = client.post("/api/medications/", json={
        "name": "Metformin", "dosage": "500mg", "frequency": "daily"
    }).json()
    for _ in range(3):
        client.post("/api/doses/", json={
            "medication_id": med["id"],
            "scheduled_time": datetime.utcnow().isoformat(),
            "was_taken": True,
        })
    client.post("/api/doses/", json={
        "medication_id": med["id"],
        "scheduled_time": datetime.utcnow().isoformat(),
        "was_taken": False,
    })
    resp = client.get("/api/reports/adherence")
    assert resp.status_code == 200
    report = resp.json()[0]
    assert report["total_scheduled"] == 4
    assert report["total_taken"] == 3
    assert report["adherence_rate"] == 75.0


# --- Health check ---

def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"
