from fastapi import APIRouter, Body, HTTPException
from .model import BookSchema

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
    if len(books) >= 100:
        raise HTTPException(status_code=400, detail="Maximum number of books reached.")
    book_id = str(len(books) + 1)
    books[book_id] = book.dict()
    return {"message": f"Book {book_id} added successfully", "book_id": book_id}


@router.delete("/{id}")
def delete_book(id: str) -> dict:
    if id not in books:
        raise HTTPException(status_code=400, detail="Invalid book ID")
    del books[id]
    return {"message": f"Book {id} deleted successfully"}
