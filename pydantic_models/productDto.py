from pydantic import BaseModel

class ProductDto(BaseModel):
    id: str
    name: str
    price: float
    description: str
    in_stock: bool



    