# readcsv

Projeto teste para cognitivo.io

### Requisitos

https://drive.google.com/file/d/1pO5RECTeubZnkSZ6t1ht6wu84231Xv-A/view

### Setup

1. Faça o clone do projeto no github: `git clone https://github.com/juniorcarvalho/readcsv.git`
2. Crie um virtualenv com `python-3.7`: `python -m venv .venv` 
3. Instale `docker` e `docker-compose`
4. Suba o banco de dados: `docker-compose-up`
5. Ative o virtualenv: `source .venv/bin/activate`
6. Instale as dependências: `pip install -r requirements-test.txt`
7. Copie o `env-sample` para `.env` e altere as variáveis de ambiente do django
8. Faça o setup inicial da base de dados: `python manage.py migrate`
9. Suba o servidor: `python manage.py runserver`
10. Acesse `localhost:8000`

### Rodando os testes

1. Ative o virtualenv: `source .venv/bin/activate`
2. Execute: `pytest -s -vvv`


### twitter api
Configure as seguintes variáves no .env

TWITTER_API_KEY=

TWITTER_SECRET_KEY=

TWITTER_ACCESS_TOKEN=

TWITTER_ACCESS_TOKEN_SECRET=
