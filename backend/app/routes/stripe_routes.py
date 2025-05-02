from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
import stripe
import os

from app.db.db import get_db
from app.models import Order, OrderItem, Product

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

class OrderRequest(stripe.util.convert_to_stripe_object):
    product_id: int
    quantity: int

@router.post("/create-checkout-session")
def create_checkout_session(data: OrderRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    order = Order(
        stripe_session_id="placeholder",
        total_amount=product.price_cents * data.quantity / 100,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    db.add(OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=data.quantity,
        unit_price=product.price_cents
    ))
    db.commit()

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": product.name},
                "unit_amount": product.price_cents,
            },
            "quantity": data.quantity,
        }],
        mode="payment",
        success_url="https://hobbyhosting.org/success",
        cancel_url="https://hobbyhosting.org/cancel",
        metadata={"order_id": str(order.id)},
    )

    order.stripe_session_id = session.id
    db.commit()

    return {"id": session.id}


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session.get("metadata", {}).get("order_id")
        if order_id:
            order = db.query(Order).filter(Order.id == int(order_id)).first()
            if order:
                order.status = "paid"
                db.commit()

    return {"status": "ok"}
