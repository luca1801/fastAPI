# Importa contextmanager para criar um gerenciador de contexto personalizado
from contextlib import contextmanager

# Importa datetime para trabalhar com datas e horas nos testes
from datetime import datetime

# Importa o módulo pytest para criar fixtures de teste
import pytest
import pytest_asyncio

# Importa o cliente de teste do FastAPI para fazer requisições HTTP simuladas
from fastapi.testclient import TestClient

# Importa a função para criar engines de conexão com o banco de dados
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# Importa a sessão do SQLAlchemy para gerenciar transações do banco de dados
from sqlalchemy.pool import StaticPool

# Importa a aplicação FastAPI principal
from fast_api.app import app
from fast_api.config.settings import settings
from fast_api.database.database import get_session

# Importa o registry de tabelas para criar as tabelas no banco de dados
from fast_api.models.users import UserBase, table_registry
from fast_api.security.security import get_password_hash


# Função que inicializa uma sessão de BD para testes
@pytest_asyncio.fixture
async def session_init():
    # Cria um engine SQLAlchemy com banco de dados
    # em memória (não persistente)
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    # Cria todas as tabelas definidas no table_registry no
    # banco de dados
    # table_registry.metadata.create_all(engine)

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)

    # Abre uma sessão com o banco de dados
    # with Session(engine) as session:
    #     # Retorna a sessão para uso nos testes (comportamento de generator)
    #     yield session

    # # Após o uso da sessão, descarta todas as tabelas do banco de dados
    # table_registry.metadata.drop_all(engine)

    # # Fecha todas as conexões abertas do engine para liberar recursos
    # engine.dispose()
    # try:
    #     with Session(engine) as session:
    #         yield session
    # finally:
    #     table_registry.metadata.drop_all(engine)
    #     engine.dispose()


# Define uma fixture do pytest que fornece um cliente de teste
@pytest.fixture
def client(session_init):
    def get_session_override():
        return session_init

    app.dependency_overrides[get_session] = get_session_override
    try:
        # Cria um cliente de teste usando o TestClient do FastAPI
        with TestClient(app) as client:
            # app.dependency_overrides[get_session] = get_session_override
            yield client
    finally:
        # Limpa os overrides de dependência após o teste
        app.dependency_overrides.clear()


# Define um gerenciador de contexto que permite mockar a
# data/hora de criação no banco de dados
@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 1, 1)):
    # Define uma função que será executada antes de cada inserção
    # no banco de dados
    def fake_time_hook(mapper, connection, target):
        # Verifica se o modelo possui o atributo
        # 'created_at' (data de criação)
        if hasattr(target, 'created_at'):
            target.created_at = time

    # Registra o hook (gancho) para executar antes de cada
    # inserção do modelo
    event.listen(model, 'before_insert', fake_time_hook)

    # Retorna o tempo mockado para uso dentro do
    # bloco 'with' (comportamento de gerenciador)
    yield time

    # Remove o hook registrado anteriormente para não afetar
    # outros testes
    event.remove(model, 'before_insert', fake_time_hook)


# Define uma fixture pytest que retorna a função de
# mock de tempo
@pytest.fixture
def mock_db_time():
    # Retorna a função _mock_db_time para ser usada nos testes
    return _mock_db_time


# Define uma fixture pytest que cria um usuário de teste
@pytest_asyncio.fixture
async def create_user(session_init: AsyncSession):
    async def _create_user(username: str, email: str, password: str):

        new_user = UserBase(
            username=username,
            email=email,
            password=get_password_hash(password),
        )

        session_init.add(new_user)
        await session_init.commit()
        await session_init.refresh(new_user)
        new_user.clean_password = password
        return new_user

    return _create_user


@pytest_asyncio.fixture
async def generate_token(client, create_user):
    user = await create_user(
        'testuser', 'testuser@example.com', 'testpassword'
    )
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    return user, response.json()['access_token']


@pytest.fixture
def Settings():
    return settings
