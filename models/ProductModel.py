from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    created_at: str
    created_by: str
    updated_at: str
    updated_by: str
    status: str