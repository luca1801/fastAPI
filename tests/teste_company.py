# teste rota de empresas do app.py usando pytest e TestClient do FastAPI

from http import HTTPStatus


def teste_criar_empresa_deve_retornar_empresa_criada(client, generate_token):
    company_post = {
        'name': 'Empresa Teste',
        'service': 'Teste de serviço',
        'location': 'Teste de localização',
        'ramal': '1234',
    }
    company_response = {
        'id': 1,
        'name': 'Empresa Teste',
        'service': 'Teste de serviço',
        'location': 'Teste de localização',
        'ramal': '1234',
        'status': 'active',
    }

    response = client.post(
        '/company/',
        json=company_post,
        headers={'Authorization': f'Bearer {generate_token[1]}'},
    )  # Act

    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == company_response  # Assert
