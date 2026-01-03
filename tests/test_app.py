from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api.app import app


def teste_root_deve_retornar_hello_world():
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Hello World!'}  # Assert
