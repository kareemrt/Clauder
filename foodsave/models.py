"""Data models for FoodSave."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
import json


@dataclass
class FoodItem:
    name: str
    quantity: float
    unit: str
    category: str
    purchase_date: date
    expiry_date: date
    item_id: Optional[str] = None

    def days_until_expiry(self) -> int:
        return (self.expiry_date - date.today()).days

    def is_expired(self) -> bool:
        return self.expiry_date < date.today()

    def is_expiring_soon(self, threshold_days: int = 3) -> bool:
        return 0 <= self.days_until_expiry() <= threshold_days

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "quantity": self.quantity,
            "unit": self.unit,
            "category": self.category,
            "purchase_date": self.purchase_date.isoformat(),
            "expiry_date": self.expiry_date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FoodItem":
        return cls(
            item_id=data.get("item_id"),
            name=data["name"],
            quantity=data["quantity"],
            unit=data["unit"],
            category=data["category"],
            purchase_date=date.fromisoformat(data["purchase_date"]),
            expiry_date=date.fromisoformat(data["expiry_date"]),
        )


@dataclass
class WasteRecord:
    item_name: str
    quantity: float
    unit: str
    category: str
    waste_date: date
    reason: str
    kg_co2_wasted: float
    usd_wasted: float
    record_id: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "record_id": self.record_id,
            "item_name": self.item_name,
            "quantity": self.quantity,
            "unit": self.unit,
            "category": self.category,
            "waste_date": self.waste_date.isoformat(),
            "reason": self.reason,
            "kg_co2_wasted": self.kg_co2_wasted,
            "usd_wasted": self.usd_wasted,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WasteRecord":
        return cls(
            record_id=data.get("record_id"),
            item_name=data["item_name"],
            quantity=data["quantity"],
            unit=data["unit"],
            category=data["category"],
            waste_date=date.fromisoformat(data["waste_date"]),
            reason=data["reason"],
            kg_co2_wasted=data["kg_co2_wasted"],
            usd_wasted=data["usd_wasted"],
        )


@dataclass
class ImpactStats:
    total_items_saved: int = 0
    total_kg_food_saved: float = 0.0
    total_co2_avoided_kg: float = 0.0
    total_money_saved_usd: float = 0.0
    total_items_wasted: int = 0
    total_kg_food_wasted: float = 0.0
    total_co2_emitted_kg: float = 0.0
    total_money_wasted_usd: float = 0.0
