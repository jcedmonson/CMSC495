from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn

import backend

# Create all the tables if they need to be created
backend.models.Base.metadata.create_all(bind=backend.engine)

app = FastAPI()

# Dependency
def get_db():
    db = backend.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root() -> dict:
    return {"message": "Project set up properly"}

@app.get("/users/", response_model=list[backend.schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = backend.crud.get_users(db, skip=skip, limit=limit)
    return users


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                log_level="info")
