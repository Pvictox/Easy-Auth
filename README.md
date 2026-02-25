# Easy - Auth

Um projeto de autenticação simples usando FastAPI, JWT e Redis para cache.

## Escopo

| Modelo | Descrição |
|-------|-----------|
| **Usuário** | Representa um usuário do sistema|
| **Token** | Representa um token JWT para autenticação |
| **Pefil** | Representa o perfil do usuário (admin, user, etc) |

## Como rodar a aplicação

1. Crie um arquivo `.env` na raiz do projeto. Siga o modelo do `env.example` para configurar as variáveis de ambiente.


### Modo com Docker (Recomendado):
1. Certifique-se de ter o Docker instalado e rodando.
2. Na raiz do projeto, execute (Se for usar o compose de desenvolvimento use o `docker-compose-dev.yml`, se for produção use o `docker-compose-prod.yml`):
   ```bash
   docker compose -f {nome_do_arquivo_compose} up --build
   ```

### Modo sem Docker (Não recomendado):
1. Crie um ambiente virtual (Aqui eu irei usar o `venv` do Python, mas você pode usar o `conda` ou outro de sua preferência):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Acesse a pasta `app` e rode a aplicação:
Desenvolvimento:
    ```bash
        fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload #Para Desenvolvimento
        fastapi run app/main.py --host 0.0.0.0 --port 8000 #Para Produção
    ```
