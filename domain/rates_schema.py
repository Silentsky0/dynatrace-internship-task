from pydantic import BaseModel


class MinMaxAverageSchema(BaseModel):
    min: float
    max: float
