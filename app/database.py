from collections.abc import Generator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import get_settings

settings = get_settings()
metadata = MetaData(schema="agency")


class Base(DeclarativeBase):
    """Declarative base with default schema."""

    metadata = metadata


engine = create_engine(settings.database_url, echo=False, future=True)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=Session,
)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session for FastAPI dependency injection."""
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
