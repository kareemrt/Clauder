import os
import json
from datetime import datetime, date, timedelta
from flask import Flask, request, jsonify, render_template
from database import db, Item, WasteLog, init_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///freshsave.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


def get_claude_recipes(items):
    """Call Claude API to get recipe suggestions for expiring items."""
    if not ANTHROPIC_API_KEY:
        return _mock_recipes(items)

    import anthropic

    ingredient_list = "\n".join(
        f"- {item['name']} ({item['quantity']} {item['unit']}, expires {item['expiry_date']})"
        for item in items
    )

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a creative chef helping reduce food waste.
I have these ingredients expiring soon:

{ingredient_list}

Please suggest 3 practical recipes that use as many of these ingredients as possible.
For each recipe provide:
1. Recipe name
2. Brief description (1-2 sentences)
3. Ingredients used from my list (mark which ones from the expiring list)
4. Simple steps (3-5 steps)
5. Estimated prep + cook time

Format as JSON with this structure:
{{
  "recipes": [
    {{
      "name": "Recipe Name",
      "description": "Brief description",
      "uses_expiring": ["item1", "item2"],
      "ingredients": ["ingredient1", "ingredient2"],
      "steps": ["step1", "step2"],
      "time": "30 minutes"
    }}
  ]
}}""",
            }
        ],
    )

    try:
        content = message.content[0].text
        # Extract JSON from response
        start = content.find("{")
        end = content.rfind("}") + 1
        return json.loads(content[start:end])
    except Exception:
        return _mock_recipes(items)


def _mock_recipes(items):
    """Fallback recipes when API key not available."""
    names = [item["name"] for item in items[:3]]
    ingredient_str = ", ".join(names) if names else "your ingredients"
    return {
        "recipes": [
            {
                "name": f"Quick {names[0] if names else 'Pantry'} Stir-Fry",
                "description": f"A simple stir-fry using {ingredient_str} to minimize waste.",
                "uses_expiring": names[:2],
                "ingredients": names + ["olive oil", "garlic", "salt", "pepper"],
                "steps": [
                    "Heat oil in a pan over medium-high heat",
                    "Add garlic and cook 1 minute",
                    f"Add {ingredient_str} and stir-fry 5-7 minutes",
                    "Season with salt and pepper",
                    "Serve immediately",
                ],
                "time": "15 minutes",
            },
            {
                "name": "Waste-Free Soup",
                "description": "A hearty soup that uses everything in your pantry.",
                "uses_expiring": names,
                "ingredients": names + ["vegetable broth", "onion", "herbs"],
                "steps": [
                    "Sauté onion until soft",
                    f"Add {ingredient_str} and cook 3 minutes",
                    "Pour in broth and bring to boil",
                    "Simmer 20 minutes",
                    "Blend or serve chunky",
                ],
                "time": "30 minutes",
            },
        ]
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/items", methods=["GET"])
def get_items():
    status = request.args.get("status", "active")
    items = Item.query.filter_by(status=status).order_by(Item.expiry_date).all()
    return jsonify([item.to_dict() for item in items])


@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    expiry = datetime.strptime(data["expiry_date"], "%Y-%m-%d").date()
    item = Item(
        name=data["name"],
        quantity=float(data.get("quantity", 1)),
        unit=data.get("unit", "unit"),
        expiry_date=expiry,
        category=data.get("category", "other"),
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    new_status = data.get("status")

    if new_status in ("used", "wasted"):
        log = WasteLog(
            item_id=item.id,
            item_name=item.name,
            quantity=item.quantity,
            unit=item.unit,
            outcome=new_status,
            category=item.category,
        )
        db.session.add(log)
        item.status = new_status

    db.session.commit()
    return jsonify(item.to_dict())


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"deleted": True})


@app.route("/api/recipes", methods=["POST"])
def get_recipes():
    data = request.get_json()
    item_ids = data.get("item_ids", [])

    if item_ids:
        items = Item.query.filter(Item.id.in_(item_ids)).all()
    else:
        # Default: items expiring within 5 days
        cutoff = date.today() + timedelta(days=5)
        items = Item.query.filter(
            Item.status == "active", Item.expiry_date <= cutoff
        ).all()

    if not items:
        return jsonify({"error": "No items selected"}), 400

    recipes = get_claude_recipes([i.to_dict() for i in items])
    return jsonify(recipes)


@app.route("/api/stats", methods=["GET"])
def get_stats():
    all_logs = WasteLog.query.all()
    total_saved = sum(l.quantity for l in all_logs if l.outcome == "used")
    total_wasted = sum(l.quantity for l in all_logs if l.outcome == "wasted")
    total_items = Item.query.count()
    active_items = Item.query.filter_by(status="active").count()

    expiring_soon = Item.query.filter(
        Item.status == "active",
        Item.expiry_date <= date.today() + timedelta(days=3),
    ).count()

    # Category breakdown of waste
    category_waste = {}
    for log in all_logs:
        if log.outcome == "wasted":
            category_waste[log.category] = category_waste.get(log.category, 0) + 1

    # Waste reduction rate
    total_logged = total_saved + total_wasted
    rescue_rate = round((total_saved / total_logged * 100) if total_logged > 0 else 0, 1)

    return jsonify(
        {
            "total_items": total_items,
            "active_items": active_items,
            "expiring_soon": expiring_soon,
            "items_saved": int(total_saved),
            "items_wasted": int(total_wasted),
            "rescue_rate": rescue_rate,
            "category_waste": category_waste,
            # Average household wastes ~$1,500/year; each saved item ~$3
            "estimated_savings_usd": round(total_saved * 3, 2),
            "co2_saved_kg": round(total_saved * 0.5, 2),  # ~0.5kg CO2 per food item
        }
    )


if __name__ == "__main__":
    with app.app_context():
        init_db(app)
    app.run(debug=True, host="0.0.0.0", port=5000)
