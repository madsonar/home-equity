import os
import tempfile
from typing import List
from pathlib import Path

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from loguru import logger

from app.domain.knowledge.entities import KnowledgeChunk
from app.domain.knowledge.ports import IDocumentParser


def _get_docling():
    try:
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        return DocumentConverter, PdfFormatOption, PdfPipelineOptions
    except ImportError as e:
        raise ImportError("docling não instalado. Execute: pip install docling") from e


def _get_converter():
    DocumentConverter, PdfFormatOption, PdfPipelineOptions = _get_docling()
    pipeline_opts = PdfPipelineOptions(do_ocr=False, do_table_structure=True)
    return DocumentConverter(format_options={"pdf": PdfFormatOption(pipeline_options=pipeline_opts)})


def _pdf_to_text_pypdf(content_or_path) -> str:
    """Fallback simples usando pypdfium2 — evita modelos de layout do docling."""
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(content_or_path)
    try:
        return "\n\n".join(page.get_textpage().get_text_range() for page in pdf)
    finally:
        pdf.close()


def _markdown_to_chunks(
    markdown: str,
    source: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> List[KnowledgeChunk]:
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")]
    )
    char_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    header_splits = header_splitter.split_text(markdown)
    chunks = char_splitter.split_documents(header_splits)
    return [
        KnowledgeChunk(content=c.page_content, source=source,
                       metadata={**c.metadata, "type": "document"})
        for c in chunks
    ]


class DoclingParser(IDocumentParser):
    def parse_bytes(self, content: bytes, filename: str) -> List[KnowledgeChunk]:
        suffix = Path(filename).suffix.lower()
        if suffix in {".txt", ".md"}:
            text = content.decode("utf-8", errors="replace")
            return _markdown_to_chunks(text, source=filename)
        with tempfile.NamedTemporaryFile(suffix=suffix or ".pdf", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            try:
                converter = _get_converter()
                result = converter.convert(tmp_path)
                markdown = result.document.export_to_markdown()
            except Exception as e:
                if suffix == ".pdf":
                    logger.warning(f"Docling falhou ({e.__class__.__name__}); usando pypdf como fallback")
                    markdown = _pdf_to_text_pypdf(tmp_path)
                else:
                    raise
            return _markdown_to_chunks(markdown, source=filename)
        finally:
            os.unlink(tmp_path)

    def parse_directory(self, path: str) -> List[KnowledgeChunk]:
        chunks = []
        supported = {".pdf", ".docx", ".pptx", ".html", ".txt", ".md"}
        for file_path in Path(path).rglob("*"):
            if file_path.suffix.lower() not in supported:
                continue
            if file_path.suffix.lower() in {".txt", ".md"}:
                try:
                    text = file_path.read_text(encoding="utf-8")
                    file_chunks = _markdown_to_chunks(text, source=str(file_path))
                    chunks.extend(file_chunks)
                    logger.info(f"Lido {file_path.name}: {len(file_chunks)} chunks")
                except Exception as e:
                    logger.error(f"Erro ao ler {file_path}: {e}")
                continue
            try:
                converter = _get_converter()
                result = converter.convert(str(file_path))
                file_chunks = _markdown_to_chunks(result.document.export_to_markdown(), source=str(file_path))
                chunks.extend(file_chunks)
                logger.info(f"Parsed {file_path.name}: {len(file_chunks)} chunks")
            except ImportError:
                logger.warning(f"Docling não instalado — pulando {file_path.name}")
            except Exception as e:
                logger.error(f"Erro ao parsear {file_path}: {e}")
        return chunks
