import sqlite3
import json
import math
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, g

app = Flask(__name__)
DATABASE = "data/foodbridge.db"

# --- DB helpers ---

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.executescript("""
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                donor_name TEXT NOT NULL,
                donor_type TEXT NOT NULL,
                food_name TEXT NOT NULL,
                food_category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                neighborhood TEXT NOT NULL,
                city TEXT NOT NULL,
                lat REAL,
                lng REAL,
                notes TEXT,
                status TEXT DEFAULT 'available',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                claimed_at TEXT,
                recipient_name TEXT
            );

            CREATE TABLE IF NOT EXISTS claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id INTEGER NOT NULL,
                recipient_name TEXT NOT NULL,
                recipient_type TEXT NOT NULL,
                contact TEXT NOT NULL,
                pickup_time TEXT NOT NULL,
                claimed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (listing_id) REFERENCES listings(id)
            );

            CREATE TABLE IF NOT EXISTS impact_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id INTEGER NOT NULL,
                food_weight_kg REAL NOT NULL,
                meals_equivalent INTEGER NOT NULL,
                co2_saved_kg REAL NOT NULL,
                logged_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        db.commit()

# --- CO2 & meals math ---
# 1 kg of food waste ≈ 2.5 kg CO2 (EPA avg)
# 1 meal ≈ 0.4 kg of food
CO2_PER_KG = 2.5
KG_PER_MEAL = 0.4

UNIT_TO_KG = {
    "lbs": 0.453592,
    "kg": 1.0,
    "portions": 0.3,
    "servings": 0.3,
    "loaves": 0.45,
    "cans": 0.4,
    "boxes": 0.5,
    "bags": 0.5,
    "trays": 1.2,
    "gallons": 3.785,
    "liters": 1.0,
}

def calc_impact(quantity, unit):
    kg = quantity * UNIT_TO_KG.get(unit, 0.5)
    meals = max(1, int(kg / KG_PER_MEAL))
    co2 = round(kg * CO2_PER_KG, 2)
    return round(kg, 2), meals, co2

# --- Routes ---

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/donate")
def donate_page():
    return render_template("donate.html")

@app.route("/find")
def find_page():
    return render_template("find.html")

@app.route("/impact")
def impact_page():
    return render_template("impact.html")

# --- API ---

@app.route("/api/listings", methods=["GET"])
def get_listings():
    db = get_db()
    category = request.args.get("category", "")
    city = request.args.get("city", "")
    status = request.args.get("status", "available")

    query = "SELECT * FROM listings WHERE status = ?"
    params = [status]
    if category:
        query += " AND food_category = ?"
        params.append(category)
    if city:
        query += " AND LOWER(city) LIKE ?"
        params.append(f"%{city.lower()}%")
    query += " ORDER BY expiry_date ASC"

    rows = db.execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/listings", methods=["POST"])
def create_listing():
    data = request.get_json()
    required = ["donor_name", "donor_type", "food_name", "food_category",
                "quantity", "unit", "expiry_date", "neighborhood", "city"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Validate expiry is in the future
    try:
        exp = datetime.strptime(data["expiry_date"], "%Y-%m-%d")
        if exp.date() < datetime.now().date():
            return jsonify({"error": "Expiry date must be in the future"}), 400
    except ValueError:
        return jsonify({"error": "Invalid expiry date format (use YYYY-MM-DD)"}), 400

    db = get_db()
    db.execute(
        """INSERT INTO listings
           (donor_name, donor_type, food_name, food_category, quantity, unit,
            expiry_date, neighborhood, city, lat, lng, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data["donor_name"], data["donor_type"], data["food_name"],
            data["food_category"], data["quantity"], data["unit"],
            data["expiry_date"], data["neighborhood"], data["city"],
            data.get("lat"), data.get("lng"), data.get("notes", "")
        )
    )
    db.commit()
    return jsonify({"success": True, "message": "Listing created successfully"}), 201

@app.route("/api/listings/<int:listing_id>/claim", methods=["POST"])
def claim_listing(listing_id):
    data = request.get_json()
    required = ["recipient_name", "recipient_type", "contact", "pickup_time"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    db = get_db()
    listing = db.execute("SELECT * FROM listings WHERE id = ?", (listing_id,)).fetchone()
    if not listing:
        return jsonify({"error": "Listing not found"}), 404
    if listing["status"] != "available":
        return jsonify({"error": "This listing has already been claimed"}), 409

    now = datetime.now().isoformat()
    db.execute(
        "UPDATE listings SET status='claimed', claimed_at=?, recipient_name=? WHERE id=?",
        (now, data["recipient_name"], listing_id)
    )
    db.execute(
        """INSERT INTO claims
           (listing_id, recipient_name, recipient_type, contact, pickup_time)
           VALUES (?, ?, ?, ?, ?)""",
        (listing_id, data["recipient_name"], data["recipient_type"],
         data["contact"], data["pickup_time"])
    )
    # Log impact
    kg, meals, co2 = calc_impact(listing["quantity"], listing["unit"])
    db.execute(
        "INSERT INTO impact_log (listing_id, food_weight_kg, meals_equivalent, co2_saved_kg) VALUES (?, ?, ?, ?)",
        (listing_id, kg, meals, co2)
    )
    db.commit()
    return jsonify({
        "success": True,
        "message": f"Successfully claimed! Estimated impact: {meals} meals, {co2} kg CO₂ saved"
    })

@app.route("/api/stats", methods=["GET"])
def get_stats():
    db = get_db()
    total_listings = db.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
    claimed = db.execute("SELECT COUNT(*) FROM listings WHERE status='claimed'").fetchone()[0]
    available = db.execute("SELECT COUNT(*) FROM listings WHERE status='available'").fetchone()[0]

    impact = db.execute(
        "SELECT SUM(food_weight_kg), SUM(meals_equivalent), SUM(co2_saved_kg) FROM impact_log"
    ).fetchone()
    total_kg = round(impact[0] or 0, 1)
    total_meals = impact[1] or 0
    total_co2 = round(impact[2] or 0, 1)

    # Monthly trend (last 6 months)
    monthly = []
    for i in range(5, -1, -1):
        d = datetime.now() - timedelta(days=30 * i)
        month_str = d.strftime("%Y-%m")
        label = d.strftime("%b %Y")
        row = db.execute(
            "SELECT SUM(meals_equivalent) FROM impact_log WHERE logged_at LIKE ?",
            (f"{month_str}%",)
        ).fetchone()
        monthly.append({"month": label, "meals": row[0] or 0})

    # By category
    cats = db.execute(
        """SELECT l.food_category, COUNT(*), SUM(il.meals_equivalent)
           FROM listings l
           LEFT JOIN impact_log il ON il.listing_id = l.id
           WHERE l.status='claimed'
           GROUP BY l.food_category"""
    ).fetchall()

    return jsonify({
        "totals": {
            "listings": total_listings,
            "claimed": claimed,
            "available": available,
            "kg_rescued": total_kg,
            "meals": total_meals,
            "co2_saved_kg": total_co2,
            "trees_equivalent": round(total_co2 / 21, 1)  # avg tree absorbs 21 kg CO2/yr
        },
        "monthly_trend": monthly,
        "by_category": [{"category": r[0], "count": r[1], "meals": r[2] or 0} for r in cats]
    })

@app.route("/api/seed", methods=["POST"])
def seed_data():
    """Seed with realistic demo data — only for demonstration."""
    db = get_db()
    existing = db.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
    if existing > 0:
        return jsonify({"message": "Data already seeded"}), 200

    today = datetime.now()
    listings = [
        ("Green Leaf Bistro", "restaurant", "Mixed Vegetable Stir-Fry", "prepared",
         20, "portions", (today + timedelta(days=1)).strftime("%Y-%m-%d"),
         "Downtown", "San Francisco", 37.7749, -122.4194,
         "Freshly made, mild seasoning. Best reheated."),
        ("Whole Foods Market", "grocery", "Organic Bread Loaves", "bakery",
         15, "loaves", (today + timedelta(days=2)).strftime("%Y-%m-%d"),
         "Mission District", "San Francisco", 37.7599, -122.4148,
         "Day-old bread, still excellent quality."),
        ("City Hotel & Suites", "hotel", "Breakfast Buffet Surplus", "prepared",
         50, "portions", (today + timedelta(hours=10)).strftime("%Y-%m-%d"),
         "Union Square", "San Francisco", 37.7879, -122.4075,
         "Eggs, toast, fruit. Available after 11am checkout."),
        ("Fresh Harvest Co-op", "grocery", "Ripe Bananas", "produce",
         40, "lbs", (today + timedelta(days=2)).strftime("%Y-%m-%d"),
         "Tenderloin", "San Francisco", 37.7836, -122.4147,
         "Perfect for baking. Very ripe."),
        ("Sunrise Bakery", "bakery", "Assorted Pastries", "bakery",
         30, "portions", (today + timedelta(days=1)).strftime("%Y-%m-%d"),
         "Hayes Valley", "San Francisco", 37.7764, -122.4242,
         "Croissants, muffins, danishes. End of day surplus."),
        ("Pacific Rim Restaurant", "restaurant", "Cooked Rice & Proteins", "prepared",
         25, "portions", (today + timedelta(days=1)).strftime("%Y-%m-%d"),
         "Chinatown", "San Francisco", 37.7941, -122.4079,
         "Chicken, tofu and rice dishes. Halal options available."),
        ("Bay Area Catering", "catering", "Event Surplus Food", "prepared",
         80, "portions", (today + timedelta(days=1)).strftime("%Y-%m-%d"),
         "SoMa", "San Francisco", 37.7786, -122.3961,
         "Corporate lunch surplus. Mixed cuisines."),
        ("Community Garden", "farm", "Seasonal Vegetables", "produce",
         30, "lbs", (today + timedelta(days=5)).strftime("%Y-%m-%d"),
         "Richmond", "San Francisco", 37.7791, -122.4687,
         "Kale, lettuce, zucchini. Freshly harvested."),
    ]

    for l in listings:
        db.execute(
            """INSERT INTO listings
               (donor_name, donor_type, food_name, food_category, quantity, unit,
                expiry_date, neighborhood, city, lat, lng, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", l
        )

    # Create some historical claimed listings for impact stats
    past_listings = [
        ("Metro Deli", "restaurant", "Deli Sandwiches", "prepared",
         30, "portions", (today - timedelta(days=5)).strftime("%Y-%m-%d"),
         "Financial District", "San Francisco", None, None, ""),
        ("Bay Supermarket", "grocery", "Mixed Produce Box", "produce",
         50, "lbs", (today - timedelta(days=10)).strftime("%Y-%m-%d"),
         "Sunset", "San Francisco", None, None, ""),
        ("Harbor Hotel", "hotel", "Conference Lunch Surplus", "prepared",
         60, "portions", (today - timedelta(days=15)).strftime("%Y-%m-%d"),
         "Embarcadero", "San Francisco", None, None, ""),
        ("Golden Gate Bakery", "bakery", "Day-Old Bread", "bakery",
         20, "loaves", (today - timedelta(days=20)).strftime("%Y-%m-%d"),
         "Chinatown", "San Francisco", None, None, ""),
        ("Civic Center Cafe", "restaurant", "Soup & Stew", "prepared",
         40, "portions", (today - timedelta(days=25)).strftime("%Y-%m-%d"),
         "Civic Center", "San Francisco", None, None, ""),
        ("Farmers Market Stand", "farm", "Seasonal Fruits", "produce",
         35, "lbs", (today - timedelta(days=32)).strftime("%Y-%m-%d"),
         "Embarcadero", "San Francisco", None, None, ""),
        ("University Dining", "institution", "Student Meal Surplus", "prepared",
         90, "portions", (today - timedelta(days=38)).strftime("%Y-%m-%d"),
         "Castro", "San Francisco", None, None, ""),
        ("Airport Lounge", "institution", "Pre-Packaged Meals", "prepared",
         45, "servings", (today - timedelta(days=45)).strftime("%Y-%m-%d"),
         "SoMa", "San Francisco", None, None, ""),
        ("Tech Campus Kitchen", "institution", "Catered Lunch Leftover", "prepared",
         70, "portions", (today - timedelta(days=55)).strftime("%Y-%m-%d"),
         "Mission Bay", "San Francisco", None, None, ""),
        ("Organic Market", "grocery", "Near-Expiry Produce", "produce",
         60, "lbs", (today - timedelta(days=62)).strftime("%Y-%m-%d"),
         "Noe Valley", "San Francisco", None, None, ""),
    ]

    for idx, l in enumerate(past_listings):
        days_ago = [5, 10, 15, 20, 25, 32, 38, 45, 55, 62][idx]
        claimed_at = (today - timedelta(days=days_ago)).isoformat()
        db.execute(
            """INSERT INTO listings
               (donor_name, donor_type, food_name, food_category, quantity, unit,
                expiry_date, neighborhood, city, lat, lng, notes,
                status, claimed_at, recipient_name)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'claimed', ?, 'Community Food Bank')""",
            (*l, claimed_at)
        )
        lid = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        kg, meals, co2 = calc_impact(l[4], l[5])
        log_date = (today - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
        db.execute(
            "INSERT INTO impact_log (listing_id, food_weight_kg, meals_equivalent, co2_saved_kg, logged_at) VALUES (?, ?, ?, ?, ?)",
            (lid, kg, meals, co2, log_date)
        )

    db.commit()
    return jsonify({"success": True, "message": "Demo data seeded successfully"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
