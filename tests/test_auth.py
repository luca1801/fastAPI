from http import HTTPStatus

import pytest
from freezegun import freeze_time


@pytest.mark.asyncio
async def teste_login_usuario_deve_retornar_token(client, create_user):
    user = await create_user()
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


@pytest.mark.asyncio
async def test_token_expirou_apos_tempo_definido(client, create_user):
    with freeze_time('2023-07-14 12:00:00'):
        user = await create_user()
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_token_nao_expirou_apos_tempo_definido(client, create_user):
    with freeze_time('2023-07-14 12:00:00'):
        user = await create_user()
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:29:59'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'id': user.id,
            'username': 'wrongwrong',
            'email': 'wrong@wrong.com',
        }


def test_token_usuario_inexistente_deve_retornar_erro(client):
    response = client.post(
        '/auth/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_senha_incorreta_deve_retornar_erro(client):
    response = client.post(
        '/auth/token',
        data={
            'username': 'no_user@no_domain.com',
            'password': 'wrongpassword',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token_deve_revalidar_token(client, generate_token):
    old_token = generate_token[1]
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {old_token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    # assert data['access_token'] != old_token
    assert data['token_type'] == 'bearer'


@pytest.mark.asyncio
async def test_token_continua_valido_apos_refresh(client, create_user):
    with freeze_time('2023-07-14 12:00:00'):
        user = await create_user()
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:29:58'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.OK
        # new_token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


@pytest.mark.asyncio
async def test_token_expirado_deve_retornar_erro_ao_tentar_refresh(
    client, create_user
):
    with freeze_time('2023-07-14 12:00:00'):
        user = await create_user()
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


# def test_token_deve_expirar_apos_tempo_definido(
# client, create_user, Settings
# ):
#     with freeze_time() as frozen:
#         user = frozen.call(create_user())
#         response = client.post(
#             '/auth/token',
#             data={
#                 'username': user.email,
#                 'password': user.clean_password,
#             },
#         )  # Act
#         token = response.json()

#         assert response.status_code == HTTPStatus.OK  # Assert
#         assert 'access_token' in token  # Assert

#         frozen.tick(Settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

#         response = client.delete(
#             '/users/1',
#             headers={'Authorization': f'Bearer {token["access_token"]}'},
#         )

#         assert response.status_code == HTTPStatus.UNAUTHORIZED  # Assert
#         assert response.json() == {
#             'detail': 'Could not validate credentials'
#         }  # Assert
