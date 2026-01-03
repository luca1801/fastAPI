from fastapi import FastAPI

app = FastAPI()  # iniciando uma aplicação FastAPI


# Definindo um endpoint com o endereço / acessível pelo método HTTP GET
@app.get('/')
def read_root():
    return {'message': 'Hello World!'}
