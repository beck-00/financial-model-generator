from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

