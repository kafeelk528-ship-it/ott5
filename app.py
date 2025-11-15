from flask import Flask, render_template, request, redirect, url_for
import stripe
import os

app = Flask(__name__)

# Stripe keys from Render environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")

# Fake plans (you can replace with database later)
plans = [
    {"id": 1, "name": "Netflix Basic", "price": 199},
    {"id": 2, "name": "Amazon Prime", "price": 149},
    {"id": 3, "name": "Hotstar Premium", "price": 299},
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/plans")
def show_plans():
    return render_template("plans.html", plans=plans)


@app.route("/plan/<int:id>")
def plan_details(id):
    for p in plans:
        if p["id"] == id:
            return render_template("plan-details.html", plan=p)
    return "Plan not found"


@app.route("/create-checkout-session/<int:id>")
def create_checkout_session(id):
    for p in plans:
        if p["id"] == id:
            selected_plan = p

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {'name': selected_plan["name"]},
                'unit_amount': selected_plan["price"] * 100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('success', _external=True),
        cancel_url=url_for('show_plans', _external=True)
    )

    return redirect(checkout_session.url, code=303)


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
