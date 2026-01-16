<style>
code {
  # background-color: #f5eb9cff;
  padding: 1px 2px;
  border-radius: 2px;
}
pre {
  background-color: #3d4b4adb !important;
  #border: 1px solid #c9cdf9ff !important;
  border-radius: 4px;
  padding: 6px !important;
}
pre code {
  background-color: transparent;
  padding: 0;
}
blockquote{
  #border: 5px;
  #border-radius: 4px;
  #padding: 2px !important;
  #font-size: 9px
  #color: #e1f90aff;
  
}
</style>

# fast_api API Project

## Configuração

### Pipx

Ferramenta usada para instalar e executar ferramentas Python globalmente no sistema de forma segura. Diferente do `pip`, que instala pacotes no ambiente global, o `pipx` isola cada ferramenta em um ambiente virtual, evitando "sujar" o ambiente do sistema.

Para instalar o `pipx` no Ubuntu Server, rode:

```bash
sudo apt install pipx
pipx ensurepath
```


O comando `pipx ensurepath` adiciona ao `PATH` do sistema os binários instalados pelo `pipx`. Após executar, reinicie o shell para que a alteração tenha efeito.

### Poetry

O `Poetry` é um gerenciador de projetos Python que cuida de dependências, ambientes virtuais e publicação de pacotes. No projeto usaremos o `Poetry` para criar e manter o ambiente do projeto.

Instalação do `poetry` via `pipx`:

>___
```bash
pipx install poetry
```

Opcional: habilitar o plugin que fornece o comando `poetry shell`:

```bash
pipx inject poetry poetry-plugin-shell
```

O comando `pipx inject` instala pacotes dentro do ambiente virtual do `poetry` gerenciado pelo `pipx`.

### Python

Depois de instalar o `Poetry`, podemos instruí-lo a usar uma versão específica do Python disponível no sistema ou pedir para o poetry baixar uma versão específica para usar no projeto.

```bash
poetry python install 3.14
# ou, se necessário, informar o caminho completo do executável:
poetry env use 3.14

# se quiser informar o caminho completo do executável, caso queira usar o executável do python instalado no sistema, por exemplo:
poetry env use /usr/bin/python3.12
```

O comando `poetry python list` mostra todos as versões do python disponível.<br>
Nota: o `Poetry` não baixa automaticamente versões do Python — o executável pode estar instalado no sistema (por exemplo via `pyenv` ou instalador do sistema).

### Criando um projeto

Para criar um novo projeto com `poetry` (exemplo usando o nome `fastAPI`):

```bash
poetry new --flat fast_API
```

Isso criará a estrutura básica:

```
.
├── fastAPI
│  └── __init__.py
├── pyproject.toml
├── README.md
└── tests
   └── __init__.py
```

Depois de entrar no diretório do projeto, confirme que o `poetry` está usando a versão correta do Python (veja a seção "Python" acima).

No `pyproject.toml` especifique a versão mínima do Python suportada pelo projeto:

```toml
[project]
# ...
requires-python = ">=3.14,<4.0"
```

A expressão `">=3.14,<4.0"` significa que qualquer versão maior ou igual a 3.14 será válida para o projeto menos a 4.0 para baixo.

### Instalando o FastAPI

Com toda a base do nosso projeto pronta, podemos finalmente instalar o FastAPI.

```bash
poetry install 
poetry add 'fastapi[standard]' 
```
### Primeira Execução de um "Hello, World!"


Uma coisa bastante interessante sobre o FastAPI é que ele é um framework web baseado em funções. Da mesma forma em que criamos funções tradicionalmente em python, podemos estender essas funções para que elas sejam servidas pelo servidor. Por exemplo:

```python
def read_root():
    return {'message': 'Olá Mundo!'}
```

Essa função em python basicamente retorna um dicionário com uma chave chamada 'message' e uma mensagem 'Olá Mundo!'. Se adicionarmos essa função em novo arquivo chamado app.py no diretório fast_zero. Podemos fazer a chamada dela pelo terminal interativo (REPL):

```bash
python3 -i app.py
```
```bash
>>> read_root()
{'message': 'Olá Mundo!'}
```

Agora, partindo para a implementação em `fastapi`, usamos um decorador e podemos fazer com que uma determinada função seja acessível pela rede.

```python
from fastapi import FastAPI 

app = FastAPI()  

@app.get('/')  
def read_root():  
    return {'message': 'Olá Mundo!'}
```

A linha em destaque @app.get('/') expõe a nossa função para ser servida pelo `FastAPI`. Dizendo que quando um cliente acessar o nosso endereço de rede no caminho /, usando o método `HTTP GET`, a função será executada. Desta maneira, temos todo o código necessário para criar nossa primeira aplicação web com `FastAPI`.

Antes de iniciarmos nossa aplicação, temos que fazer um passo importante, habilitar o ambiente virtual, para que o python consiga enxergar nossas dependências instaladas. O `poetry` tem um comando específico para isso:

```bash
poetry shell
```

Agora com o ambiente virtual ativo, podemos iniciar nosso servidor `FastAPI` para iniciar nossa aplicação:

```bash
fastapi dev fast_api/app.py
```

Esse comando diz ao `FastAPI` para iniciar o servidor de desenvolvimento (dev) usando o arquivo `fast_api/app.py`

Obs: Também é possível executar os comandos sem entrar no shell do ambiente virtual. É mais verboso, mas funciona bem:

```bash
poetry run fastapi dev fast_api/app.py
```

Quando executamos nossa aplicação FastAPI a mensagem de resposta do CLI: `serving: http://127.0.0.1:8000 `tem uma informação bastante importante.

1. Ela nos mostra qual protocolo está sendo utilizado, no caso o HTTP, que é o protocolo padrão da web;
2. O endereço de rede (IP) que está escutando, no caso 127.0.0.1, endereço especial (loopback) que aponta para a nossa própria máquina;
3. A porta :8000, a qual é a porta da nossa máquina que está reservada para nossa aplicação.

Agora, com o servidor inicializado, podemos usar um cliente para acessar o endereço `http://127.0.0.1:8000`.

O cliente mais tradicional da web é o navegador, podemos digitar o endereço na barra de navegação e se tudo ocorreu corretamente, você deve ver a mensagem `"Olá Mundo!"` em formato `JSON`.

### Documentação padrão

O fastapi já vem com aplicações de documentação nativa, o 'swagger' e o 'redoc'.

* `Swagger`: Se acessarmos `http://127.0.0.1:8000/docs` podemos ver os endpoints da nossa aplicação e testar os requests

* `redoc`: Se acessarmos `http://127.0.0.1:8000/redoc` podemos ver os endpoints e suas respostas de forma mais detalhada.

### Instalando as ferramentas de desenvolvimento

As escolhas de ferramentas de desenvolvimento, de forma geral, são escolhas bem particulares. Não costumam ser consensuais nem mesmo em times de desenvolvimento. Dito isso, selecionei algumas ferramentas que gosto de usar e alinhadas com a utilidade que elas apresentam no desenvolvimento do projeto.

As ferramentas escolhidas são:

* `taskipy`: ferramenta usada para criação de comandos. Como executar a aplicação, rodar os testes, etc.
* `pytest`: ferramenta para escrever e executar testes
* `ruff`: Uma ferramenta que tem duas funções no nosso código:

    a. Um analisador estático de código (um linter), para dizer se não estamos infringindo alguma boa prática de programação;
    
    b. Um formatador de código. Para seguirmos um estilo único de código. Vamos nos basear na PEP-8.

Para instalar essas ferramentas que usaremos em desenvolvimento, podemos usar um grupo de dependências (`--group dev` no poetry) focado nelas, para não serem instaladas quando nossa aplicação estiver em produção:

```bash
poetry add --group dev pytest pytest-cov taskipy ruff
```

#### Ruff

Para configurar o `Ruff` montamos a configuração em 3 tabelas distintas no arquivo pyproject.toml. Uma para as configurações globais, uma para o linter e uma para o formatador.

**Configuração global**

Na configuração global do `Ruff` queremos alterar somente duas coisas. O comprimento de linha para 79 caracteres (conforme sugerido na `PEP-8`) e, em seguida, informaremos que o diretório de migrações de banco de dados será ignorado na checagem e na formatação (Nessa fase de configuração, excluiremos a pasta migrations, isso pode não fazer muito sentido nesse momento. Contudo, quando iniciarmos o trabalho com o banco de dados, a ferramenta Alembic faz geração de código automático. Por serem códigos gerados automaticamente, não queremos alterar a configuração feita por ela).

**Configuração linter**

Durante a análise estática do código, queremos buscar por coisas específicas. No `Ruff`, precisamos dizer exatamente o que ele deve analisar. Isso é feito por códigos. Usaremos estes:

* **I** (`Isort`): Checagem de ordenação de imports em ordem alfabética
* **F** (`Pyflakes`): Procura por alguns erros em relação a boas práticas de código
* **E** (`Erros pycodestyle`): Erros de estilo de código
* **W** (`Avisos pycodestyle`): Avisos de coisas não recomendadas no estilo de código
* **PL** (`Pylint`): Como o *F*, também procura por erros em relação a boas práticas de código
* **PT** (`flake8-pytest`): Checagem de boas práticas do Pytest

**Configuração Formatter**

A formatação do `Ruff` praticamente não precisa ser alterada. Pois ele vai seguir as boas práticas e usar a configuração global de 79 caracteres por linha. A única alteração que farei é o uso de aspas simples ' no lugar de aspas duplas " como padrão do projeto.

```toml
# Configuração global do Ruff
[tool.ruff]
line-length = 79
extend-exclude = [
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "migrations"
]

# Configuração específica para linting do ruff
[tool.ruff.lint]
preview = true
select = [ 'I', 'E', 'F', 'W', 'PL', 'PT']

# Confuguração de formatação do ruff
[tool.ruff.format]
preview = true
quotes = 'single'
```

**Usando o Ruff**

* `ruff check .` :  Faz a checagem dos termos que definimos antes.
* `ruff format .` :  Faz a formatação automáticado do nosso código conforme foi configurado.

#### Pytest

O Pytest é uma framework de testes, que usaremos para escrever e executar nossos testes. O configuraremos para reconhecer o caminho base para execução dos testes na raiz do projeto `./fastAPI`.
Na segunda linha, dizemos para o pytest adicionar a opção `no:warnings` para ter uma visualização mais limpa dos testes, caso alguma biblioteca exiba uma mensagem de warning, isso será suprimido pelo pytest.

```toml
[tool.pytest.ini_options]
pyhtonpath = ['./fastAPI']
addopts = "-p no:warnings"
```
#### Taskipy

A ideia do `Taskipy` é ser um executor de tarefas (*task runner*) complementar em nossa aplicação. No lugar de ter que lembrar comandos como o do fastapi, que vimos na execução da aplicação, que tal substituir ele simplesmente por `task run`?

Isso funcionaria para qualquer comando complicado em nossa aplicação. Simplificando as chamadas e também para não termos que lembrar de como executar todos os comandos de cabeça.Alguns comandos que criaremos agora no início:

```toml
[tool.taskipy.tasks]
lint = 'ruff check'
pre_format = 'ruff check --fix'
format = 'ruff format'
run = 'fastapi dev fast_zero/app.py'
pre_test = 'task lint'
test = 'pytest -s -x --cov=fast_zero -vv'
post_test = 'coverage html'
```


* **`lint`**: Faz a checagem de boas práticas do código python
* **`pre_format`**: Faz algumas correções de boas práticas automaticamente
* **`format`**: Executa a formatação do código em relação às convenções de estilo de código
* **`run`**: executa o servidor de desenvolvimento do FastAPI
* **`pre_test`**: executa a camada de lint antes de executar os testes
* **`test`**: executa os testes com pytest de forma verbosa (-vv) e adiciona nosso código como base de cobertura
* **`post_test`**: gera um report de cobertura após os testes


### Entendendo os conceitos de Testes

Antes de entendermos a dinâmica dos testes, precisamos entender o efeito que eles têm no nosso código. Podemos começar analisando a cobertura (o quanto do nosso código está sendo efetivamente testado). Vamos executar os testes:

* **`task test`** : executa os testes na aplicação e gera um relatório no terminal.
* **`task post_test`** : Isso gera um relatório de cobertura de testes em formato HTML. Podemos abrir esse arquivo em nosso navegador e entender exatamente quais linhas do código não estão sendo testadas.


**Escrevendo um Teste**

Agora, escreveremos nosso primeiro teste com `Pytest`. Mas, antes de escrever o teste, precisamos criar um arquivo específico para eles. Na pasta `tests`, vamos criar um arquivo chamado `test_app.py`.

Para testar o código feito com FastAPI, precisamos de um cliente de teste. A grande vantagem é que o FastAPI já conta com um cliente de testes no módulo `fastapi.testclient `com o objeto `TestClient`, que precisa receber nosso app como parâmetro:

```python
from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api.app import app

def teste_root_deve_retornar_hello_world():
    client = TestClient(app)  # Arrange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Hello World!'}  # Assert
```

Esse teste faz uma requisição `GET` no endpoint `/` e verifica se o código de status da resposta é `200` e se o conteúdo da resposta é `{'message': 'Olá Mundo!'}`.

Dessa forma, temos um teste que coletou 1 item (1 teste). Esse teste foi aprovado e a cobertura não deixou de abranger nenhuma linha de código.
Como conseguimos coletar um item, o `post_test` foi executado e também gerou um HTML com a cobertura atualizada.

**Estrutura de um teste**

Agora que escrevemos nosso primeiro teste de forma intuitiva, podemos entender o que cada passo do teste faz. Essa compreensão é vital, pois nos ajudará a escrever testes com mais confiança e eficácia. Para desvendar o método por trás da nossa abordagem, exploraremos uma estratégia conhecida como AAA, que divide o teste em três fases distintas: Arrange, Act, Assert.

Com base no código de teste anterior, podemos observar as três fases:

**Fase 1 - Organizar (Arrange)**:

Nesta primeira etapa, estamos preparando o ambiente para o teste. No exemplo, a linha com o comentário Arrange não é o teste em si, ela monta o ambiente para o teste poder ser executado. Estamos configurando um client de testes para fazer a requisição ao app.

**Fase 2 - Agir (Act)**:

Aqui é a etapa onde acontece a ação principal do teste, que consiste em chamar o Sistema Sob Teste (SUT). No nosso caso, o SUT é a rota /, e a ação é representada pela linha response = client.get('/'). Estamos exercitando a rota e armazenando sua resposta na variável response. É a fase em que o código de testes executa o código de produção que está sendo testado. Agir aqui significa interagir diretamente com a parte do sistema que queremos avaliar, para ver como ela se comporta.

**Fase 3 - Afirmar (Assert)**:

Esta é a etapa de verificar se tudo correu como esperado. É fácil notar onde estamos fazendo a verificação, pois essa linha sempre tem a palavra reservada assert. A verificação é booleana, ou está correta, ou não está. Por isso, um teste deve sempre incluir um assert para verificar se o comportamento esperado está correto.

### Criando nosso repositório GIT

**Criando o arquivo `.gitignore`**

Criado o arquivo `.gitignore` e copiado o conteúdo do arquivo semelhante do projeto original [fastapi-do-zero](https://github.com/dunossauro/fastapi-do-zero/blob/main/.gitignore) 

<!-- Vamos iniciar com a criação de um arquivo `.gitignore` específico para Python. Existem diversos modelos disponíveis na internet, como os disponíveis pelo próprio GitHub, ou o gitignore.io. Uma ferramenta útil é a `ignr`, feita em Python, que faz o download automático do arquivo para a nossa pasta de trabalho atual:

```bash
pipx run ignr -p python > .gitignores
```
O `.gitignore` é importante porque ele nos ajuda a evitar que arquivos desnecessários ou sensíveis sejam enviados para o repositório. Isso inclui o ambiente virtual, arquivos de configuração pessoal, entre outros. -->

#### Criando um repositório no github

Agora, com nossos arquivos indesejados ignorados, podemos iniciar o versionamento de código usando o `git`. Para criar um repositório local, usamos o comando `git init .`. Para criar esse repositório no GitHub, utilizaremos o gh, um utilitário de linha de comando que nos auxilia nesse processo:

```bash
git init .
gh repo create
git add .
git commit -m "Configuração inicial do projeto"
git push
```

Ao executar `gh repo create`, algumas informações serão solicitadas, como o nome do repositório e se ele será público ou privado. Isso irá criar um repositório tanto localmente quanto no GitHub.


Com o repositório pronto, vamos versionar nosso código. Primeiro, adicionamos o código ao próximo commit com `git add .`. Em seguida, criamos um ponto na história do projeto com` git commit -m "Configuração inicial do projeto"`. Por fim, sincronizamos o repositório local com o remoto no GitHub usando `git push`

```
Obs: Caso seja a primeira vez que está utilizando o git push, talvez seja necessário configurar suas credenciais(nome, email) do GitHub.
```