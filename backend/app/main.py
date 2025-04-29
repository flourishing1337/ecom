from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Product

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
DATABASE_URL = "postgresql://postgres:password@db:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
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
    return [{"id": p.id, "name": p.name, "price": p.price} for p in products]

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
