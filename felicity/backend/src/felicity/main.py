from fastapi import FastAPI

from database.core import Base
from database.session import engine

from users.routers import router as users_router
from patients.routers import router as patient_router
from rooms.routers import router as room_router


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(users_router)
app.include_router(patient_router)
app.include_router(room_router)


@app.get("/")
async def root():
    return {"message": "hello"}
