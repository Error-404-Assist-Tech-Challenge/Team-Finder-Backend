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


@payments_router.post("/create-checkout-session")
async def create_checkout_session(data: Plan, user_id: str = Depends(auth_handler.auth_wrapper)):
    data = data.model_dump()
    user = db.get_user(user_id)
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
