from http import HTTPStatus


def teste_login_usuario_deve_retornar_token(client, create_user):
    user = create_user('lucas', 'lucas@gmail.com', 'secret')
    response = client.post(
        '/auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )  # Act
    token = response.json()

    assert response.status_code == HTTPStatus.OK  # Assert
    assert 'access_token' in token  # Assert
    assert token['token_type'] == 'bearer'  # Assert
