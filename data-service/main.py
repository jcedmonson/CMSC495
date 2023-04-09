from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import uvicorn

import backend
from backend import pydantic_models as pm
from backend import crud

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

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def root() -> dict:
    return {"message": "Project set up properly"}


@app.post("/login")
async def login_user(user: pm.UserBase, db: Session = Depends(get_db)) -> dict:
    # res = crud.auth_user(db, user)
    print(user)
    # print(f"result is: {res}")
    return {"Worky": "Yeah, it worky"}




# @app.post("/users/")
# def create_user(user: pm.UserProfile,
#                 db: Session = Depends(get_db)) -> pm.UserCreate:
#
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[backend.schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = backend.crud.get_users(db, skip=skip, limit=limit)
#     return users
#
# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                log_level="info")
