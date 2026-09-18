-- Habilita pgvector no banco da aplicação para uso futuro de embeddings em SQL.
-- O script roda apenas no primeiro boot do container (data dir vazio).
CREATE EXTENSION IF NOT EXISTS vector;
