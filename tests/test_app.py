from http import HTTPStatus


def teste_root_deve_retornar_hello_world(client):
    # client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Hello World!'}  # Assert


def teste_criar_usuario_deve_retornar_usuario_criado(client):
    # client = TestClient(app)  # Arrange

    usuario_post = {
        'nome': 'Lucas',
        'email': 'lucas@gmail.com',
        'senha': 'secret',
    }
    usuario_response = {
        'nome': 'Lucas',
        'email': 'lucas@gmail.com',
        'id': 1,
    }

    response = client.post('/users', json=usuario_post)  # Act
    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == usuario_response  # Assert


def teste_listar_usuarios_deve_retornar_lista_de_usuarios(client):
    response = client.get('/users/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'users': [
            {
                'nome': 'Lucas',
                'email': 'lucas@gmail.com',
                'id': 1,
            }
        ]
    }  # Assert


def teste_atualizar_usuario_deve_retornar_usuario_atualizado(client):
    response = client.put(
        '/users/1',
        json={
            'nome': 'Lucas Silva',
            'email': 'lucas.silva@gmail.com',
            'senha': 'newsecret',
        },
    )  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'nome': 'Lucas Silva',
        'email': 'lucas.silva@gmail.com',
        'id': 1,
    }  # Assert

    response = client.put(
        '/users/2',
        json={
            'nome': 'Lucas Silva',
            'email': 'lucas.silva@gmail.com',
            'senha': 'newsecret',
        },
    )  # Act
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert


def teste_deletar_usuario_deve_retornar_usuario_deletado(client):
    response = client.delete('/users/1')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {
        'nome': 'Lucas Silva',
        'email': 'lucas.silva@gmail.com',
        'id': 1,
    }  # Assert

    response = client.delete('/users/2')  # Act
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert
