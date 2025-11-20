from pydantic import BaseModel
from typing import Optional

class FilterBase(BaseModel):
    name: str
    query: str
    color: str = "grey"
    is_favorite: bool = False

class FilterCreate(FilterBase):
    pass

class Filter(FilterBase):
    id: int

    class Config:
        orm_mode = True
