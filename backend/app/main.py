from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from dotenv import load_dotenv
import stripe
import os

from app.models import Base
from app.db.db import get_db
from app.routes import products as product_routes
from app.stripe_routes import router as stripe_router

load_dotenv()

app = FastAPI()

# Include routers
app.include_router(stripe_router)
app.include_router(product_routes.router)

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

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}
