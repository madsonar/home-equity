from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Configuração central da aplicação.

    TODA configuração de runtime (modelos, endpoints, coleções, paths,
    backends) vem DAQUI — nunca hardcoded no código. Para trocar de
    provider de LLM/embedding/vector-store basta editar o `.env`.
    """

    # ── LLM Providers ────────────────────────────────────────────────────
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    google_api_key: str = Field(default="", alias="GOOGLE_API_KEY")
    deepseek_api_key: str = Field(default="", alias="DEEPSEEK_API_KEY")
    cohere_api_key: str = Field(default="", alias="COHERE_API_KEY")

    # provider e modelo ativos (chat/score)
    default_llm_provider: str = Field(default="google", alias="DEFAULT_LLM_PROVIDER")
    default_llm_model: str = Field(default="gemini-2.5-pro", alias="DEFAULT_LLM_MODEL")
    default_llm_temperature: float = Field(default=0.0, alias="DEFAULT_LLM_TEMPERATURE")

    # embeddings (pode ser outro provider do LLM)
    embedding_provider: str = Field(default="google", alias="EMBEDDING_PROVIDER")
    embedding_model: str = Field(default="models/text-embedding-004", alias="EMBEDDING_MODEL")
    local_embedding_model: str = Field(
        default="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        alias="LOCAL_EMBEDDING_MODEL",
    )

    # agente default ("langchain" | "agno")
    default_agent: str = Field(default="langchain", alias="DEFAULT_AGENT")

    # ── Vector Stores ────────────────────────────────────────────────────
    vector_store_backend: str = Field(default="chroma", alias="VECTOR_STORE_BACKEND")  # chroma|faiss
    chroma_host: str = Field(default="localhost", alias="CHROMA_HOST")
    chroma_port: int = Field(default=8001, alias="CHROMA_PORT")
    chroma_persist_path: str = Field(default="./data/chroma_db", alias="CHROMA_PERSIST_PATH")
    chroma_collection: str = Field(default="credit_knowledge_base", alias="CHROMA_COLLECTION")
    faiss_index_path: str = Field(default="./data/faiss_index", alias="FAISS_INDEX_PATH")
    llama_collection: str = Field(default="llama_credit_index", alias="LLAMA_COLLECTION")
    rag_top_k: int = Field(default=4, alias="RAG_TOP_K")

    # ── Memory / Sessions ────────────────────────────────────────────────
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    memory_collection_prefix: str = Field(default="memory_", alias="MEMORY_COLLECTION_PREFIX")
    short_term_memory_window: int = Field(default=10, alias="SHORT_TERM_MEMORY_WINDOW")

    # ── ML / Credit Scorer ───────────────────────────────────────────────
    credit_model_path: str = Field(default="./data/credit_model.pkl", alias="CREDIT_MODEL_PATH")

    # ── App ──────────────────────────────────────────────────────────────
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    knowledge_base_path: str = Field(default="./data/knowledge_base", alias="KNOWLEDGE_BASE_PATH")

    # ── Observability — OpenTelemetry + Langfuse ─────────────────────────
    otlp_endpoint: str = Field(default="", alias="OTLP_ENDPOINT")
    langfuse_public_key: str = Field(default="", alias="LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key: str = Field(default="", alias="LANGFUSE_SECRET_KEY")
    langfuse_host: str = Field(default="https://cloud.langfuse.com", alias="LANGFUSE_HOST")

    # ── WhatsApp / Twilio ────────────────────────────────────────────────
    twilio_account_sid: str = Field(default="", alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str = Field(default="", alias="TWILIO_AUTH_TOKEN")
    twilio_whatsapp_from: str = Field(default="", alias="TWILIO_WHATSAPP_FROM")

    # ── Snowflake ────────────────────────────────────────────────────────
    snowflake_account: str = Field(default="", alias="SNOWFLAKE_ACCOUNT")
    snowflake_user: str = Field(default="", alias="SNOWFLAKE_USER")
    snowflake_password: str = Field(default="", alias="SNOWFLAKE_PASSWORD")
    snowflake_warehouse: str = Field(default="", alias="SNOWFLAKE_WAREHOUSE")
    snowflake_database: str = Field(default="", alias="SNOWFLAKE_DATABASE")
    snowflake_schema: str = Field(default="PUBLIC", alias="SNOWFLAKE_SCHEMA")

    model_config = {"env_file": ".env", "populate_by_name": True, "extra": "ignore"}


settings = Settings()
