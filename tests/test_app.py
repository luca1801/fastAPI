from http import HTTPStatus

from fast_api.schemas.schemas import UserSchemaPublic

# def teste_root_deve_retornar_hello_world(client):
#     # client = TestClient(app)  # Arrange

#     response = client.get('/')  # Act

#     assert response.status_code == HTTPStatus.OK  # Assert
#     assert response.json() == {'message': 'Hello World!'}  # Assert


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


def teste_listar_usuarios_deve_retornar_lista_de_usuarios(client):

    response = client.get('/users/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'users': []}  # Assert


def teste_listar_usuarios_com_dados_retorna_lista_de_usuarios(
    client, create_user
):

    user_schema = UserSchemaPublic.model_validate(
        create_user('lucas', 'lucas@gmail.com', 'secret')
    ).model_dump()
    response = client.get('/users/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'users': [user_schema]}  # Assert


def teste_atualizar_usuario_deve_retornar_usuario_atualizado(
    client, create_user
):
    create_user('lucas', 'lucas@gmail.com', 'secret')
    response = client.put(
        '/users/1',
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
        json={
            'username': 'Lucas Silva',
            'email': 'lucas.silva@gmail.com',
            'password': 'newsecret',
        },
    )  # Act
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert


def teste_deletar_usuario_deve_retornar_usuario_deletado(client, create_user):
    create_user('lucas', 'lucas@gmail.com', 'secret')
    response = client.delete('/users/1')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'message': 'User deleted successfully'
    }  # Assert

    response = client.delete('/users/2')  # Act
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert


def teste_update_erro_integridade_usuario_ja_existe(client, create_user):
    create_user('lucas', 'lucas@gmail.com', 'secret')
    client.post(
        '/users',
        json={
            'username': 'maria',
            'email': 'maria@gmail.com',
            'password': 'secret',
        },
    )
    response = client.put(
        '/users/1',
        json={
            'username': 'maria',
            'email': 'maria@gmail.com',
            'password': 'newsecret',
        },
    )  # Act

    assert response.status_code == HTTPStatus.CONFLICT  # Assert
    assert response.json() == {
        'detail': 'Username or email already exists'
    }  # Assert
