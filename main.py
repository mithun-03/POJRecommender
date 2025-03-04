from fastapi import FastAPI
from database import engine, Base
from routes.user_routes import router as user_router
from routes.home_routes import router as home_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(user_router, prefix="/auth", tags=["Auth"])
app.include_router(home_router, tags=["Home"])

@app.get("/")
def root():
    return {"message": "FastAPI Authentication System"}
