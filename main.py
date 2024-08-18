from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    description: str | None = None

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html",{
        "request": request,
        "title": "Fruitables",
        "message": "Fake api of fruit and vegetable products"
    })

@app.get("/api/v1/products")
async def list_products():
    return {"message: Products not found"}

@app.get("/api/v1/products/{item_id}")
async def read_item(item_id: int):
    if type(item_id) == int:
        return {"item_id": item_id}
    else:
        return {"message": "Item not found"}


@app.post("/api/v1/products")
async def create_product(product: Product):
    return product

@app.delete("/api/v1/products/{item_id}")
async def delete_item(item_id: int):
    return {"message: No items to delete"}