from fastapi import FastAPI
from src.authentications.routers import auth_router
from src.users.routers import users_router
from src.db.session import engine, Base

app = FastAPI(
    title="User Authentication",
    description="API for a user authentication in TODO Application.",
)

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix=f"/api/auth", tags=['auth'])
app.include_router(users_router, prefix=f"/api/users", tags=['users'])  

@app.get("/")
def read_root():
    return {"message": "Hello Avenir"}