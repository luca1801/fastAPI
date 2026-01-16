# Importa BaseSettings do pydantic para validar variáveis de ambiente
from pydantic_settings import BaseSettings, SettingsConfigDict


# Classe que define todas as configurações da aplicação
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    # Variável de ambiente para URL do banco de dados
    DATABASE_URL: str
    # Variável de ambiente para chave secreta
    # SECRET_KEY: str


# Cria uma instância global das configurações
settings = Settings()
