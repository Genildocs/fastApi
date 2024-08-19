from itertools import product

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .crud import get_products
from .database import engine, SessionLocal
from .schemas import ProductCreateSchema, ProductResponseSchema

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def index():
    return {"message": {"Teste"}}

@app.post("/api/v1/products", response_model=schemas.ProductResponseSchema)
async def create_product(product: schemas.ProductCreateSchema, db:Session = Depends(get_db)):
    db_product = crud.get_products(db, product_id=product.name)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already registered")
    return crud.create_product(db=db, product=product)

@app.get("/api/v1/products", response_model=list[schemas.ProductResponseSchema])
async def read_products(skip: int= 0, limit: int= 10, db: Session = Depends(get_db)):
    products = crud.get_products(db,skip=skip,limit=limit)
    if products is None:
        raise HTTPException(status_code=404, detail="Products not found")
    return products
