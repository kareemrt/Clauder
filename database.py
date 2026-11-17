from datetime import date, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, default=1.0)
    unit = db.Column(db.String(30), default="unit")
    expiry_date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), default="other")
    status = db.Column(db.String(20), default="active")  # active, used, wasted
    added_date = db.Column(db.Date, default=date.today)

    def days_until_expiry(self):
        return (self.expiry_date - date.today()).days

    def urgency(self):
        days = self.days_until_expiry()
        if days < 0:
            return "expired"
        elif days <= 2:
            return "critical"
        elif days <= 5:
            return "warning"
        return "good"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity,
            "unit": self.unit,
            "expiry_date": self.expiry_date.isoformat(),
            "category": self.category,
            "status": self.status,
            "added_date": self.added_date.isoformat(),
            "days_until_expiry": self.days_until_expiry(),
            "urgency": self.urgency(),
        }


class WasteLog(db.Model):
    __tablename__ = "waste_logs"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    item_name = db.Column(db.String(100))
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(30))
    outcome = db.Column(db.String(20))  # used, wasted
    category = db.Column(db.String(50))
    logged_date = db.Column(db.Date, default=date.today)


def init_db(app):
    db.create_all()
    # Seed demo data if empty
    if Item.query.count() == 0:
        _seed_demo_data()


def _seed_demo_data():
    today = date.today()
    demo_items = [
        Item(name="Spinach", quantity=1, unit="bag", expiry_date=today + timedelta(days=1), category="vegetables"),
        Item(name="Chicken Breast", quantity=2, unit="pieces", expiry_date=today + timedelta(days=2), category="meat"),
        Item(name="Greek Yogurt", quantity=1, unit="container", expiry_date=today + timedelta(days=2), category="dairy"),
        Item(name="Cherry Tomatoes", quantity=1, unit="pint", expiry_date=today + timedelta(days=3), category="vegetables"),
        Item(name="Eggs", quantity=6, unit="eggs", expiry_date=today + timedelta(days=14), category="dairy"),
        Item(name="Cheddar Cheese", quantity=1, unit="block", expiry_date=today + timedelta(days=10), category="dairy"),
        Item(name="Broccoli", quantity=1, unit="head", expiry_date=today + timedelta(days=4), category="vegetables"),
        Item(name="Salmon Fillet", quantity=1, unit="piece", expiry_date=today + timedelta(days=1), category="meat"),
        Item(name="Avocado", quantity=2, unit="avocados", expiry_date=today + timedelta(days=3), category="vegetables"),
        Item(name="Blueberries", quantity=1, unit="pint", expiry_date=today + timedelta(days=5), category="fruits"),
    ]
    for item in demo_items:
        db.session.add(item)

    # Some historical waste logs
    logs = [
        WasteLog(item_name="Lettuce", quantity=1, unit="head", outcome="wasted", category="vegetables", logged_date=today - timedelta(days=5)),
        WasteLog(item_name="Mushrooms", quantity=1, unit="pack", outcome="used", category="vegetables", logged_date=today - timedelta(days=4)),
        WasteLog(item_name="Ground Beef", quantity=1, unit="lb", outcome="used", category="meat", logged_date=today - timedelta(days=3)),
        WasteLog(item_name="Strawberries", quantity=1, unit="pint", outcome="wasted", category="fruits", logged_date=today - timedelta(days=2)),
        WasteLog(item_name="Milk", quantity=1, unit="carton", outcome="used", category="dairy", logged_date=today - timedelta(days=1)),
    ]
    for log in logs:
        db.session.add(log)

    db.session.commit()
