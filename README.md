# Carteira Digital Crypto Conversion BR 🪙

**Projeto de Implementação de uma API de Carteira Digital** para a disciplina Projeto Banco de Dados, focada em segurança, uso de SQL puro e integração com serviços externos.

## 👥 Equipe

| Nome  | GitHub |
|-------|--------|
| Carlos Cavalcante | [@Carloscavalcante3](https://github.com/Carloscavalcante3) |
| Gustavo Lino | [@GustavoLino728](https://github.com/GustavoLino728) |
| Luiz Henrique Cavalcanti | [@lhickk17](https://github.com/lhickk17) |
| Nathalia Carvalho Pascoal | [@nathaliacarvalhop](https://github.com/nathaliacarvalhop) |
| Maria Eduarda Pernambuco | [@mariaeduardapernambuco](https://github.com/mariaeduardapernambuco) |

## 🏗️ Arquitetura do Projeto
A solução segue um modelo de três camadas focado em modularidade e requisitos não funcionais do projeto:

* **API (FastAPI):** Lógica de roteamento e *endpoints* RESTful.
* **Service Layer:** Lógica de negócio e regras de validação (ex: saldo suficiente, hash de chave privada).
* **Persistence Layer:** Repositórios que utilizam **SQLAlchemy Core** para comunicação direta via **SQL Puro** com o banco de dados.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** **Python 3**
* **Framework:** **FastAPI** (para API RESTful)
* **Servidor:** **Uvicorn**
* **Banco de Dados:** **PostgreSQL** (Adaptado do MySQL original)
* **Acesso a Dados:** **SQLAlchemy Core** + **SQL Puro**
* **Segurança:** Módulos `secrets` e `hashlib` para geração e *hashing* de chaves.

## 🎯 Status do Projeto

### Sprint 1  ✅

Todo o ambiente de desenvolvimento e infraestrutura base foram configurados e validados.

### 📝Entregáveis da Sprint 1

| Requisito | Status | Prova de Conclusão (Base) |
| :--- | :--- | :--- |
| **Ambiente DB (PostgreSQL)** | OK | Base `wallet_homolog` e usuário restrito `wallet_api_homolog` criados. |
| **Configuração** | OK | Arquivo `.env` configurado com credenciais de acesso ao PostgreSQL na porta 5432. |
| **Estrutura API (FastAPI)** | OK | Estrutura de módulos (`api/main.py`, `/routers`, `/services`, `/persistence`) pronta. |
| **API em Execução** | OK | Uvicorn inicia sem erros de importação ou conexão inicial. |
| **Endpoint de Teste** | OK | Acesso à rota `/` retorna `{"message": "API rodando com sucesso!"}`. |

---

## Detalhes da Infraestrutura Utilizada

| Componente | Tecnologia | Configuração |
| :--- | :--- | :--- |
| **Servidor API** | FastAPI + Uvicorn | Python 3.10+ |
| **Banco de Dados** | **PostgreSQL** (Adaptado do MySQL original) | Conexão via `psycopg2-binary` e SQLAlchemy Core. |
| **Acesso a Dados** | Repositórios com **SQL Puro** | Usuário de banco de dados restrito (apenas DML). |

---

## 🚀 Como Executar (A partir da Raiz do Projeto)

### 1. Pré-requisitos

O **PostgreSQL** deve estar instalado e o banco `wallet_homolog` com o usuário `wallet_api_homolog` devem estar criados e com as tabelas **`CARTEIRA`**, **`MOEDA`** e **`SALDO_CARTEIRA`** inicializadas (Mini-Sprint 2 - DDL).

### 2. Inicie o Servidor

Abra o terminal, ative o `venv` e execute o seguinte comando:

```bash
python -m uvicorn api.main:app --reload