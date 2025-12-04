# Carteira Digital Crypto Conversion BR

![GitHub repo size](https://img.shields.io/github/repo-size/Carloscavalcante3/Crypto-Conversion-BR)
![GitHub contributors](https://img.shields.io/github/contributors/Carloscavalcante3/Crypto-Conversion-BR)
![GitHub stars](https://img.shields.io/github/stars/Carloscavalcante3/Crypto-Conversion-BR?style=social)
![GitHub forks](https://img.shields.io/github/forks/Carloscavalcante3/Crypto-Conversion-BR?style=social)

**Carteira Digital Crypto Conversion BR** é uma API RESTful completa que permite realizar operações financeiras multi-moeda, incluindo depósitos, saques, transferências e conversões via API externa (Coinbase). O projeto foi construído com arquitetura em **Três Camadas**, uso obrigatório de **SQL Puro** e banco **PostgreSQL**, garantindo segurança, organização e aderência total aos requisitos funcionais.

A solução foi desenvolvida em cinco mini-sprints, cobrindo 100% das regras do sistema de carteira digital.

---


## 👥 Equipe

| Nome  | GitHub |
|-------|--------|
| Carlos Cavalcante | [@Carloscavalcante3](https://github.com/Carloscavalcante3) |
| Luiz Henrique Cavalcanti | [@lhickk17](https://github.com/lhickk17) |
| Nathalia Carvalho Pascoal | [@nathaliacarvalhop](https://github.com/nathaliacarvalhop) |
| Maria Eduarda Pernambuco | [@mariaeduardapernambuco](https://github.com/mariaeduardapernambuco) |

---


## 🔧 Pré-requisitos

Antes de começar, certifique-se de que você atendeu aos seguintes requisitos:

- Python **3.10+** instalado
- Servidor **PostgreSQL** rodando (porta 5432)
- Git instalado
- Leitura do arquivo `sql/DDL_Carteira_Digital.sql`

---

## 📦 Instalação — Carteira Digital Crypto Conversion BR

### Linux e macOS:
```bash
git clone https://github.com/Carloscavalcante3/Crypto-Conversion-BR.git
cd Crypto-Conversion-BR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows:
```bash
git clone https://github.com/Carloscavalcante3/Crypto-Conversion-BR.git
cd Crypto-Conversion-BR
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Usando o projeto

### 1️⃣ Configure o Banco de Dados
Execute no pgAdmin ou outro cliente SQL:
```
sql/DDL_Carteira_Digital.sql
```

### 2️⃣ Configure o arquivo `.env`
```
DB_HOST=localhost
DB_PORT=5432
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=carteira_digital
```

### 3️⃣ Inicie o servidor
```bash
python -m uvicorn api.main:app --reload
```

### 4️⃣ Acesse a documentação:
```
http://127.0.0.1:8000/docs
```

Todas as operações podem ser testadas, incluindo:
- Criação de carteiras
- Depósitos
- Saques (taxa 1%)
- Conversões (taxa 2% via Coinbase)
- Transferências (taxa 1%)

---

## 📋 Arquitetura do Projeto

| Camada | Função | Tecnologia |
|-------|--------|------------|
| API/Roteamento | Endpoints REST | FastAPI / Uvicorn |
| Serviço | Regras de Negócio, Coinbase, Validações | Python + httpx |
| Persistência | SQL Puro via SQLAlchemy Core | SQLAlchemy Core |
| Banco | Armazenamento | PostgreSQL |
