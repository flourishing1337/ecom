from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from dotenv import load_dotenv
import stripe
import os

from app.models import Base, Product
from app.stripe_routes import router as stripe_router

load_dotenv()

app = FastAPI()
app.include_router(stripe_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hobbyhosting.org", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/postgres")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class CheckoutRequest(BaseModel):
    product_name: str
    price_cents: int  # e.g., 2000 = $20.00
    currency: str = "usd"

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products")
def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    return [{"id": p.id, "name": p.name, "price": p.price_cents / 100} for p in products]


@app.post("/create-checkout-session")
def create_checkout_session(data: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": data.currency,
                    "product_data": {"name": data.product_name},
                    "unit_amount": data.price_cents,
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
