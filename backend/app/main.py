from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Product

app = FastAPI()

# Allow frontend in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hobbyhosting.org"],  # ✅ Use your real domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "postgresql://postgres:password@db:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Auto-create tables at startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Get all products
@app.get("/products")
def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    return [{"id": p.id, "name": p.name, "price": p.price} for p in products]

# Seed test products
@app.post("/seed")
def seed_products():
    db = SessionLocal()
    sample_products = [
        Product(name="Sample T-Shirt", price=19.99),
        Product(name="Coffee Mug", price=9.99),
        Product(name="Baseball Cap", price=14.99),
    ]
    db.add_all(sample_products)
    db.commit()
    return {"message": f"Added {len(sample_products)} products"}
