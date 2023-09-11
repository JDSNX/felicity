from fastapi import FastAPI
from database.core import Base
from database.session import engine
from users.routers import router as users_router
from patients.routers import router as patient_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(patient_router)


@app.get("/")
async def root():
    return {"message": "hello"}
