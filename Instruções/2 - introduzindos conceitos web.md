# fast_api API Project

## Desenvolvimento Web

### O modelo cliente-servidor

O **modelo cliente-servidor** é a arquitetura fundamental que sustenta toda a internet moderna. É um padrão de design que separa as responsabilidades entre dois componentes principais: o cliente (que solicita) e o servidor (que fornece).

#### Conceito Fundamental

```
┌──────────┐                HTTP                ┌──────────┐
│ CLIENTE  │────────────────────────────────────▶│ SERVIDOR │
│          │◀────────────────────────────────────│          │
└──────────┘           Resposta HTTP            └──────────┘
```

A comunicação segue um padrão **requisição-resposta**:
1. O cliente **inicia** a comunicação enviando uma requisição
2. O servidor **recebe** e **processa** a requisição
3. O servidor **envia** uma resposta de volta
4. O cliente **recebe** e **processa** a resposta

#### Componentes do Modelo

##### **O Cliente**

O cliente é responsável por:
- **Iniciar requisições** para o servidor
- **Apresentar** dados para o usuário
- **Coletar** informações do usuário
- **Processar** respostas recebidas
- **Gerenciar** a experiência do usuário

Exemplos de clientes:
- 🌐 **Navegadores web**: Chrome, Firefox, Safari, Edge
- 📱 **Aplicações mobile**: Apps iOS/Android, React Native
- 🖥️ **Aplicações desktop**: Electron, PyQt
- 🐍 **Scripts**: Python, Node.js, cURL
- 📡 **Clientes API**: Postman, Insomnia, TestClient

##### **O Servidor**

O servidor é responsável por:
- **Aguardar** requisições de clientes
- **Validar** dados recebidos
- **Processar** lógica de negócio
- **Acessar** banco de dados
- **Retornar** respostas apropriadas
- **Gerenciar** segurança e permissões

Exemplos de servidores:
- 🚀 **FastAPI** (seu projeto!)
- 🟢 **Node.js/Express**
- 🔴 **Ruby on Rails**
- 🐘 **Django/Python**
- ☕ **Java/Spring Boot**

#### Fluxo de Comunicação Detalhado

```
┌─────────────────────────────────────────────────────────┐
│                    REQUISIÇÃO (Request)                 │
├─────────────────────────────────────────────────────────┤
│ Método HTTP: GET, POST, PUT, DELETE, PATCH, etc        │
│ URL: http://api.exemplo.com/users/123                   │
│ Headers: Content-Type, Authorization, etc               │
│ Body: Dados (JSON, Form Data, etc)                      │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   PROCESSAMENTO NO SERVIDOR              │
├─────────────────────────────────────────────────────────┤
│ 1. Validar entrada                                       │
│ 2. Autenticar/Autorizar                                 │
│ 3. Processar lógica                                      │
│ 4. Consultar banco de dados                             │
│ 5. Preparar resposta                                     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    RESPOSTA (Response)                   │
├─────────────────────────────────────────────────────────┤
│ Status Code: 200, 201, 404, 500, etc                    │
│ Headers: Content-Type, Set-Cookie, etc                  │
│ Body: Dados (JSON, HTML, etc)                           │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  PROCESSAMENTO NO CLIENTE                │
├─────────────────────────────────────────────────────────┤
│ 1. Verificar status code                                │
│ 2. Validar dados recebidos                              │
│ 3. Atualizar interface/estado                           │
│ 4. Exibir resultado ao usuário                          │
└─────────────────────────────────────────────────────────┘
```

#### Exemplo Prático: Seu Projeto FastAPI

Em seu projeto, você tem um teste que demonstra exatamente esse modelo:

**Arquivo: `tests/test_app.py`**
```python
from http import HTTPStatus
from fastapi.testclient import TestClient
from fast_api.app import app

def teste_root_deve_retornar_hello_world():
    # 1. CLIENTE (TestClient) se conecta ao SERVIDOR (app)
    client = TestClient(app)
    
    # 2. REQUISIÇÃO: Cliente faz GET para '/'
    response = client.get('/')
    
    # 3. RESPOSTA: Servidor retorna dados
    # 4. CLIENTE processa e verifica a resposta
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}
```

**O que acontece:**
1. `TestClient(app)` cria um cliente para testar
2. `client.get('/')` faz uma requisição HTTP GET
3. O FastAPI recebe, processa e retorna a resposta
4. O cliente verifica se o status é 200 (OK)
5. O cliente verifica se os dados estão corretos

#### Vantagens do Modelo Cliente-Servidor

| Vantagem | Benefício |
|----------|-----------|
| **Separação de responsabilidades** | Cada componente tem função clara |
| **Escalabilidade** | Múltiplos clientes com um servidor |
| **Manutenção** | Alterações no servidor não afetam todos os clientes |
| **Segurança** | Lógica sensível fica protegida no servidor |
| **Diversidade** | Diferentes tipos de clientes podem usar o mesmo servidor |
| **Reutilização** | Mesma API serve web, mobile, etc |

#### Tipos de Requisições HTTP (Métodos)

O cliente usa diferentes métodos HTTP para indicar a ação desejada:

- **GET** 📖 - Recuperar dados
  ```
  GET /api/usuarios/1 → Obter dados do usuário 1
  ```

- **POST** ➕ - Criar novo recurso
  ```
  POST /api/usuarios → Criar novo usuário
  ```

- **PUT** ✏️ - Atualizar recurso completo
  ```
  PUT /api/usuarios/1 → Atualizar usuário 1 completamente
  ```

- **DELETE** 🗑️ - Remover recurso
  ```
  DELETE /api/usuarios/1 → Remover usuário 1
  ```

- **PATCH** 🔧 - Atualizar parcialmente
  ```
  PATCH /api/usuarios/1 → Atualizar parte do usuário 1
  ```

#### Códigos de Status HTTP (Respostas do Servidor)

O servidor comunica o resultado através de códigos numéricos:

- **2xx** ✅ Sucesso
  - `200 OK` - Requisição bem-sucedida
  - `201 Created` - Recurso criado com sucesso
  
- **3xx** 🔄 Redirecionamento
  - `301 Moved Permanently` - Recurso movido permanentemente
  
- **4xx** ❌ Erro do Cliente
  - `400 Bad Request` - Requisição inválida
  - `401 Unauthorized` - Sem autenticação
  - `404 Not Found` - Recurso não encontrado
  
- **5xx** 💥 Erro do Servidor
  - `500 Internal Server Error` - Erro no processamento
  - `503 Service Unavailable` - Servidor temporariamente indisponível

#### Conclusão

O modelo cliente-servidor é essencial para entender desenvolvimento web. Seu FastAPI é um **servidor** que aguarda **clientes** fazendo requisições HTTP e respondendo com dados JSON. A separação clara entre cliente e servidor permite que você tenha aplicações web robustas, escaláveis e fáceis de manter.

### FastAPI

O **FastAPI** é um framework moderno, rápido e fácil de usar para construir APIs web em Python. É construído sobre padrões web modernos e oferece funcionalidades poderosas com pouco código.

#### O que é FastAPI?

FastAPI é um framework web que permite criar servidores HTTP em Python de forma simples e elegante. Ele segue o padrão cliente-servidor e oferece:

- 🚀 **Performance excelente** - Uma das frameworks mais rápidas em Python
- 📚 **Documentação automática** - Gera docs interativas automaticamente
- ✅ **Validação de dados** - Valida automaticamente entrada e saída
- 🔐 **Segurança** - Suporte nativo para autenticação e autorização
- 🎯 **Type hints** - Aproveita tipagem Python para segurança de tipos
- 📦 **Moderno** - Usa Starlette, Pydantic e outras bibliotecas modernas

#### Arquitetura FastAPI

```
┌─────────────────────────────────────────────────────┐
│                    CLIENTE                          │
│        (Navegador, App Mobile, Script, etc)         │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP Request
                       ▼
┌─────────────────────────────────────────────────────┐
│                  FASTAPI SERVER                     │
├─────────────────────────────────────────────────────┤
│  Camada 1: Roteamento                               │
│  ├─ GET /                                           │
│  ├─ GET /api/users/{user_id}                        │
│  ├─ POST /api/users                                 │
│  └─ DELETE /api/users/{user_id}                     │
│                                                     │
│  Camada 2: Validação (Pydantic)                     │
│  ├─ Validar tipos de dados                          │
│  ├─ Validar obrigatoriedade                         │
│  └─ Converter tipos automaticamente                 │
│                                                     │
│  Camada 3: Lógica de Negócio                        │
│  ├─ Processar requisição                            │
│  ├─ Acessar banco de dados                          │
│  └─ Executar cálculos                               │
│                                                     │
│  Camada 4: Serialização                             │
│  ├─ Converter objetos para JSON                     │
│  └─ Preparar resposta                               │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP Response
                       ▼
┌─────────────────────────────────────────────────────┐
│                    CLIENTE                          │
│         (Recebe e processa a resposta)              │
└─────────────────────────────────────────────────────┘
```

#### Conceitos Principais

##### **Rotas (Routes)**

Uma rota é um endpoint - um caminho específico que o servidor responde.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/api/users")
def list_users():
    return {"users": []}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

**O `@app.get("/")` significa:**
- `@app` - usar a aplicação FastAPI
- `.get` - responder apenas a requisições GET
- `"/"` - no caminho raiz

##### **Métodos HTTP**

FastAPI suporta todos os métodos HTTP através de decoradores:

```python
@app.get("/items")          # Recuperar
@app.post("/items")         # Criar
@app.put("/items/{id}")     # Atualizar completo
@app.delete("/items/{id}")  # Deletar
@app.patch("/items/{id}")   # Atualizar parcial
```

##### **Parâmetros de Rota (Path Parameters)**

Partes variáveis da URL, cercadas por chaves `{}`:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    # user_id vem da URL
    # Exemplo: GET /users/123 → user_id = 123
    return {"user_id": user_id}
```

##### **Parâmetros de Query (Query Parameters)**

Dados passados após `?` na URL:

```python
@app.get("/search")
def search(q: str, limit: int = 10):
    # Exemplo: GET /search?q=python&limit=5
    # q = "python", limit = 5
    return {"query": q, "limit": limit}
```

##### **Request Body (Corpo da Requisição)**

Dados enviados no corpo da requisição (JSON):

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

@app.post("/users")
def create_user(user: User):
    # Recebe JSON como objeto User
    # Exemplo: POST /users
    # {
    #   "name": "João",
    #   "email": "joao@email.com",
    #   "age": 30
    # }
    return {"message": f"Usuário {user.name} criado!"}
```

##### **Response Models (Modelos de Resposta)**

Define a estrutura da resposta:

```python
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": "João Silva",
        "email": "joao@email.com"
    }
```

#### Seu Projeto Prático

Vamos analisar seu arquivo `fast_api/app.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World!"}
```

**O que acontece:**

1. **Importa FastAPI** - Carrega o framework
2. **Cria a aplicação** - `app = FastAPI()` cria uma instância
3. **Define uma rota** - `@app.get("/")` cria um endpoint
4. **Define a função** - `read_root()` executa quando a rota é acessada
5. **Retorna dados** - Automaticamente convertido para JSON

#### Validação Automática

FastAPI valida automaticamente usando type hints:

```python
@app.post("/users")
def create_user(name: str, age: int):
    # Se age não for número inteiro, FastAPI rejeita
    # Se name não for string, FastAPI rejeita
    return {"name": name, "age": age}
```

**Exemplo de erro automático:**
```
GET /users?name=João&age=abc

Resposta:
{
  "detail": [
    {
      "loc": ["query", "age"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

#### Documentação Automática

FastAPI gera documentação interativa automaticamente!

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    """Retorna uma mensagem de boas-vindas"""
    return {"message": "Hello World!"}
```

**Acessar documentação:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Status Codes

FastAPI permite controlar códigos de resposta:

```python
from fastapi import FastAPI
from http import HTTPStatus

app = FastAPI()

@app.post("/users", status_code=HTTPStatus.CREATED)
def create_user(name: str):
    return {"id": 1, "name": name}

@app.delete("/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    return
```

#### Executar a Aplicação

Ao construir um servidor, precisamos de uma biblioteca que consiga "servir" nossa aplicação. É aí que entra o `Uvicorn`, responsável por servir nossa aplicação com FastAPI.
Para iniciar seu servidor FastAPI:

```bash
# Usando uvicorn diretamente
uvicorn fast_api.app:app --reload

# ou pelo proprio fastapi
fastapi dev fast_api/app.py

```

Quando executamos esse comando. O FastAPI faz uma chamada ao uvicorn e iniciamos um servidor em loopback, acessível apenas internamente no nosso computador. Por isso, ao acessarmos `http://127.0.0.1:8000/` no navegador, estamos fazendo uma requisição ao servidor em `127.0.0.1:8000`. O servidor fica disponível em `http://localhost:8000`

**Usando o fastapi na rede local**

Falando em redes, o Uvicorn no seu PC também pode servir o FastAPI na sua rede local. Assim, você pode acessar a aplicação de outro computador na sua rede usando o endereço IP da sua máquina.

```bash
fastapi dev fast_api/app.py --host 0.0.0.0
```

#### Ciclo de Vida de uma Requisição no FastAPI

```
1. CLIENTE envia requisição HTTP
   ↓
2. FastAPI RECEBE a requisição
   ↓
3. FastAPI ROTA a requisição para o endpoint correto
   ↓
4. FastAPI VALIDA os dados usando type hints
   ↓
5. FastAPI EXECUTA a função da rota
   ↓
6. Função PROCESSA lógica de negócio
   ↓
7. Função RETORNA dados (dict, list, etc)
   ↓
8. FastAPI SERIALIZA para JSON
   ↓
9. FastAPI ENVIA resposta HTTP
   ↓
10. CLIENTE RECEBE e processa a resposta
```

#### Conclusão

FastAPI torna fácil criar APIs web robustas e rápidas em Python. Combina o poder de frameworks modernos com uma sintaxe simples e intuitiva. Sua documentação automática e validação incorporada economizam tempo e reduzem erros. É a escolha perfeita para desenvolvimento web profissional em Python!

### Pydantic: BaseModel

**Pydantic** é uma biblioteca Python que fornece validação de dados e configuração de settings usando type hints do Python. O **BaseModel** é a classe fundamental do Pydantic que você usa para definir a estrutura de seus dados.

#### O que é Pydantic?

Pydantic é uma ferramenta poderosa para:

- ✅ **Validação** - Garante que os dados têm o tipo e formato corretos
- 📋 **Documentação** - Tipos indicam claramente qual estrutura de dados esperar
- 🔄 **Serialização/Desserialização** - Converte JSON para objetos Python e vice-versa
- 🛡️ **Segurança** - Previne dados malformados de entrar em seu sistema
- ⚡ **Performance** - Validação rápida com C acelerado
- 🔍 **Transparência** - Mensagens de erro claras e detalhadas

#### O que é BaseModel?

**BaseModel** é a classe principal do Pydantic. Você a herda para criar seus próprios modelos de dados. É como um "blueprint" ou "schema" que define a estrutura esperada dos dados.

#### Criando seu Primeiro Model

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
```

**O que isso significa:**
- `class User(BaseModel)` - Define uma classe de modelo de dados
- `name: str` - Campo chamado `name` deve ser uma string
- `email: str` - Campo chamado `email` deve ser uma string
- `age: int` - Campo chamado `age` deve ser um inteiro

#### Usando o Model

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

# Criando uma instância com dados válidos
user = User(name="João", email="joao@email.com", age=30)
print(user.name)    # Output: João
print(user.age)     # Output: 30

# Convertendo para dicionário
user_dict = user.model_dump()
print(user_dict)    
# Output: {'name': 'João', 'email': 'joao@email.com', 'age': 30}

# Convertendo para JSON
user_json = user.model_dump_json()
print(user_json)
# Output: {"name":"João","email":"joao@email.com","age":30}
```

#### Validação Automática

Pydantic valida automaticamente os dados:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

# ✅ Válido - Todos os tipos corretos
user = User(name="João", email="joao@email.com", age=30)

# ❌ Inválido - age deveria ser int, não string
try:
    user = User(name="João", email="joao@email.com", age="trinta")
except Exception as e:
    print(f"Erro: {e}")
    # Erro: 1 validation error for User
    # age
    #   value is not a valid integer (type=type_error.integer)
```

#### Convertendo Tipos Automaticamente

Pydantic tenta converter tipos compatíveis:

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    quantity: int

# age será convertido de string para int automaticamente
product = Product(name="Notebook", price="1999.99", quantity="5")
print(type(product.price))      # <class 'float'>
print(type(product.quantity))   # <class 'int'>
print(product.price)            # 1999.99
print(product.quantity)         # 5
```

#### Campos Opcionais

Use `Optional` para fazer campos não obrigatórios:

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str                      # Obrigatório
    email: str                     # Obrigatório
    age: Optional[int] = None      # Opcional, padrão None
    phone: Optional[str] = None    # Opcional, padrão None

# ✅ Válido - Campos opcionais omitidos
user = User(name="João", email="joao@email.com")
print(user.age)     # None
print(user.phone)   # None

# ✅ Válido - Campos opcionais preenchidos
user = User(name="João", email="joao@email.com", age=30, phone="11999999999")
print(user.age)     # 30
```

#### Valores Padrão

Defina valores padrão para campos:

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    currency: str = "BRL"      # Padrão
    is_active: bool = True     # Padrão
    quantity: int = 0          # Padrão

# ✅ Usa valores padrão
product = Product(name="Notebook", price=1999.99)
print(product.currency)    # BRL
print(product.is_active)   # True
print(product.quantity)    # 0

# ✅ Sobrescreve valores padrão
product = Product(name="Mouse", price=50.00, currency="USD", is_active=False)
print(product.currency)    # USD
print(product.is_active)   # False
```

#### Validação Personalizada

Adicione lógica de validação customizada:

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    email: str
    age: int

    @field_validator('age')
    @classmethod
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Idade não pode ser negativa')
        if v > 150:
            raise ValueError('Idade não pode ser maior que 150')
        return v

    @field_validator('email')
    @classmethod
    def email_must_have_at(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido: deve conter @')
        return v

# ❌ Inválido - Idade negativa
try:
    user = User(name="João", email="joao@email.com", age=-5)
except Exception as e:
    print(f"Erro: {e}")

# ❌ Inválido - Email sem @
try:
    user = User(name="João", email="joao", age=30)
except Exception as e:
    print(f"Erro: {e}")

# ✅ Válido
user = User(name="João", email="joao@email.com", age=30)
```

#### Models Aninhados (Nested Models)

Você pode usar models dentro de models:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class User(BaseModel):
    name: str
    email: str
    address: Address  # Model dentro de model

# Criando com dados aninhados
user = User(
    name="João",
    email="joao@email.com",
    address={
        "street": "Rua A, 123",
        "city": "São Paulo",
        "country": "Brasil",
        "zip_code": "01310-100"
    }
)

print(user.address.city)  # São Paulo
print(user.address.country)  # Brasil
```

#### Exemplo Prático: Seu Projeto

Você pode criar models para seu FastAPI:

```python
# fast_api/schemas/schemas.py
from pydantic import BaseModel, field_validator

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

    @field_validator('age')
    @classmethod
    def age_must_be_valid(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Idade deve estar entre 0 e 150')
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

# fast_api/app.py
from fastapi import FastAPI
from fast_api.schemas.schemas import UserCreate, UserResponse

app = FastAPI()

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    # user é automaticamente validado como UserCreate
    # Se age estiver fora do intervalo, FastAPI rejeita
    return UserResponse(id=1, name=user.name, email=user.email, age=user.age)
```

#### Config do BaseModel

Você pode configurar o comportamento do model:

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,      # Remove espaços em branco
        validate_default=True,          # Valida valores padrão
        extra='forbid'                  # Rejeita campos extras
    )
    
    name: str
    email: str
    age: int = 18

# ✅ Espaços serão removidos
user = User(name="  João  ", email="joao@email.com", age=30)
print(user.name)  # João (sem espaços)

# ❌ Campo extra rejeitado
try:
    user = User(name="João", email="joao@email.com", age=30, telefone="11999999")
except Exception as e:
    print(f"Erro: Campo telefone não permitido")
```

#### Herança de Models

Você pode herdar models para reutilizar campos:

```python
from pydantic import BaseModel

class BaseUser(BaseModel):
    name: str
    email: str

class UserCreate(BaseUser):
    password: str  # Campo adicional

class UserResponse(BaseUser):
    id: int  # Campo adicional

# UserCreate tem: name, email, password
# UserResponse tem: name, email, id
```

#### Métodos Úteis do BaseModel

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

user = User(name="João", email="joao@email.com", age=30)

# Converter para dicionário
user_dict = user.model_dump()

# Converter para JSON string
user_json = user.model_dump_json()

# Criar a partir de dicionário
user2 = User.model_validate({"name": "Maria", "email": "maria@email.com", "age": 25})

# Criar a partir de JSON string
user3 = User.model_validate_json('{"name":"Pedro","email":"pedro@email.com","age":35}')

# Obter schema JSON para documentação
schema = User.model_json_schema()

# Copiar model com atualizações
user_copy = user.model_copy(update={"age": 31})
```

#### Comparação: Com e Sem Pydantic

**❌ Sem Pydantic (Inseguro):**
```python
def create_user(data):
    # Você precisa validar manualmente tudo
    if not isinstance(data.get('name'), str):
        return {"error": "name deve ser string"}
    if not isinstance(data.get('age'), int):
        return {"error": "age deve ser int"}
    if data['age'] < 0 or data['age'] > 150:
        return {"error": "age deve estar entre 0 e 150"}
    # ... muito código repetitivo
```

**✅ Com Pydantic (Seguro):**
```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int
    
    @field_validator('age')
    @classmethod
    def age_valid(cls, v):
        if v < 0 or v > 150:
            raise ValueError('age deve estar entre 0 e 150')
        return v

# Tudo validado automaticamente
user = User(name="João", age=30)
```

#### Benefícios do Pydantic

| Benefício | Descrição |
|-----------|-----------|
| **Type Safety** | Garante tipos de dados corretos |
| **Documentação** | Tipos indicam claramente a estrutura |
| **Validação** | Rejeita dados inválidos automaticamente |
| **Conversão** | Converte tipos compatíveis automaticamente |
| **Segurança** | Previne ataques com dados malformados |
| **Performance** | Validação rápida com C acelerado |
| **Integração FastAPI** | FastAPI usa Pydantic internamente |
| **Reutilização** | Models podem ser herdados e combinados |

#### Conclusão

Pydantic e BaseModel são essenciais para desenvolvimento web robusto em Python. Eles garantem que seus dados estejam sempre válidos, bem-estruturados e seguros. Quando combinados com FastAPI, você obtém uma solução poderosa para construir APIs profissionais com validação automática, documentação automática e tratamento de erros elegante. Use Pydantic em todos os seus projetos Python para código mais seguro e confiável!



