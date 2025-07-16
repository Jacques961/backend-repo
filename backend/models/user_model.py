from pydantic import BaseModel

class Base_User(BaseModel):
    name: str

class Create_User(Base_User):
    password: str
    is_admin: bool = False

class Get_User(Base_User):
    id: int

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    is_admin: bool  

    class Config:
        orm_mode = True