from pydantic import BaseModel

class ProductCreateSchema(BaseModel):
    id: int
    name: str
    price: int
    description: str
    category: str
    quantity: int
    disponible: bool

class ProductResponseSchema(BaseModel):
    id: int
    name: str
    price: int
    description: str
    category: str
    quantity: int
    disponible: bool

    class Config:
        orm_mode=True

