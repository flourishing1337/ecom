from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.db.db import get_db
from app.models import Order, OrderItem

router = APIRouter()

@router.get("/orders")
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).options(
        joinedload(Order.items).joinedload(OrderItem.product)
    ).order_by(Order.created_at.desc()).all()

    return [
        {
            "order_id": order.id,
            "status": order.status,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "items": [
                {
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price
                }
                for item in order.items
            ]
        }
        for order in orders
    ]
