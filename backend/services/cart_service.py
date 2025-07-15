from backend.models import user_model
from backend.data.database import Product_db, Cart_db, User_db, Checkout_db, CheckoutItem_db
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime

def add_item(db: Session, user_id: int, product_id: str, quantity: int):
    get_user = db.query(User_db).filter(User_db.id == user_id).first()

    if get_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")
    
    product = db.query(Product_db).filter(Product_db.id == product_id).first()

    if not product:
        return None
    
    cart_item = db.query(Cart_db).filter(
        Cart_db.product_id == product_id,
        Cart_db.user_id == user_id
        ).first()

    if cart_item:
        cart_item.quantity += quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item
    
    cart_item = Cart_db(product_id=product_id, user_id=user_id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item
    
def remove_item(db: Session, user_id: int, product_id: str):
    get_user = db.query(User_db).filter(User_db.id == user_id).first()

    if get_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    product = db.query(Cart_db).filter(
        Cart_db.product_id == product_id,
        Cart_db.user_id == user_id
        ).first()

    if not product:
        return None

    db.delete(product)
    db.commit()

    return {"message": f"Product {product_id} deleted"}

def get_cart_total(db: Session, user_id: int):
    get_user = db.query(User_db).filter(User_db.id == user_id).first()

    if get_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    items = db.query(Cart_db).options(
        joinedload(Cart_db.product)
        ).filter(Cart_db.user_id == user_id).all()

    if not items:
        return None
    
    total = sum(item.product.price * item.quantity for item in items)
    return {"items": items, "total": total}


def checkout_cart(db : Session, user_id:int):
    get_user = db.query(User_db).filter(User_db.id == user_id).first()

    if get_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    items = db.query(Cart_db).options(
        joinedload(Cart_db.product)
        ).filter(Cart_db.user_id == user_id).all()
    
    if not items:
        return None

    total = sum(item.product.price * item.quantity for item in items)
    
    checkout = Checkout_db(user_id=user_id, total_price=total)
    db.add(checkout)
    db.commit()
    db.refresh(checkout)
    
    for item in items:
        checkout_item = CheckoutItem_db(
            checkout_id=checkout.id,
            product_id=item.product.id,
            quantity=item.quantity,
            unit_price=item.product.price
        )
        db.add(checkout_item)
        
    for item in items:
        db.delete(item)

    db.commit()

    return {
        "message": "Checkout saved successfully",
        "checkout_id": checkout.id,
        "user": {"id": get_user.id, "name": get_user.name},
        "total": total
    }

# def get_order_history(db: Session, user_id: int):
#     orders = db.query(Checkout_db).filter(Checkout_db.user_id == user_id).all()
#     return orders

def get_order_history(db: Session, user_id: int):
    # Step 1: Get all checkout sessions for this user
    checkouts = db.query(Checkout_db).filter(
        Checkout_db.user_id == user_id
    ).all()

    order_history = []

    for checkout in checkouts:
        # Step 2: For each checkout, get its associated items + product info
        items = db.query(CheckoutItem_db).options(
            joinedload(CheckoutItem_db.product)  # Load product details
        ).filter(
            CheckoutItem_db.checkout_id == checkout.id
        ).all()

        # Step 3: Format each item with details
        item_list = [
            {
                "product_id": item.product_id,
                "product_name": item.product.name,   # assuming product has `name`
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total": item.quantity * item.unit_price,
                "date": checkout.timestamp
            }
            for item in items
        ]

        # Step 4: Add to the history list
        order_history.append({
            "checkout_id": checkout.id,
            "total_price": checkout.total_price,
            "items": item_list
        })

    return order_history