# SIGMA

Sistema de gestão acadêmica — uma API REST que implementa um CRUD completo de alunos
(criar, consultar, alterar e excluir), acessando um banco de dados PostgreSQL.

## Tecnologias

- **Python 3.13**
- **FastAPI** — framework web, com documentação interativa automática
- **SQLAlchemy (async)** — ORM para acesso ao banco de forma assíncrona
- **asyncpg** — driver assíncrono do PostgreSQL
- **Pydantic / pydantic-settings** — validação de dados e configuração
- **PostgreSQL** — banco de dados (hospedado no Aiven)

## Pré-requisitos

- Python 3.13 ou superior instalado
- Um banco de dados **PostgreSQL**. Este projeto foi desenvolvido usando o plano
  gratuito do [Aiven](https://aiven.io/free-postgresql-database), mas qualquer
  instância PostgreSQL funciona.

## Como configurar o banco de dados

A aplicação lê a conexão com o banco de uma variável de ambiente chamada
`DATABASE_URL`, que fica em um arquivo `.env` na raiz do projeto.

### 1. Obtenha uma instância PostgreSQL

No [Aiven](https://aiven.io/free-postgresql-database), crie um serviço PostgreSQL
gratuito. Após criado, na tela do serviço, em **Connection information**, você
encontrará: host, porta, usuário, senha e nome do banco.

### 2. Crie o arquivo `.env`

Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env` e
preencha com os dados da sua instância:

```
DATABASE_URL=postgresql+asyncpg://<usuario>:<senha>@<host>:<porta>/<banco>?ssl=require
```

> **Atenção a dois detalhes obrigatórios na URL:**
> - O início deve ser `postgresql+asyncpg://` (e não `postgres://`), para usar o driver assíncrono.
> - O final deve ser `?ssl=require` (e não `?sslmode=require`), pois o driver `asyncpg` não reconhece `sslmode`.

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/HalissonJulio/SIGMA.git
cd SIGMA
```

### 2. Criar e ativar o ambiente virtual

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Popular o banco com dados de exemplo

Para inserir 50 alunos de exemplo e já ter dados para visualizar:

```bash
python seed.py
```

O script é seguro para rodar mais de uma vez: se o banco já tiver alunos, ele não
insere nada. Se você preferir começar com o banco vazio e cadastrar os alunos
manualmente, basta pular este passo.

### 5. Rodar a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em **http://127.0.0.1:8000**

Ao iniciar, a aplicação **cria automaticamente a tabela `aluno`** no banco (caso
ela ainda não exista). Não é necessário rodar nenhum script de criação à parte.

## Como testar

Acesse a documentação interativa no navegador:

**http://127.0.0.1:8000/docs**

Por ali é possível testar todos os endpoints clicando, sem precisar de ferramentas
externas.

Se você rodou o seed (passo 4), o **GET** já retornará os 50 alunos de exemplo.
Caso contrário, comece criando um aluno pelo **POST**. Sugestão de ordem para testar:

1. **POST** `/api/v1/alunos` — cria um aluno. Exemplo de corpo:

```json
{
  "matricula": 2024001,
  "nome": "Maria Silva",
  "cpf": "12345678900",
  "email": "maria@email.com",
  "telefone_responsavel": "11999998888"
}
```

2. **GET** `/api/v1/alunos` — lista todos os alunos cadastrados.
3. **GET** `/api/v1/alunos/{matricula}` — busca um aluno específico.
4. **PATCH** `/api/v1/alunos/{matricula}` — altera dados de um aluno.
5. **DELETE** `/api/v1/alunos/{matricula}` — remove um aluno.

## Endpoints

| Método | Rota                          | Descrição                  |
|--------|-------------------------------|----------------------------|
| GET    | `/api/v1/alunos`              | Lista todos os alunos      |
| GET    | `/api/v1/alunos/{matricula}`  | Busca um aluno por matrícula |
| POST   | `/api/v1/alunos`              | Cria um novo aluno         |
| PATCH  | `/api/v1/alunos/{matricula}`  | Atualiza um aluno          |
| DELETE | `/api/v1/alunos/{matricula}`  | Remove um aluno            |

## Estrutura do projeto

O projeto segue uma arquitetura em camadas, onde cada parte tem uma
responsabilidade única:

```
SIGMA/
├── app/
│   ├── main.py                  # inicializa a aplicação e cria as tabelas
│   ├── core/
│   │   ├── config.py            # configurações lidas do .env
│   │   └── database.py          # conexão async com o banco e pool de conexões
│   ├── models/
│   │   └── aluno.py             # tabela aluno (SQLAlchemy)
│   ├── schemas/
│   │   └── aluno.py             # validação de entrada/saída (Pydantic)
│   ├── repositories/
│   │   └── aluno.py             # acesso ao banco de dados
│   ├── services/
│   │   └── aluno.py             # regras de negócio
│   └── api/
│       ├── router.py            # agrega as rotas sob o prefixo /api/v1
│       └── routes/
│           └── aluno.py         # endpoints HTTP de aluno
├── seed.py                      # popula o banco com alunos de exemplo
├── requirements.txt
├── .env.example
└── README.md
```

O fluxo de uma requisição percorre as camadas em ordem: a rota recebe a requisição,
chama o service (regras de negócio), que chama o repositório (acesso ao banco), que
fala com o PostgreSQL. A resposta volta pelo mesmo caminho.