from fastapi import FastAPI
from src.authentications.routers import auth_router
from src.db.session import engine, Base

version = "V1"

app = FastAPI(
    title="User Authentication",
    description="API for a user authentication in TODO Application.",
    version=version
)

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])

@app.get("/")
def read_root():
    return {"message": "Hello Avenir"}