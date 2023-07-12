from fastapi import APIRouter, Body
from api.model import BookSchema

router = APIRouter()

books = {}


@router.get("/")
def get_books() -> dict:
    return {"data": books}


@router.get("/{id}")
async def get_book(id: str) -> dict:
    if id not in books:
        return {"error": "Invalid book ID"}
    return {"data": books[id]}


@router.post("/")
def add_book(book: BookSchema = Body(...)) -> dict:
    book_id = str(len(books) + 1)
    books[book_id] = book.dict()
    return {"message": f"Book {book_id} added successfully", "book_id": book_id}
