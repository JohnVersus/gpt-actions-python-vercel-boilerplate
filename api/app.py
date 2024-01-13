# This is an example API. Replace with your custom API code
from fastapi import APIRouter, Body, HTTPException
from .model import BookResponse, BookSchema, MessageResponse, ErrorResponse
from fastapi.responses import JSONResponse

router = APIRouter()

books = {}


@router.get("/", response_model=BookResponse)
def get_books() -> BookResponse:
    return BookResponse(data=books)


@router.get(
    "/{id}", response_model=BookResponse, responses={404: {"model": ErrorResponse}}
)
async def get_book(id: str) -> dict:
    if id not in books:
        return JSONResponse(status_code=404, content={"error": "Invalid book ID"})
    return BookResponse(data={id: books[id]})


@router.post(
    "/", response_model=MessageResponse, responses={400: {"model": ErrorResponse}}
)
def add_book(book: BookSchema) -> MessageResponse:
    if len(books) >= 100:
        raise HTTPException(status_code=400, detail="Maximum number of books reached.")
    book_id = str(len(books) + 1)
    books[book_id] = book.dict()
    return MessageResponse(message=f"Book {book_id} added successfully")


@router.delete(
    "/{id}", response_model=MessageResponse, responses={400: {"model": ErrorResponse}}
)
def delete_book(id: str) -> MessageResponse:
    if id not in books:
        raise HTTPException(status_code=400, detail="Invalid book ID")
    del books[id]
    return MessageResponse(message=f"Book {id} deleted successfully")
