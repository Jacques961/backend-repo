from sqlalchemy.orm import Session 
from backend.models.product_model import Create_Product
from backend.data.database import Product_db
import uuid
import time
import hashlib

def get_all_products(db: Session):
    all_products = db.query(Product_db).all()

    if all_products is None:
        return None
    
    return all_products


def get_product_by_id(db: Session, product_id: str):
    product = db.query(Product_db).filter(Product_db.id == product_id).first()

    if product is None:
        return None
    
    return product

def get_prodcts_by_category(db: Session, category: str):
    all_products = db.query(Product_db).filter(Product_db.category == category).all()

    if not all_products:
        return None
    
    return all_products 

def create_new_product(db: Session, product: Create_Product):
    first_char = product.category[0].upper()
    base = str(uuid.uuid4()) + str(time.time())
    hash_str = hashlib.sha256(base.encode()).hexdigest()

    id = first_char + hash_str[:3]

    new_product = Product_db(id=id, **product.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

def update_product(db:Session, product: Create_Product, product_id: str):
    product_to_update = db.query(Product_db).filter(Product_db.id == product_id).first()

    if product_to_update is None:
        return None
    
    if product.name != 'string':
        product_to_update.name = product.name
    if product.category != 'string':
        product_to_update.category = product.category
    if product.price != 0.0:
        product_to_update.price = product.price
    if product.image != 'string':
        product_to_update.image = product.image
    
    db.commit()
    db.refresh(product_to_update)
    return product_to_update

def delete_product(db: Session, product_id: str):
    product_to_delete = db.query(Product_db).filter(Product_db.id == product_id).first()

    if product_to_delete is None:
        return None
    
    db.delete(product_to_delete)
    db.commit()
    return product_to_delete