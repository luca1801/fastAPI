from fastapi import FastAPI

from fast_api.routers import auth, company, users

app = FastAPI()  # iniciando uma aplicação FastAPI

# database = []  # lista que simula um banco de dados

# Incluir rotas
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(company.router)
