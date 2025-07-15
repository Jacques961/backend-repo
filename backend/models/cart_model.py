from pydantic import BaseModel
from backend.models import product_model

class Base_Cart_Item(BaseModel):
    product_id: str
    quantity: int

class Create_Cart_Item(Base_Cart_Item):
    pass

class Get_Cart_Item(BaseModel):
    id: int
    product: product_model.Get_Product
    quantity: int

    class Config:
        from_attributes = True


class Cart_Response(BaseModel):
    items: list[Get_Cart_Item]
    total: float