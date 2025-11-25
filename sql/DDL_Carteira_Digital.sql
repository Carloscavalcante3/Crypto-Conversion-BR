-- =========================================================
--  Script de criação da base, usuário,
--  Projeto: Carteira Digital
--  Banco:   PostgreSQL
-- =========================================================

-- 1) Criação da base de homologação
-- Requer a conexão inicial como superusuário (postgres)
CREATE DATABASE wallet_homolog;


-- 2) Criação do usuário restrito para a API
--    (ajuste a senha conforme necessário)
CREATE USER wallet_api_homolog WITH PASSWORD 'api123';


-- 3) Grants: apenas DML (sem CREATE/DROP/ALTER)
--    (Conceder permissão de conexão)
GRANT CONNECT ON DATABASE wallet_homolog TO wallet_api_homolog;

-- ATENÇÃO: Os grants DML para as tabelas devem ser executados após a criação das tabelas DDL.
-- É necessário rodar o seguinte comando na base 'wallet_homolog'
-- para conceder DML em todas as tabelas criadas e futuras:

-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO wallet_api_homolog;


-- =========================================================
--  Tabelas (Aluno deve fazer o modelo)
