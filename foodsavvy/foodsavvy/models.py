"""Data models for FoodSavvy."""
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
import json


@dataclass
class PantryItem:
    name: str
    category: str
    quantity: float
    unit: str
    expiry_date: date
    location: str = "pantry"  # pantry, fridge, freezer
    notes: str = ""
    id: Optional[int] = None
    added_date: date = field(default_factory=date.today)

    @property
    def days_until_expiry(self) -> int:
        return (self.expiry_date - date.today()).days

    @property
    def status(self) -> str:
        d = self.days_until_expiry
        if d < 0:
            return "expired"
        elif d == 0:
            return "expires_today"
        elif d <= 2:
            return "critical"
        elif d <= 7:
            return "warning"
        else:
            return "good"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "unit": self.unit,
            "expiry_date": self.expiry_date.isoformat(),
            "location": self.location,
            "notes": self.notes,
            "added_date": self.added_date.isoformat(),
        }


@dataclass
class WasteRecord:
    item_name: str
    category: str
    quantity: float
    unit: str
    reason: str  # expired, spoiled, overstock, other
    estimated_cost: float
    waste_date: date = field(default_factory=date.today)
    id: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "item_name": self.item_name,
            "category": self.category,
            "quantity": self.quantity,
            "unit": self.unit,
            "reason": self.reason,
            "estimated_cost": self.estimated_cost,
            "waste_date": self.waste_date.isoformat(),
        }


@dataclass
class Recipe:
    name: str
    ingredients: list[str]
    instructions: str
    prep_time: int  # minutes
    servings: int
    tags: list[str] = field(default_factory=list)
    id: Optional[int] = None

    def matches(self, available_items: list[str], threshold: float = 0.5) -> float:
        """Return match score 0.0-1.0 based on available ingredients."""
        if not self.ingredients:
            return 0.0
        available_lower = [i.lower() for i in available_items]
        matched = sum(
            1 for ing in self.ingredients
            if any(ing.lower() in a or a in ing.lower() for a in available_lower)
        )
        return matched / len(self.ingredients)
