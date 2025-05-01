# backend/app/stripe_routes.py

import os
import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter()

class CheckoutRequest(BaseModel):
    product_name: str
    price: int  # in cents
    currency: str = "usd"

@router.post("/create-checkout-session")
def create_checkout_session(data: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": data.currency,
                    "product_data": {"name": data.product_name},
                    "unit_amount": data.price,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
        )
        return {"id": session.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
