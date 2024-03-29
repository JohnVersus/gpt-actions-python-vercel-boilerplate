from typing import Optional, Dict
from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    publication_year: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Inferno",
                "author": "Dan Brown",
                "description": "A thrilling book about symbology and secret societies.",
                "publication_year": 2013,
            }
        }


class BookResponse(BaseModel):
    data: Dict[str, BookSchema]


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str
