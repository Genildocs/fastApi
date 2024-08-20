from itertools import product
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, defer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from . import models, schemas, crud
from .crud import get_products
from .database import engine, SessionLocal
from .schemas import ProductCreateSchema, ProductResponseSchema

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/fruitableApi/static", StaticFiles(directory="fruitableApi/static"), name="static")
templates = Jinja2Templates(directory="fruitableApi/templates")

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", 
                                      {"request": request,
                                       "title": "Fruitables Api",
                                       "message": "Welcome to the Fruitables Api"
                                       })

@app.post("/api/v1/products", response_model=schemas.ProductResponseSchema)
def create_product(product: schemas.ProductCreateSchema, db:Session = Depends(get_db)):    
    db_product = crud.get_product(db, product_id=product.id)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already registered")  
    return crud.create_product(db=db, product=product)

@app.get("/api/v1/products", response_model=list[schemas.ProductResponseSchema])
def read_products(skip: int= 0, limit: int= 10, db: Session = Depends(get_db)):   
    products = crud.get_products(db,skip=skip,limit=limit)
    if products is None:
        raise HTTPException(status_code=404, detail="Products not found")
    return products

@app.get("/api/v1/product/{product_id}", response_model=schemas.ProductResponseSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):    
    product = crud.get_product(db, product_id)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")    
    return product


@app.delete("/api/v1/product/{product_id}", response_model=schemas.ProductResponseSchema)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.delete_product(db, product_id)
    return product 