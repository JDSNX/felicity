from fastapi import FastAPI
from database.core import engine, Base
from routers.accounts import router as accounts_router
from routers.auth import router as auth_router
from routers.patients import router as patients_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(accounts_router)
app.include_router(auth_router)
app.include_router(patients_router)

@app.get("/api")
async def root():
    return {"message": "hello"}


