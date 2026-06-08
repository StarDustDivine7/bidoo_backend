from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Database engine application start par ek baar banega.
engine = create_engine(settings.DATABASE_URL, echo=False)

# Har request ke liye alag DB session create hoga.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Saare SQLAlchemy models is base ko inherit karenge.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency.
    Request ke duration tak DB session open rakhta hai.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
