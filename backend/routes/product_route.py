from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import product_model
from backend.services import product_service, auth_service
from backend.data.database import get_db

router = APIRouter()

@router.get("/products", response_model=list[product_model.Get_Product])
def get_products(db: Session = Depends(get_db)):
    all_products = product_service.get_all_products(db)

    if not all_products:
        raise HTTPException(status_code=404, detail="NO PRODUCTS FOUND")
    
    return all_products

@router.get("/products/{product_id}", response_model=product_model.Get_Product)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="PRODUCT NOT FOUND")
    
    return product


@router.get("/products/category/{category}", response_model=list[product_model.Get_Product])
def get_products_by_catgory(category:str, db: Session = Depends(get_db)):
    all_products = product_service.get_prodcts_by_category(db, category)

    if not all_products:
        raise HTTPException(status_code=404, detail="NO PRODUCTS FOUND")

    return all_products
        
@router.post("/products", response_model=product_model.Get_Product, status_code=200)
def create_product(product: product_model.Create_Product, db: Session = Depends(get_db),
                   current_user: dict = Depends(auth_service.get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="You do not have permission to add products")
    return product_service.create_new_product(db, product)

@router.put("/products/{product_id}", response_model=product_model.Get_Product)
def update_product(product: product_model.Create_Product, product_id:str, db: Session = Depends(get_db),
                   current_user: dict = Depends(auth_service.get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="You do not have permission to update products")
    
    product = product_service.update_product(db, product, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="PRODUCT NOT FOUND")
    
    return product

@router.delete("/products/{product_id}", response_model=product_model.Get_Product)
def delete_product(product_id:str, db: Session = Depends(get_db),
                   current_user: dict = Depends(auth_service.get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="You do not have permission to delete products")
    
    product = product_service.delete_product(db, product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="PRODUCT NOT FOUND")
    
    return product