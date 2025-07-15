from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import cart_model
from backend.services import cart_service
from backend.data.database import get_db
from backend.services.auth_service import get_current_user 

router = APIRouter()

@router.get("/cart", response_model=cart_model.Cart_Response)
def get_cart(user_id: int, db: Session = Depends(get_db),
             current_user: dict = Depends(get_current_user)):
    
    user_id = current_user["id"]
    cart = cart_service.get_cart_total(db, user_id)

    if cart is None:
        raise HTTPException(status_code=400, detail='Empty Cart')
    
    return cart

@router.post("/cart", response_model=cart_model.Get_Cart_Item, status_code=200)
def create_item(item: cart_model.Create_Cart_Item, user_id:int, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    
    user_id = current_user["id"]
    created = cart_service.add_item(db, user_id, item.product_id, item.quantity)

    if not created:
        raise HTTPException(status_code=404, detail='Item not found')
    
    return created

@router.delete("/cart/{product_id}")
def delete_item(product_id: str, user_id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    
    user_id = current_user["id"]
    
    deleted = cart_service.remove_item(db, user_id, product_id)

    if not deleted:
        raise HTTPException(status_code=404, detail='Item not found')
    return deleted

@router.post("/checkout")
def place_order(user_id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)):
    
    user_id = current_user["id"]    
    return cart_service.checkout_cart(db, user_id)


@router.get("/orders/{user_id}")
def get_order_history(user_id: int, db: Session = Depends(get_db),
                      current_user: dict = Depends(get_current_user)):
    
    user_id = current_user["id"]
    
    orders = cart_service.get_order_history(db, user_id)
    return orders