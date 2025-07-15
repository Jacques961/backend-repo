from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///myapp.db', echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class Product_db(Base):
    __tablename__ = 'products'

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    price = Column(Float)
    image = Column(String)

class Cart_db(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, ForeignKey('products.id'))
    quantity = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey('users.id'))

    product = relationship('Product_db')
    user = relationship('User_db')

class User_db(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    hashed_pass = Column(String)
    is_admin = Column(Boolean, default=False)
    checkouts = relationship("Checkout_db")
    
class Checkout_db(Base):
    __tablename__ = 'checkouts'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total_price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User_db")
    items = relationship("CheckoutItem_db")

class CheckoutItem_db(Base):
    __tablename__ = 'checkout_items'
    
    id = Column(Integer, primary_key=True, index=True)
    checkout_id = Column(Integer, ForeignKey('checkouts.id'))
    product_id = Column(String, ForeignKey('products.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)
    
    checkout = relationship("Checkout_db")
    product = relationship("Product_db")

