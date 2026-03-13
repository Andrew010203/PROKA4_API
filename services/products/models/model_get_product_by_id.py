from pydantic import BaseModel

class ProductResponse(BaseModel):
    category: str
    description: str
    id: int
    image_url: str
    name: str
    price: float
    rating: float
    reviews_count: int
    stock: int