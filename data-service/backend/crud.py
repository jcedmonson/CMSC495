from sqlalchemy.orm import Session

from . import models
from . import pydantic_models as py_models

def create_user(db: Session, user: py_models.UserProfile):
    new_user = models.UserProfile(user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user