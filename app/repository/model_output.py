from typing import Optional
from pydantic import BaseModel

class Dialog(BaseModel):
    id: int
    dialog: str

    class Config:
        from_attributes = True