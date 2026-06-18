from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from storm_db.config import settings

_engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    echo=settings.debug,
)


def init_db() -> None:
    SQLModel.metadata.create_all(_engine)


def get_session() -> Generator[Session, None, None]:
    with Session(_engine) as session:
        yield session
