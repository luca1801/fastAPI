# teste da rota de usuários do app.py usando pytest e TestClient do FastAPI
from http import HTTPStatus

from fast_api.schemas.schemas import UserSchemaPublic


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


def teste_deve_listar_usuarios(client, create_user, generate_token):
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


def teste_atualizar_usuario_deve_retornar_usuario_atualizado(
    client, create_user, generate_token
):
    # create_user('lucas', 'lucas@gmail.com', 'secret')
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': 'Lucas Silva',
            'email': 'lucas.silva@gmail.com',
            'password': 'newsecret',
        },
    )  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'username': 'Lucas Silva',
        'email': 'lucas.silva@gmail.com',
        'id': 1,
    }  # Assert

    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': 'Lucas Silva',
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


def teste_update_erro_integridade_usuario_ja_existe(client, generate_token):
    # create_user('lucas', 'lucas@gmail.com', 'secret')
    # adiciona outro usuario para gerar conflito
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'testpassword',
        },
    )
    # tenta atualizar o usuario criado na fixture generate_token
    response = client.put(
        f'/users/{generate_token[0].id}',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': 'fausto',
            'email': 'testuser2@example.com',
            'password': 'testpassword',
        },
    )  # Act

    assert response.status_code == HTTPStatus.CONFLICT  # Assert
    assert response.json() == {
        'detail': 'Username or email already exists'
    }  # Assert


def teste_criar_usuario_deve_retornar_erro_para_usuario_existente(
    client, generate_token
):
    response = client.post(
        '/users',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
        json={
            'username': 'testuser',
            'email': 'testuser2@example.com',
            'password': 'testpassword',
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
            'username': 'testuser2',
            'email': 'testuser@example.com',
            'password': 'testpassword',
        },
    )  # Act

    assert response.status_code == HTTPStatus.CONFLICT  # Assert
    assert response.json() == {'detail': 'Email already exists'}  # Assert
