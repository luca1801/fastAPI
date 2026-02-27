# Importa asdict para converter objetos dataclass em dicionários
from dataclasses import asdict

import pytest

# Importa select do SQLAlchemy para criar queries de seleção no banco de dados
from sqlalchemy import select

# Importa o módulo de modelos de usuários para usar na criação de usuários
from fast_api.models import users


# Função de teste que valida a criação de um novo usuário no banco de dados
@pytest.mark.asyncio
async def teste_criar_usuario_no_banco_retorna_usuario_criado(
    # Fixture que fornece uma sessão do banco de dados em memória
    session_init,
    # Fixture que fornece a função para mockar a data de criação
    mock_db_time,
):
    # Ativa o mock de data/hora para a classe UserBase com
    # data padrão (2026-01-01)
    with mock_db_time(model=users.UserBase) as time:
        # Cria um novo usuário com os dados de teste
        new_user = users.UserBase(
            username='testuser',
            email='testuser@example.com',
            empresa_id=1,  # Empresa associada (deve existir no BD de teste)
            password='testpassword',
        )

        # Adiciona o novo usuário à sessão do banco de dados
        session_init.add(new_user)
        # Confirma a transação e persiste o usuário no banco de dados
        await session_init.commit()

        # Busca o usuário criado no banco de dados usando uma
        # query SELECT
        user = await session_init.scalar(
            # Seleciona o usuário com username igual a 'testuser'
            select(users.UserBase).where(users.UserBase.username == 'testuser')
        )

        # Valida que o usuário foi criado com os dados corretos
        assert asdict(user) == {
            'id': 1,  # ID esperado (primeira inserção no banco de testes)
            'username': 'testuser',  # Nome de usuário fornecido
            'email': 'testuser@example.com',  # Email fornecido
            'password': 'testpassword',  # Senha fornecida
            'created_at': time,  # Data de criação mockada (2026-01-01)
            'empresa_id': 1,  # Empresa associada (deve existir no BD de teste)
        }
