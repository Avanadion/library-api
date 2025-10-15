from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Library API")

class Book(BaseModel):
    id: int | None = None
    title: str
    author: str
    year: int

books = [
    {"id": 1, "title": "Гарри Поттер и философский камень", "author": "Джоан Роулинг", "year": 1997},
    {"id": 2, "title": "Оно", "author": "Стивен Кинг", "year": 1986},
]

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/books")
def get_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.post("/books")
def add_book(book: Book):
    new_id = max([b["id"] for b in books]) + 1 if books else 1
    book.id = new_id
    books.append(book.dict())
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, updated: Book):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            updated.id = book_id
            books[i] = updated.dict()
            return updated
    raise HTTPException(status_code=404, detail="Книга не найдена")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Книга удалена"}
    raise HTTPException(status_code=404, detail="Книга не найдена")
