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

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class JWTUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class JWTDBUser(JWTUser):
    hashed_password: str

class UserPostBody(BaseModel):
    body: str