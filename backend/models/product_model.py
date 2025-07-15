from pydantic import BaseModel

class Base_Product(BaseModel):
    name: str
    category: str
    price: float
    image: str

class Create_Product(Base_Product):
    pass 

class Get_Product(Base_Product):
    id: str

    class Config:
        from_attributes = True