from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserLogin(UserBase):
    password: str

class UserAuthed(BaseModel):
    user_id: int
    user_name: str
    auth_token: str


# class LoginUser(BaseUser):
#     password: str
#
# class UserProfile(BaseModel):
#     id: int
#     user_name: str
#
# class UserProfileAll(UserProfile):
#     account_status: bool
#     account_private: bool
#
# class PostComment(UserProfile):
#     id: int
#     post_id: int
#     user_id: int
#
# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None
#
#
# class ItemCreate(ItemBase):
#     pass
#
#
# class Item(ItemBase):
#     id: int
#     owner_id: int
#
#     class Config:
#         orm_mode = True
#
#
#
#
# class UserCreate(UserBase):
#     password: str
#
#
# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []
#
#     class Config:
#         orm_mode = True