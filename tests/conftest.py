# Importa contextmanager para criar um gerenciador de contexto personalizado
from contextlib import contextmanager

# Importa datetime para trabalhar com datas e horas nos testes
from datetime import datetime

# Importa o módulo pytest para criar fixtures de teste
import pytest

# Importa o cliente de teste do FastAPI para fazer requisições HTTP simuladas
from fastapi.testclient import TestClient

# Importa a função para criar engines de conexão com o banco de dados
from sqlalchemy import create_engine, event

# Importa a sessão do SQLAlchemy para gerenciar transações do banco de dados
from sqlalchemy.orm import Session

# Importa a aplicação FastAPI principal
from fast_api.app import app

# Importa o registry de tabelas para criar as tabelas no banco de dados
from fast_api.models.users import table_registry


# Define uma fixture do pytest que fornece um cliente de teste
@pytest.fixture
def client():
    # Retorna uma instância do TestClient conectada à aplicação FastAPI
    return TestClient(app)


@pytest.fixture
def session_init():  # Função que inicializa uma sessão de BD para testes
    # Cria um engine SQLAlchemy com banco de dados em memória (não persistente)
    engine = create_engine('sqlite:///:memory:')
    # Cria todas as tabelas definidas no table_registry no banco de dados
    table_registry.metadata.create_all(engine)

    # Abre uma sessão com o banco de dados
    with Session(engine) as session:
        # Retorna a sessão para uso nos testes (comportamento de generator)
        yield session

    # Após o uso da sessão, descarta todas as tabelas do banco de dados
    table_registry.metadata.drop_all(engine)

    # Fecha todas as conexões abertas do engine para liberar recursos
    engine.dispose()


# Define um gerenciador de contexto que permite mockar a data/hora de criação no banco de dados
@contextmanager
def _mock_db_time(*, model, time=datetime(2026, 1, 1)):
    # Define uma função que será executada antes de cada inserção no banco de dados
    def fake_time_hook(mapper, connection, target):
        # Verifica se o modelo possui o atributo 'created_at' (data de criação)
        if hasattr(target, 'created_at'):
            target.created_at = time

    # Registra o hook (gancho) para executar antes de cada inserção do modelo
    event.listen(model, 'before_insert', fake_time_hook)

    # Retorna o tempo mockado para uso dentro do bloco 'with' (comportamento de gerenciador)
    yield time

    # Remove o hook registrado anteriormente para não afetar outros testes
    event.remove(model, 'before_insert', fake_time_hook)


# Define uma fixture pytest que retorna a função de mock de tempo
@pytest.fixture
def mock_db_time():
    # Retorna a função _mock_db_time para ser usada nos testes
    return _mock_db_time
