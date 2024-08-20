from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas

def create_product(db:Session, product: schemas.ProductCreateSchema):
    db_product = models.Product(name=product.name, price=product.price, description=product.description )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db:Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def get_product(db:Session, product_id: int):        
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def delete_product(db:Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product deleted")
    if db_product:       
        db.delete(db_product)
        db.commit() 
        
    return db_product
    