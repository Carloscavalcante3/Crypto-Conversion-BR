CREATE TABLE CARTEIRA (
    -- Endereço público (Chave Primária) [cite: 10, 110]
    endereco_carteira VARCHAR(64) PRIMARY KEY, 
    
    -- Hash SHA-256 da chave privada (NUNCA a chave em texto puro) [cite: 13, 107, 111]
    hash_chave_privada VARCHAR(64) NOT NULL,
    
    -- Data de criação [cite: 16, 112]
    data_criacao TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Status (ATIVA ou BLOQUEADA) [cite: 19, 113]
    status VARCHAR(10) NOT NULL DEFAULT 'ATIVA' 
);

CREATE TABLE MOEDA (
    -- Chave Primária
    id_moeda SMALLSERIAL PRIMARY KEY, 
    
    -- Código (BTC, USD, BRL)
    codigo VARCHAR(10) UNIQUE NOT NULL, 
    
    -- Nome Completo (Bitcoin, Dólar Americano)
    nome VARCHAR(50) NOT NULL,
    
    -- Tipo (CRYPTO ou FIAT) [cite: 122]
    tipo VARCHAR(10) NOT NULL
);


CREATE TABLE SALDO_CARTEIRA (
    -- Chave Estrangeira para CARTEIRA [cite: 40, 42]
    endereco_carteira VARCHAR(64) NOT NULL REFERENCES CARTEIRA (endereco_carteira),
    
    -- Chave Estrangeira para MOEDA [cite: 46, 50]
    id_moeda SMALLINT NOT NULL REFERENCES MOEDA (id_moeda),
    
    -- Saldo atual (DECIMAL com boa precisão) [cite: 62]
    saldo NUMERIC(18, 8) NOT NULL DEFAULT 0.00000000,
    
    -- Data da última atualização
    data_atualizacao TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Chave Primária Composta (Uma carteira, uma moeda, um saldo) [cite: 40, 46]
    PRIMARY KEY (endereco_carteira, id_moeda)
);