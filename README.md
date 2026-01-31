# CRUD de Usuários — FastAPI

API REST para gerenciamento de usuários, desenvolvida em Python com FastAPI, PostgreSQL e Redis, utilizando Docker Compose para orquestração dos serviços.

---

## 🚀 Stack Tecnológica

- **Python 3.12**
- **FastAPI**
- **SQLAlchemy (Async)**
- **PostgreSQL**
- **Redis**
- **Docker & Docker Compose**

---

## 📌 Funcionalidades

- Criar usuário
- Listar usuários com paginação
- Buscar usuário por ID
- Atualizar usuário
- Remover usuário
- Cache em Redis para consultas (`GET`)
- Invalidação automática de cache em operações de escrita

---

## 🧱 Arquitetura

O projeto segue uma arquitetura em camadas:

- **API (Controllers)**: definição das rotas
- **Services**: regras de negócio e cache
- **Repositories**: acesso a dados
- **Models**: mapeamento ORM
- **Schemas**: contratos da API
- **Core**: infraestrutura (DB, cache, config)

Essa separação garante organização, testabilidade e escalabilidade.

---

## ▶️ Como executar

### Pré-requisitos
- Docker
- Docker Compose

### Subir a aplicação
```bash
docker compose up --build

A aplicação estará disponível em:

API: http://localhost:8000

Swagger UI: http://localhost:8000/docs

📄 Endpoints

Criar usuário

POST /api/v1/usuarios

{
  "name": "João Silva",
  "email": "joao.silva@email.com",
  "age": 30
}

Listar usuários (paginado)

GET /api/v1/usuarios?limit=10&offset=0

Buscar usuário por ID

GET /api/v1/usuarios/{id}

Atualizar usuário

PUT /api/v1/usuarios/{id}

{
  "name": "João Atualizado"
}

Remover usuário

DELETE /api/v1/usuarios/{id}

⚙️ Variáveis de ambiente

Arquivo .env na raiz do projeto:

DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/users_db
REDIS_URL=redis://cache:6379/0
APP_ENV=development

🧪 Observações Técnicas

O cache é utilizado apenas em operações de leitura (GET).

O cache é invalidado automaticamente em operações de criação, atualização e remoção.

O banco de dados é inicializado automaticamente na primeira execução.

UUID é utilizado como chave primária para os usuários.

📦 Estrutura do Projeto
app/
├── api/
├── core/
├── models/
├── repositories/
├── schemas/
├── services/
└── main.py

📝 Licença

Projeto desenvolvido exclusivamente para fins de avaliação técnica.


## 🏁 Resultado final (visão da banca)

#Código organizado  
#Infra reprodutível  
#Cache consciente  
#API REST bem definida  
# README claro e objetivo  

