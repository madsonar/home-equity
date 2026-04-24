"""Indexa a knowledge_base local no ChromaDB + FAISS."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.ingestion.doc_parser import parse_directory
from app.rag.chroma_store import add_documents_to_chroma
from app.rag.faiss_store import add_documents_to_faiss
from app.rag.llama_rag import build_llama_index

kb_path = "./data/knowledge_base"
if not os.path.exists(kb_path):
    print(f"Knowledge base não encontrada em {kb_path}")
    sys.exit(1)

print(f"Indexando {kb_path}...")
docs = parse_directory(kb_path)

if not docs:
    print("Nenhum documento encontrado.")
    sys.exit(0)

add_documents_to_chroma(docs)
add_documents_to_faiss(docs)
build_llama_index([d.page_content for d in docs])

print(f"{len(docs)} chunks indexados em ChromaDB + FAISS + LlamaIndex")
