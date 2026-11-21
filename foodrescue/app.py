"""
FoodRescue Connect - Community food rescue coordination platform.
Connects food donors with recipients to reduce waste and fight hunger.
"""

import sqlite3
import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

DB_PATH = os.path.join(os.path.dirname(__file__), "foodrescue.db")

FOOD_CATEGORIES = [
    "Prepared Meals",
    "Baked Goods",
    "Produce",
    "Dairy",
    "Meat & Seafood",
    "Pantry Staples",
    "Beverages",
    "Other",
]

DONOR_TYPES = ["Restaurant", "Grocery Store", "Bakery", "Catering Company", "Event", "Individual", "Other"]

RECIPIENT_TYPES = ["Food Bank", "Shelter", "Community Fridge", "Soup Kitchen", "Individual", "Other"]

# Approximate CO2 saved per pound of food rescued (kg CO2e)
CO2_PER_LB = 2.5
# Average meal size in pounds
LBS_PER_MEAL = 1.2


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT NOT NULL,
            donor_type TEXT NOT NULL,
            food_description TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            expiry_date TEXT,
            pickup_address TEXT NOT NULL,
            contact_info TEXT NOT NULL,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'available',
            created_at TEXT NOT NULL,
            claimed_at TEXT,
            completed_at TEXT,
            recipient_name TEXT,
            recipient_type TEXT,
            recipient_contact TEXT
        );

        CREATE TABLE IF NOT EXISTS impact_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donation_id INTEGER NOT NULL,
            pounds_rescued REAL NOT NULL,
            logged_at TEXT NOT NULL,
            FOREIGN KEY (donation_id) REFERENCES donations(id)
        );
    """)
    conn.commit()
    conn.close()


def seed_demo_data():
    """Seed the database with realistic demo data."""
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM donations").fetchone()[0]
    if count > 0:
        conn.close()
        return

    today = date.today()
    demo_donations = [
        {
            "donor_name": "The Golden Spoon Restaurant",
            "donor_type": "Restaurant",
            "food_description": "Assorted pasta dishes, salads, and bread rolls from lunch service",
            "category": "Prepared Meals",
            "quantity": 45,
            "unit": "lbs",
            "expiry_date": today.isoformat(),
            "pickup_address": "123 Main St, Downtown",
            "contact_info": "chef@goldenspoon.com | (555) 100-2000",
            "notes": "Available for pickup after 3pm. Hot food kept warm.",
            "status": "available",
            "created_at": datetime.now().isoformat(),
        },
        {
            "donor_name": "Sunrise Bakery",
            "donor_type": "Bakery",
            "food_description": "Day-old sourdough loaves, croissants, and muffins",
            "category": "Baked Goods",
            "quantity": 30,
            "unit": "lbs",
            "expiry_date": today.isoformat(),
            "pickup_address": "456 Oak Ave, Midtown",
            "contact_info": "info@sunrisebakery.com | (555) 200-3000",
            "notes": "Perfectly good, just day-old. All sealed in bags.",
            "status": "available",
            "created_at": datetime.now().isoformat(),
        },
        {
            "donor_name": "FreshMart Supermarket",
            "donor_type": "Grocery Store",
            "food_description": "Mixed produce: carrots, zucchini, tomatoes, bell peppers - cosmetically imperfect",
            "category": "Produce",
            "quantity": 120,
            "unit": "lbs",
            "expiry_date": today.isoformat(),
            "pickup_address": "789 Elm Blvd, Westside",
            "contact_info": "donations@freshmart.com | (555) 300-4000",
            "notes": "Perfectly nutritious, pulled for cosmetic reasons. Need large vehicle.",
            "status": "claimed",
            "claimed_at": datetime.now().isoformat(),
            "recipient_name": "City Food Bank",
            "recipient_type": "Food Bank",
            "recipient_contact": "pickup@cityfoodbank.org",
            "created_at": datetime.now().isoformat(),
        },
        {
            "donor_name": "Harbor View Hotel",
            "donor_type": "Catering Company",
            "food_description": "Catering surplus from conference: sandwiches, fruit platters, cookies",
            "category": "Prepared Meals",
            "quantity": 80,
            "unit": "lbs",
            "expiry_date": today.isoformat(),
            "pickup_address": "321 Harbor Dr, Dockside",
            "contact_info": "catering@harborview.com | (555) 400-5000",
            "notes": "Conference ended early. Food in excellent condition.",
            "status": "completed",
            "claimed_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat(),
            "recipient_name": "Hope Shelter",
            "recipient_type": "Shelter",
            "recipient_contact": "meals@hopeshelter.org",
            "created_at": datetime.now().isoformat(),
        },
        {
            "donor_name": "Green Valley Farm Stand",
            "donor_type": "Individual",
            "food_description": "Surplus summer squash and herbs from home garden",
            "category": "Produce",
            "quantity": 15,
            "unit": "lbs",
            "expiry_date": today.isoformat(),
            "pickup_address": "654 Garden Ln, Suburbs",
            "contact_info": "jsmith@email.com | (555) 500-6000",
            "notes": "Freshly picked this morning. Can deliver within 2 miles.",
            "status": "available",
            "created_at": datetime.now().isoformat(),
        },
        {
            "donor_name": "Metro Diner",
            "donor_type": "Restaurant",
            "food_description": "Soup, chili, and cornbread from daily prep overage",
            "category": "Prepared Meals",
            "quantity": 25,
            "unit": "lbs",
            "expiry_date": today.isoformat(),
            "pickup_address": "987 Central Ave, Midtown",
            "contact_info": "metro.diner@gmail.com | (555) 600-7000",
            "notes": "Ready at 8pm after close. Ring back doorbell.",
            "status": "completed",
            "claimed_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat(),
            "recipient_name": "St. Mary's Community Kitchen",
            "recipient_type": "Soup Kitchen",
            "recipient_contact": "kitchen@stmarys.org",
            "created_at": datetime.now().isoformat(),
        },
    ]

    for d in demo_donations:
        cols = ", ".join(d.keys())
        placeholders = ", ".join(["?"] * len(d))
        conn.execute(
            f"INSERT INTO donations ({cols}) VALUES ({placeholders})",
            list(d.values()),
        )

    # Seed impact log for completed donations
    completed = conn.execute(
        "SELECT id, quantity FROM donations WHERE status = 'completed'"
    ).fetchall()
    for row in completed:
        conn.execute(
            "INSERT INTO impact_log (donation_id, pounds_rescued, logged_at) VALUES (?, ?, ?)",
            (row["id"], row["quantity"], datetime.now().isoformat()),
        )

    conn.commit()
    conn.close()


def calculate_impact(total_lbs):
    """Return impact metrics from total pounds rescued."""
    return {
        "pounds": round(total_lbs, 1),
        "meals": round(total_lbs / LBS_PER_MEAL),
        "co2_kg": round(total_lbs * CO2_PER_LB, 1),
        "co2_lbs": round(total_lbs * CO2_PER_LB * 2.205, 1),
    }


@app.route("/")
def index():
    conn = get_db()
    total_lbs = conn.execute(
        "SELECT COALESCE(SUM(pounds_rescued), 0) FROM impact_log"
    ).fetchone()[0]
    rescues = conn.execute(
        "SELECT COUNT(*) FROM donations WHERE status = 'completed'"
    ).fetchone()[0]
    active = conn.execute(
        "SELECT COUNT(*) FROM donations WHERE status = 'available'"
    ).fetchone()[0]
    recent = conn.execute(
        "SELECT * FROM donations ORDER BY created_at DESC LIMIT 4"
    ).fetchall()
    conn.close()

    impact = calculate_impact(total_lbs)
    return render_template(
        "index.html",
        impact=impact,
        rescues=rescues,
        active_listings=active,
        recent=recent,
    )


@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        data = {
            "donor_name": request.form["donor_name"].strip(),
            "donor_type": request.form["donor_type"],
            "food_description": request.form["food_description"].strip(),
            "category": request.form["category"],
            "quantity": float(request.form["quantity"]),
            "unit": request.form["unit"],
            "expiry_date": request.form.get("expiry_date", ""),
            "pickup_address": request.form["pickup_address"].strip(),
            "contact_info": request.form["contact_info"].strip(),
            "notes": request.form.get("notes", "").strip(),
            "status": "available",
            "created_at": datetime.now().isoformat(),
        }

        if not all([data["donor_name"], data["food_description"], data["pickup_address"], data["contact_info"]]):
            flash("Please fill in all required fields.", "error")
            return render_template("donate.html", food_categories=FOOD_CATEGORIES, donor_types=DONOR_TYPES, form=request.form)

        conn = get_db()
        conn.execute(
            """INSERT INTO donations
               (donor_name, donor_type, food_description, category, quantity, unit,
                expiry_date, pickup_address, contact_info, notes, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [data[k] for k in ["donor_name", "donor_type", "food_description", "category",
                                "quantity", "unit", "expiry_date", "pickup_address",
                                "contact_info", "notes", "status", "created_at"]],
        )
        conn.commit()
        conn.close()
        flash(f"Thank you! Your donation of {data['quantity']} {data['unit']} has been listed.", "success")
        return redirect(url_for("listings"))

    return render_template("donate.html", food_categories=FOOD_CATEGORIES, donor_types=DONOR_TYPES)


@app.route("/listings")
def listings():
    category = request.args.get("category", "")
    conn = get_db()
    if category:
        rows = conn.execute(
            "SELECT * FROM donations WHERE status = 'available' AND category = ? ORDER BY expiry_date ASC, created_at DESC",
            (category,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM donations WHERE status = 'available' ORDER BY expiry_date ASC, created_at DESC"
        ).fetchall()
    conn.close()
    return render_template("listings.html", donations=rows, categories=FOOD_CATEGORIES, selected_category=category)


@app.route("/claim/<int:donation_id>", methods=["GET", "POST"])
def claim(donation_id):
    conn = get_db()
    donation = conn.execute("SELECT * FROM donations WHERE id = ?", (donation_id,)).fetchone()
    if not donation or donation["status"] != "available":
        flash("This donation is no longer available.", "error")
        conn.close()
        return redirect(url_for("listings"))

    if request.method == "POST":
        recipient_name = request.form["recipient_name"].strip()
        recipient_type = request.form["recipient_type"]
        recipient_contact = request.form["recipient_contact"].strip()

        if not all([recipient_name, recipient_contact]):
            flash("Please fill in all required fields.", "error")
            conn.close()
            return render_template("claim.html", donation=donation, recipient_types=RECIPIENT_TYPES)

        conn.execute(
            """UPDATE donations SET
               status = 'claimed', claimed_at = ?, recipient_name = ?,
               recipient_type = ?, recipient_contact = ?
               WHERE id = ?""",
            (datetime.now().isoformat(), recipient_name, recipient_type, recipient_contact, donation_id),
        )
        conn.commit()
        conn.close()
        flash(f"Donation claimed! Contact the donor at {donation['contact_info']} to arrange pickup.", "success")
        return redirect(url_for("listings"))

    conn.close()
    return render_template("claim.html", donation=donation, recipient_types=RECIPIENT_TYPES)


@app.route("/complete/<int:donation_id>", methods=["POST"])
def complete(donation_id):
    conn = get_db()
    donation = conn.execute("SELECT * FROM donations WHERE id = ?", (donation_id,)).fetchone()
    if donation and donation["status"] == "claimed":
        conn.execute(
            "UPDATE donations SET status = 'completed', completed_at = ? WHERE id = ?",
            (datetime.now().isoformat(), donation_id),
        )
        conn.execute(
            "INSERT INTO impact_log (donation_id, pounds_rescued, logged_at) VALUES (?, ?, ?)",
            (donation_id, donation["quantity"] if donation["unit"] == "lbs" else donation["quantity"] * 0.5, datetime.now().isoformat()),
        )
        conn.commit()
        flash(f"Rescue confirmed! {donation['quantity']} {donation['unit']} of food rescued.", "success")
    conn.close()
    return redirect(url_for("impact"))


@app.route("/impact")
def impact():
    conn = get_db()
    total_lbs = conn.execute(
        "SELECT COALESCE(SUM(pounds_rescued), 0) FROM impact_log"
    ).fetchone()[0]
    by_category = conn.execute(
        """SELECT d.category, COUNT(*) as count, SUM(il.pounds_rescued) as total_lbs
           FROM impact_log il JOIN donations d ON il.donation_id = d.id
           GROUP BY d.category ORDER BY total_lbs DESC""",
    ).fetchall()
    recent_rescues = conn.execute(
        """SELECT d.donor_name, d.food_description, d.recipient_name, d.recipient_type,
                  il.pounds_rescued, il.logged_at
           FROM impact_log il JOIN donations d ON il.donation_id = d.id
           ORDER BY il.logged_at DESC LIMIT 10""",
    ).fetchall()
    total_donors = conn.execute(
        "SELECT COUNT(DISTINCT donor_name) FROM donations WHERE status = 'completed'"
    ).fetchone()[0]
    total_recipients = conn.execute(
        "SELECT COUNT(DISTINCT recipient_name) FROM donations WHERE status IN ('claimed', 'completed')"
    ).fetchone()[0]
    conn.close()

    metrics = calculate_impact(total_lbs)
    return render_template(
        "impact.html",
        metrics=metrics,
        by_category=by_category,
        recent_rescues=recent_rescues,
        total_donors=total_donors,
        total_recipients=total_recipients,
    )


@app.route("/api/stats")
def api_stats():
    conn = get_db()
    total_lbs = conn.execute(
        "SELECT COALESCE(SUM(pounds_rescued), 0) FROM impact_log"
    ).fetchone()[0]
    active = conn.execute(
        "SELECT COUNT(*) FROM donations WHERE status = 'available'"
    ).fetchone()[0]
    conn.close()
    impact = calculate_impact(total_lbs)
    impact["active_listings"] = active
    return jsonify(impact)


if __name__ == "__main__":
    init_db()
    seed_demo_data()
    app.run(debug=True, host="0.0.0.0", port=5000)
