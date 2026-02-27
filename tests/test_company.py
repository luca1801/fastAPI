# teste rota de empresas do app.py usando pytest e TestClient do FastAPI

from http import HTTPStatus

import pytest

from fast_api.schemas.company import CompanySchema


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


@pytest.mark.asyncio
async def teste_deve_listar_empresas(client, generate_token, create_company):
    company_schema = CompanySchema.model_validate(
        await create_company()
    ).model_dump()
    # Converta o status para string, igual ao retorno da API
    company_schema['status'] = company_schema['status'].value
    response = client.get(
        '/company/',
        headers={'Authorization': f'Bearer {generate_token[1]}'},
    )  # Act
    print(f'Listed companies response: {list(response.json())}')

    assert response.status_code == HTTPStatus.OK  # Assert
    # assert isinstance(response.json(), list)
    assert response.json() == [company_schema]  # Assert
