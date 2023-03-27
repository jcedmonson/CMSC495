from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Lazy initialization; does not actually make a connection to the db
# The connection is actually made with a connection object `engine.connect()`
# It is often preferred to use `engine.begin()` as a succinct way to commit
# at the end
engine = create_engine(
    f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('HOST')}/{getenv('POSTGRES_DB')}",
    echo=True)

# Sessions are the usual way to interact with the database. They will fetch a
# connection when it is needed making it efficient. THe usual way
# to interact with it is with:

# with Session(engine) as session:
#     session.begin()
#     try:
#         session.add(some_object)
#         session.add(some_other_object)
#     except:
#         session.rollback()
#         raise
#     else:
#         session.commit()

# Just like with connection you can also use the `begin` to wrap
# these calls into one
# with Session(engine) as session, session.begin():
#     session.add(some_object)
#     session.add(some_other_object)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# With a session maker, we can make a session factory so that we don't have
# to keep specifying the engine and use it as a way to make the same config
# session. This makes the code a lot smaller with"

# with Session.begin() as session:
#     session.add(some_object)
#     session.add(some_other_object)

# it is typical for Engine and SessionMaker result be module level objects
# so that can be used globally by any thread (thread safe)

# Represent the metadata from ORM mapped class
Base = declarative_base()
