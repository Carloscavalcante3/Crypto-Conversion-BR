CREATE TABLE CARTEIRA (
    endereco_carteira VARCHAR(64) PRIMARY KEY, 
    hash_chave_privada VARCHAR(64) NOT NULL,
    data_criacao TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(10) NOT NULL DEFAULT 'ATIVA' 
);

CREATE TABLE MOEDA (
    id_moeda SMALLSERIAL PRIMARY KEY, 
    codigo VARCHAR(10) UNIQUE NOT NULL, 
    nome VARCHAR(50) NOT NULL,
    tipo VARCHAR(10) NOT NULL
);

CREATE TABLE SALDO_CARTEIRA (
    endereco_carteira VARCHAR(64) NOT NULL REFERENCES CARTEIRA (endereco_carteira),
    id_moeda SMALLINT NOT NULL REFERENCES MOEDA (id_moeda),
    saldo NUMERIC(18, 8) NOT NULL DEFAULT 0.00000000,
    data_atualizacao TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (endereco_carteira, id_moeda)
);

CREATE TABLE DEPOSITO_SAQUE (
    id_movimentacao BIGSERIAL PRIMARY KEY,
    endereco_carteira VARCHAR(64) NOT NULL REFERENCES CARTEIRA (endereco_carteira),
    id_moeda SMALLINT NOT NULL REFERENCES MOEDA (id_moeda),
    tipo VARCHAR(10) NOT NULL, 
    valor NUMERIC(18, 8) NOT NULL,
    taxa_valor NUMERIC(18, 8) NOT NULL DEFAULT 0.00,
    data_hora TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CONVERSAO (
    id_conversao BIGSERIAL PRIMARY KEY,
    endereco_carteira VARCHAR(64) NOT NULL REFERENCES CARTEIRA (endereco_carteira),
    id_moeda_origem SMALLINT NOT NULL REFERENCES MOEDA (id_moeda),
    id_moeda_destino SMALLINT NOT NULL REFERENCES MOEDA (id_moeda),
    valor_origem NUMERIC(18, 8) NOT NULL,
    valor_destino NUMERIC(18, 8) NOT NULL,
    taxa_percentual NUMERIC(5, 4) NOT NULL,
    taxa_valor NUMERIC(18, 8) NOT NULL,
    cotacao_utilizada NUMERIC(18, 8) NOT NULL,
    data_hora TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TRANSFERENCIA (
    id_transferencia BIGSERIAL PRIMARY KEY,
    endereco_origem VARCHAR(64) NOT NULL REFERENCES CARTEIRA (endereco_carteira),
    endereco_destino VARCHAR(64) NOT NULL REFERENCES CARTEIRA (endereco_carteira),
    id_moeda SMALLINT NOT NULL REFERENCES MOEDA (id_moeda),
    valor NUMERIC(18, 8) NOT NULL,
    taxa_valor NUMERIC(18, 8) NOT NULL,
    data_hora TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO MOEDA (codigo, nome, tipo) VALUES 
('BTC', 'Bitcoin', 'CRYPTO'),   
('ETH', 'Ethereum', 'CRYPTO'),   
('SOL', 'Solana', 'CRYPTO'),     
('USD', 'Dólar Americano', 'FIAT'), 
('BRL', 'Real (Brasil)', 'FIAT');