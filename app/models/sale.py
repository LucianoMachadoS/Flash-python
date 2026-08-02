from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime, time

class Sale(BaseModel):
    product_id: str = Field(min_length=1)
    quantity: int
    sale_date: date
    total_value: float

    model_config = ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True
        )

    def to_mongo(self) -> dict:
        data = self.model_dump()
        # O BSON não possui um tipo `date`, apenas `datetime`
        data['sale_date'] = datetime.combine(self.sale_date, time.min)
        return data
