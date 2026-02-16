from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from fast_api.config.settings import settings

engine = create_async_engine(settings.DATABASE_URL)


async def get_session():
    """Create and return a new SQLAlchemy session assincrona ."""
    # expire_on_commit é necessário para evitar que os objetos sejam expirados
    # após o commit, permitindo que sejam usados mesmo depois do commit.
    async with AsyncSession(engine, expire_on_commit=False) as session:
        # yield faz com que a função seja um
        # gerador de contexto
        yield session
