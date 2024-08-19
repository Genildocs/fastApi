from sqlalchemy.orm import Session
from .models import Product
from .schemas import ProductCreateSchema

def create_product(db:Session, product: ProductCreateSchema):
    db_product = Product(name=product.name, price=product.price, description=product.description )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db:Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

def get_product(db:Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

    