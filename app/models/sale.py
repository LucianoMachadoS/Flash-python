from pydantic import BaseModel
from datetime import date

class Sale(BaseModel):
    product_id: str
    quantity: int
    sale_date: date
    total_value: float