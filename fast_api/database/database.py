from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_api.config.settings import settings

engine = create_engine(settings.DATABASE_URL)


def get_session():
    """Create and return a new SQLAlchemy session."""
    with Session(engine) as session:
        # yield faz com que a função seja um
        # gerador de contexto
        yield session
