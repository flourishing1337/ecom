from app.db.db import SessionLocal
from app.models import Product

def seed():
    db = SessionLocal()

    products = [
        Product(
            name="Eco T-Shirt",
            description="Organic cotton T-shirt",
            price_cents=2900,
            image_url="https://via.placeholder.com/400x400.png?text=Eco+T-Shirt"
        ),
        Product(
            name="Reusable Bottle",
            description="Insulated water bottle",
            price_cents=3500,
            image_url="https://via.placeholder.com/400x400.png?text=Reusable+Bottle"
        )
    ]

    db.add_all(products)
    db.commit()
    db.close()
    print("✅ Seeded test products!")

if __name__ == "__main__":
    seed()
