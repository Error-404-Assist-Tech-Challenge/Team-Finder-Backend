from datetime import datetime
from typing import List

from fastapi import APIRouter, Response, Depends, Cookie, HTTPException, Header, Request
from starlette.responses import JSONResponse

from auth import AuthHandler
from Payments.models import *
import stripe, os
from database.db import db

auth_handler = AuthHandler()
payments_router = APIRouter(tags=["Stripe"])
stripe.api_key = os.environ["SSK"]
webhook_secret = os.environ["WHS"]


@payments_router.get("/pricings", response_model=Pricing)
def get_pricing_info(user_id: str = Depends(auth_handler.auth_wrapper)):
    # Fetch pricing props
    product_fetch = stripe.Product.list()
    prices_fetch = stripe.Price.list()
    product = product_fetch["data"][0]
    response_body = {"name": product.get("name"),
                     "product_id": product.get("id"),
                     "description": product.get("description"),
                     "price_list": []}
    for price in prices_fetch["data"]:
        if price["active"]:
            price_body = {"price_id": price["id"],
                          "interval": price["recurring"]["interval"],
                          "currency": price["currency"],
                          "amount": price["unit_amount"]}
            response_body["price_list"].append(price_body)
    return response_body


@payments_router.get("/membership_info", response_model=MembershipInfo)
def get_membership_info(user_id: str = Depends(auth_handler.auth_wrapper)):
    user = db.get_user(user_id)
    try:
        # Retrieve customer by email
        customers = stripe.Customer.list(email=user.get("email"))
        if customers.data:
            customer_id = customers.data[0].id  # Assuming only one customer per email
            # Retrieve subscriptions by customer ID
            subscriptions = stripe.Subscription.list(customer=customer_id)
            subscriptions = subscriptions["data"][0]
            if subscriptions:
                if subscriptions["status"] == "active":
                    currency = subscriptions.get("currency")
                    current_period_start = subscriptions.get("current_period_start")
                    current_period_end = subscriptions.get("current_period_end")

                    items = subscriptions.get("items", {}).get("data", [])
                    if items:
                        amount = items[0].get("plan", {}).get("amount")
                        interval = items[0].get("plan", {}).get("interval")
                    else:
                        amount = None
                        interval = None

                    returned_object = {
                        "currency": currency,
                        "current_period_start": datetime.utcfromtimestamp(current_period_start),
                        "current_period_end": datetime.utcfromtimestamp(current_period_end),
                        "amount": amount,
                        "interval": interval
                    }
                    return returned_object
        else:
            return None  # No customer found with the given email
    except stripe.error.StripeError as e:
        print("Stripe error:", e)
        return None


@payments_router.post("/create-checkout-session")
async def create_checkout_session(data: Plan, user_id: str = Depends(auth_handler.auth_wrapper)):
    data = data.model_dump()
    user = db.get_user(user_id)

    # Get pricing details
    pricing_details = stripe.Price.retrieve(data.get("price_id"))
    subscription_type = pricing_details["recurring"].get("interval")

    # Verify if user has a subscription
    subscriptions = get_membership_info(user_id)
    current_interval = subscriptions.get("interval")
    if subscription_type == current_interval and subscription_type == "year":
        raise HTTPException(status_code=500, detail="User already has an yearly subscription")
    elif subscription_type == 'month' and subscription_type == current_interval:
        raise HTTPException(status_code=500, detail="User already has an monthly subscription")
    elif subscription_type == "month" and "year" == current_interval:
        raise HTTPException(status_code=500, detail="User already has an yearly subscription")
    else:
        try:
            session = stripe.checkout.Session.create(
                success_url="https://google.com/",
                cancel_url="https://google.com/",
                payment_method_types=["card"],
                client_reference_id=user.get("id"),
                line_items=[
                    {
                        "price": data.get("price_id"),
                        "quantity": 1,
                    }
                ],
                mode="subscription",
            )
            return {"url": session.url}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@payments_router.post("/webhook")
async def webhook(request: Request):
    event = None
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        raise HTTPException(status_code=400, detail=str(e))
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise HTTPException(status_code=400, detail=str(e))

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Update user subscription
        session_id = session["id"]
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        organization_id = db.get_user(checkout_session["client_reference_id"]).get("org_id")
        return db.update_subscription(organization_id)

    else:
        print(f"Unhandled event type {event['type']}")

    return JSONResponse(content={"success": True})
