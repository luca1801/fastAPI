# teste da rota de usuários do app.py usando pytest e TestClient do FastAPI
from http import HTTPStatus

import pytest

from fast_api.schemas.users import UserSchemaPublic


def teste_criar_usuario_deve_retornar_usuario_criado(client):
    # client = TestClient(app)  # Arrange

    usuario_post = {
        'username': 'Lucas2w',
        'email': 'lucas2w@gmail.com',
        'password': 'secret',
    }
    usuario_response = {
        'username': 'Lucas2w',
        'email': 'lucas2w@gmail.com',
        'id': 1,
    }

    response = client.post('/users', json=usuario_post)  # Act
    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == usuario_response  # Assert


def teste_deve_listar_usuarios(client, generate_token):
    # create_user.user = create_user('lucas', 'lucas@gmail.com', 'secret')
    # generate_token.user.username = 'lucas'
    # generate_token.user.password = 'secret'
    user_schema = UserSchemaPublic.model_validate(
        generate_token[0]
    ).model_dump()
    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
    )  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'users': [user_schema]}  # Assert


@pytest.mark.asyncio
async def teste_atualizar_usuario_deve_retornar_usuario_atualizado(
    client, generate_token, create_other_user
):
    # create_user('lucas', 'lucas@gmail.com', 'secret')
    # user = await create_other_user()
    response = client.put(
        f'/users/{generate_token[0].id}',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': generate_token[0].username,
            'email': 'teste@example.com',
            'password': generate_token[0].clean_password,
        },
    )  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'username': generate_token[0].username,
        'email': 'teste@example.com',
        'id': generate_token[0].id,
    }  # Assert

    user = await create_other_user()
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': 'lucas',
            'email': 'lucas.silva@gmail.com',
            'password': 'newsecret',
        },
    )  # Act
    assert response.status_code == HTTPStatus.UNAUTHORIZED  # Assert


def teste_deletar_usuario_deve_retornar_usuario_deletado(
    client, generate_token
):
    # create_user('lucas', 'lucas@gmail.com', 'secret')
    # deletar o usuario criado na fixture generate_token
    response = client.delete(
        f'/users/{generate_token[0].id}',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
    )  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'message': 'User deleted successfully'
    }  # Assert

    response = client.delete('/users/2')  # Act
    assert response.status_code == HTTPStatus.UNAUTHORIZED  # Assert


@pytest.mark.asyncio
async def teste_update_erro_integridade_usuario_ja_existe(
    client, generate_token, create_other_user
):
    # create_user('lucas', 'lucas@gmail.com', 'secret')
    # adiciona outro usuario para gerar conflito
    user = await create_other_user()
    client.post(
        '/users',
        json={
            'username': user.username,
            'email': user.email,
            'password': 'anything',
        },
    )
    # tenta atualizar o usuario criado na fixture generate_token
    response = client.put(
        f'/users/{generate_token[0].id}',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': user.username,
            'email': user.email,
            'password': 'anything',
        },
    )  # Act

    assert response.status_code == HTTPStatus.CONFLICT  # Assert
    assert response.json() == {
        'detail': 'Username or email already exists'
    }  # Assert


def teste_criar_usuario_deve_retornar_erro_para_usuario_existente(
    client, generate_token
):
    # user = create_user()
    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': generate_token[0].username,
            'email': generate_token[0].email,
            'password': generate_token[0].clean_password,
        },
    )  # Act

    assert response.status_code == HTTPStatus.CONFLICT  # Assert
    assert response.json() == {'detail': 'Username already exists'}  # Assert


def teste_criar_usuario_deve_retornar_erro_para_email_existente(
    client, generate_token
):
    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': 'newuser',
            'email': generate_token[0].email,
            'password': generate_token[0].clean_password,
        },
    )  # Act

    assert response.status_code == HTTPStatus.CONFLICT  # Assert
    assert response.json() == {'detail': 'Email already exists'}  # Assert


@pytest.mark.asyncio
async def teste_atualizar_cadastro_com_usuario_diferente_deve_retornar_erro(
    client, generate_token, create_other_user
):
    user = await create_other_user()
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )  # Act

    assert response.status_code == HTTPStatus.FORBIDDEN  # Assert
    assert response.json() == {
        'detail': 'You do not have permission to update this user'
    }


@pytest.mark.asyncio
async def teste_deletar_cadastro_com_usuario_diferente_deve_retornar_erro(
    client, generate_token, create_other_user
):
    user = await create_other_user()
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
    )  # Act

    assert response.status_code == HTTPStatus.FORBIDDEN  # Assert
    assert response.json() == {
        'detail': 'You do not have permission to delete this user'
    }
