from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    user_name: str


class UserLogin(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserCreate(UserLogin):
    first_name: str
    last_name: str
    email: EmailStr


class User(BaseModel):
    user_id: int
    user_name: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class UserAcc(User):
    account_status: bool
    account_private: bool
    email: EmailStr


class UserAuthed(UserAcc):
    token: str | None

class UserSensitive(UserAuthed):
    password_hash: bytes
