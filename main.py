import logging
from fastapi import FastAPI, Request
from fastapi.security import OAuth2

from src.routes.book_route import router

app = FastAPI(title="Book Inventory Management")
app.include_router(router)

logging.basicConfig(level=logging.DEBUG)

@app.get("/")
def root():
    return "Connected to the Book Inventroy Management"

