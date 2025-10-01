from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from config import settings
from .models import Base

_engine = None
_SessionLocal = None

def init_db():
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(settings.database_url, connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {})
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
    return _engine

@contextmanager
def get_session():
    if _engine is None:
        init_db()
    db = _SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def create_all():
    if _engine is None:
        init_db()
    Base.metadata.create_all(bind=_engine)
