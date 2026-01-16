# fast_api API Project

## CRUD

CRUD é um acrônimo que representa as quatro operações básicas em qualquer sistema que trabalha com dados:

### O que é CRUD?

- **C** - Create (Criar): Inserir novos dados no banco de dados
- **R** - Read (Ler): Recuperar/buscar dados existentes
- **U** - Update (Atualizar): Modificar dados já existentes
- **D** - Delete (Deletar): Remover dados do banco de dados

---

### CRUD em FastAPI

Em uma aplicação FastAPI, as operações CRUD são implementadas através de **endpoints HTTP** que utilizam os diferentes métodos HTTP:

#### 1. **CREATE (POST)**
```python
@app.post("/items/")
def create_item(item: ItemSchema):
    # Lógica para salvar o item no banco de dados
    return {"message": "Item criado com sucesso", "item": item}
```
- Método HTTP: `POST`
- Objetivo: Inserir um novo recurso
- Status de sucesso: `201 Created` ou `200 OK`

#### 2. **READ (GET)**
```python
@app.get("/items/")
def read_items():
    # Recupera todos os itens
    return items

@app.get("/items/{item_id}")
def read_item(item_id: int):
    # Recupera um item específico pelo ID
    return item
```
- Método HTTP: `GET`
- Objetivo: Recuperar dados existentes
- Status de sucesso: `200 OK`

#### 3. **UPDATE (PUT/PATCH)**
```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemSchema):
    # Atualiza um item completo
    return {"message": "Item atualizado", "item": item}

@app.patch("/items/{item_id}")
def partial_update_item(item_id: int, item: ItemSchema):
    # Atualiza parcialmente um item
    return {"message": "Item parcialmente atualizado"}
```
- Método HTTP: `PUT` (atualização completa) ou `PATCH` (atualização parcial)
- Objetivo: Modificar dados existentes
- Status de sucesso: `200 OK`

#### 4. **DELETE (DELETE)**
```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    # Remove um item do banco de dados
    return {"message": "Item deletado com sucesso"}
```
- Método HTTP: `DELETE`
- Objetivo: Remover um recurso
- Status de sucesso: `200 OK` ou `204 No Content`

---

### Boas Práticas para CRUD em FastAPI

1. **Use tipos de dados corretos**: Utilize Pydantic models para validação automática
2. **Implemente status HTTP apropriados**: Retorne os códigos corretos (201, 404, 400, etc.)
3. **Valide os dados**: FastAPI faz isso automaticamente com Pydantic
4. **Trate erros**: Use `HTTPException` para erros específicos
5. **Use path parameters para IDs**: Ex: `/items/{item_id}`
6. **Use query parameters para filtros**: Ex: `/items?skip=0&limit=10`

---

### Exemplo Completo de CRUD

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

# Simula um banco de dados
users_db = []

# CREATE
@app.post("/users/")
def create_user(user: User):
    users_db.append(user)
    return {"message": "Usuário criado", "user": user}

# READ - Todos
@app.get("/users/")
def read_users():
    return users_db

# READ - Um específico
@app.get("/users/{user_id}")
def read_user(user_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# UPDATE
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    users_db.remove(user)
    users_db.append(updated_user)
    return {"message": "Usuário atualizado", "user": updated_user}

# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    users_db.remove(user)
    return {"message": "Usuário deletado"}
```