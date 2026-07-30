-- psql -U postgres -c "CREATE DATABASE \"sistema_gestao\";"
-- psql -U postgres -d "sistema_gestao" -f database.sql


CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE usuarios (
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

CREATE TABLE contas (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('CAIXA', 'CORRENTE', 'POUPANCA', 'CARTEIRA', 'INVESTIMENTO')),
    saldo_inicial NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    ativa BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contas_usuario_ativa ON contas(usuario_id, ativa);

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('RECEITA', 'DESPESA')),
    categoria_pai_id INT REFERENCES categorias(id) ON DELETE CASCADE,
    cor VARCHAR(7) NOT NULL DEFAULT '#FFFFFF',
    ativa BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_categorias_usuario ON categorias(usuario_id);

CREATE TABLE centros_custo (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE formas_pagamento (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

INSERT INTO formas_pagamento (nome) VALUES
    ('Dinheiro'),
    ('Cartão de Crédito'),
    ('Cartão de Débito'),
    ('PIX'),
    ('Boleto'),
    ('Transferência Bancária');

CREATE TABLE cartoes_credito (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    limite NUMERIC(12, 2) NOT NULL,
    dia_fechamento INT NOT NULL CHECK (dia_fechamento BETWEEN 1 AND 31),
    dia_vencimento INT NOT NULL CHECK (dia_vencimento BETWEEN 1 AND 31),
    conta_pagamento_id INT NOT NULL REFERENCES contas(id) ON DELETE CASCADE
);

CREATE TABLE movimentacoes (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    conta_id INT NOT NULL REFERENCES contas(id) ON DELETE RESTRICT,
    categoria_id INT NOT NULL REFERENCES categorias(id) ON DELETE RESTRICT,
    formas_pagamento_id INT REFERENCES formas_pagamento(id) ON DELETE SET NULL,
    centros_custo_id INT REFERENCES centros_custo(id) ON DELETE SET NULL,
    cartao_id INT REFERENCES cartoes_credito(id) ON DELETE SET NULL,

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

CREATE INDEX idx_mov_usuario_data ON movimentacoes(usuario_id, data_movimentacao);
CREATE INDEX idx_mov_usuario_status ON movimentacoes(usuario_id, status);
CREATE INDEX idx_mov_grupo_parcela ON movimentacoes(grupo_parcela);

CREATE TABLE transferencias (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    conta_origem_id INT NOT NULL REFERENCES contas(id) ON DELETE RESTRICT,
    conta_destino_id INT NOT NULL REFERENCES contas(id) ON DELETE RESTRICT,
    valor NUMERIC(12, 2) NOT NULL,
    data DATE NOT NULL,
    observacao TEXT,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE anexos_movimentacoes (
    id SERIAL PRIMARY KEY,
    movimentacao_id INT NOT NULL REFERENCES movimentacoes(id) ON DELETE CASCADE,
    arquivo VARCHAR(255) NOT NULL,
    enviado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
