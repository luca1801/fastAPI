from http import HTTPStatus

from jwt import decode

from fast_api.security.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
)


def teste_login_deve_retornar_token_de_acesso():
    data = {'test': 'test'}
    access_token = create_access_token(data=data)
    decoded_token = decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_token['test'] == data['test']
    assert 'exp' in decoded_token


def test_jwt_decode_deve_levantar_excecao_para_token_invalido(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer invalidtoken'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not_found__exercicio(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
