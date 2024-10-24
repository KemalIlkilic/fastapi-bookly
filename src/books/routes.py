from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List, Annotated
from src.db.main import get_session
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()

MyAsyncSession = Annotated[AsyncSession, Depends(get_session)]
UserDetails = Annotated[dict,Depends(access_token_bearer)]

@book_router.get("/", response_model=List[Book])
async def get_all_books(session : MyAsyncSession, user_details : UserDetails):
    #user_details : {'user': {'email': 'kemal@dmca.io', 'user_uid': '2e53a352-c25f-61cd281461'},
    #            'exp': 1729468596, 'jti': '<function uuid4 at 0x100f5cc20>', 'refresh': False}
    print(user_details)
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED , response_model=Book)
async def create_a_book(book_data : BookCreateModel, session : MyAsyncSession, user_details: UserDetails): 
    new_book = await book_service.create_book(book_data,session)
    return new_book


@book_router.get("/{book_uid}" , response_model=Book)
async def get_book(book_uid : str, session : MyAsyncSession, user_details: UserDetails):
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(book_uid : str, book_update_data : BookUpdateModel, session : MyAsyncSession, user_details: UserDetails) :
    updated_book = await book_service.update_book(book_uid, book_update_data, session )
    if updated_book:
        return updated_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_uid}")
async def delete_book(book_uid : str, session : MyAsyncSession, user_details: UserDetails):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {"message" : "book deleted successfully"}
    