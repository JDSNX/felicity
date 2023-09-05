from fastapi import FastAPI
from database.core import Base
from database.session import engine

from auth.router import router as auth_router
from users.router import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "hello"}
