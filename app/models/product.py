from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId

class Product(BaseModel):
    id: Optional[ObjectId] = Field(None, alias='_id')
    name: str
    price: float
    description: Optional[str] = None
    stock: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class ProductDBModel(Product):
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if '_id' in data and isinstance(data['_id'], ObjectId):
            data['_id'] = str(data['_id'])
        return data

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None