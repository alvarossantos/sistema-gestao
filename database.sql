-- psql -U postgres -c "CREATE DATABASE \"sistema_gestao\";"
-- psql -U postgres -d "sistema_gestao" -f database.sql


CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    primeiro_nome VARCHAR(150) NOT NULL,
    ultimo_nome VARCHAR(150) NOT NULL,
    foto TEXT DEFAULT '/img/usuarios/default.png',
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    ultimo_login TIMESTAMP WITH TIME ZONE,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conta (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('CAIXA', 'CORRENTE', 'POUPANCA', 'CARTEIRA', 'INVESTIMENTO')),
    saldo_inicial NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    ativa BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_conta_usuario_ativa ON conta(usuario_id, ativa);

CREATE TABLE categoria (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('RECEITA', 'DESPESA')),
    categoria_pai_id INT REFERENCES categoria(id) ON DELETE CASCADE,
    cor VARCHAR(7) NOT NULL DEFAULT '#FFFFFF',
    ativa BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_categoria_usuario ON categoria(usuario_id);

CREATE TABLE centro_custo (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE forma_pagamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

INSERT INTO forma_pagamento (nome) VALUES
    ('Dinheiro'),
    ('Cartão de Crédito'),
    ('Cartão de Débito'),
    ('PIX'),
    ('Boleto'),
    ('Transferência Bancária');

CREATE TABLE cartao_credito (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    limite NUMERIC(12, 2) NOT NULL,
    dia_fechamento INT NOT NULL CHECK (dia_fechamento BETWEEN 1 AND 31),
    dia_vencimento INT NOT NULL CHECK (dia_vencimento BETWEEN 1 AND 31),
    conta_pagamento_id INT NOT NULL REFERENCES conta(id) ON DELETE CASCADE
);

CREATE TABLE movimentacao (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    conta_id INT NOT NULL REFERENCES conta(id) ON DELETE RESTRICT,
    categoria_id INT NOT NULL REFERENCES categoria(id) ON DELETE RESTRICT,
    forma_pagamento_id INT REFERENCES forma_pagamento(id) ON DELETE SET NULL,
    centro_custo_id INT REFERENCES centro_custo(id) ON DELETE SET NULL,
    cartao_id INT REFERENCES cartao_credito(id) ON DELETE SET NULL,

    descricao VARCHAR(255) NOT NULL,
    valor NUMERIC(12, 2) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('RECEITA', 'DESPESA')),
    status VARCHAR(15) NOT NULL DEFAULT 'PENDENTE' CHECK (status IN ('PENDENTE', 'PAGO', 'CANCELADO')),

    data_movimentacao DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    data_pagamento DATE,

    grupo_parcela UUID,
    numero_parcela INT,
    total_parcelas INT,

    observacao TEXT,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_mov_usuario_data ON movimentacao(usuario_id, data_movimentacao);
CREATE INDEX idx_mov_usuario_status ON movimentacao(usuario_id, status);
CREATE INDEX idx_mov_grupo_parcela ON movimentacao(grupo_parcela);

CREATE TABLE transferencia (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuario(id) ON DELETE CASCADE,
    conta_origem_id INT NOT NULL REFERENCES conta(id) ON DELETE RESTRICT,
    conta_destino_id INT NOT NULL REFERENCES conta(id) ON DELETE RESTRICT,
    valor NUMERIC(12, 2) NOT NULL,
    data DATE NOT NULL,
    observacao TEXT,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE anexo_movimentacao (
    id SERIAL PRIMARY KEY,
    movimentacao_id INT NOT NULL REFERENCES movimentacao(id) ON DELETE CASCADE,
    arquivo VARCHAR(255) NOT NULL,
    enviado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
