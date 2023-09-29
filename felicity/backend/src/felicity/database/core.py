from sqlalchemy.ext.declarative import declarative_base
from .session import session_local

Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
