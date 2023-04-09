from sqlalchemy.orm import Session

from . import models
from . import pydantic_models as pm

# def create_user(db: Session, user: pm.UserProfile):
#     new_user = models.UserProfile(user)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

def auth_user(db: Session, user: pm.UserLogin):
    res = db.query(models.UserProfile).filter(models.UserProfile.user_name == user).first()
    print(type(res))
    print(res)