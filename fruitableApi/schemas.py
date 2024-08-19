from pydantic import BaseModel

class ProductCreateSchema(BaseModel):
    id: int
    name: str
    price: int
    description: str

class ProductResponseSchema(BaseModel):
    id: int
    name: str
    price: int
    description: str

    class Config:
        orm_mode=True

