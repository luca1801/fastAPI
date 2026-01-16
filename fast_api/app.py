from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_api.schemas.schemas import (
    MessageSchema,
    UserDB,
    UserList,
    UserSchema,
    UserSchemaPublic,
)

app = FastAPI()  # iniciando uma aplicação FastAPI

database = []  # lista que simula um banco de dados


# Definindo um endpoint com o endereço / acessível pelo método HTTP GET
@app.get('/', status_code=HTTPStatus.OK, response_model=MessageSchema)
def read_root():
    return {'message': 'Hello World!'}


@app.post(
    '/users', status_code=HTTPStatus.CREATED, response_model=UserSchemaPublic
)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        **user.model_dump(),
        id=len(database) + 1,
    )
    database.append(user_with_id)
    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users():
    return {'users': database}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaPublic,
)
def update_user(user: UserSchema, user_id: int):
    user_with_id = UserDB(
        **user.model_dump(),
        id=user_id,
    )
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    database[user_id - 1] = user_with_id
    return user_with_id


# @app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserSchemaPublic,
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    return database.pop(user_id - 1)
