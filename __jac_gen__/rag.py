from __future__ import annotations
from jaclang import jac_import as __jac_import__
import typing as _jac_typ
from jaclang.plugin.feature import JacFeature as _Jac
from jaclang.plugin.builtin import *
from dataclasses import dataclass as __jac_dataclass__
if _jac_typ.TYPE_CHECKING:
    import os
else:
    os, = __jac_import__(target='os', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={})
if _jac_typ.TYPE_CHECKING:
    from langchain_community.document_loaders import PyPDFDirectoryLoader
else:
    PyPDFDirectoryLoader, = __jac_import__(target='langchain_community.document_loaders', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={'PyPDFDirectoryLoader': None})
if _jac_typ.TYPE_CHECKING:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
else:
    RecursiveCharacterTextSplitter, = __jac_import__(target='langchain_text_splitters', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={'RecursiveCharacterTextSplitter': None})
if _jac_typ.TYPE_CHECKING:
    from langchain.schema.document import Document
else:
    Document, = __jac_import__(target='langchain.schema.document', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={'Document': None})
if _jac_typ.TYPE_CHECKING:
    from langchain_community.embeddings.ollama import OllamaEmbeddings
else:
    OllamaEmbeddings, = __jac_import__(target='langchain_community.embeddings.ollama', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={'OllamaEmbeddings': None})
if _jac_typ.TYPE_CHECKING:
    from langchain_community.vectorstores.chroma import Chroma
else:
    Chroma, = __jac_import__(target='langchain_community.vectorstores.chroma', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={'Chroma': None})

@_Jac.make_obj(on_entry=[], on_exit=[])
@__jac_dataclass__(eq=False)
class RagEngine(_Jac.Obj):
    file_path: str = _Jac.has_instance_default(gen_func=lambda: 'docs')
    chroma_path: str = _Jac.has_instance_default(gen_func=lambda: 'chroma')

    def __post_init__(self) -> None:
        documents: list = self.load_documents()
        chunks: list = self.split_documents(documents)
        self.add_to_chroma(chunks)

    def load_documents(self) -> None:
        document_loader = PyPDFDirectoryLoader(self.file_path)
        return document_loader.load()

    def split_documents(self, documents: list[Document]) -> None:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80, length_function=len, is_separator_regex=False)
        return text_splitter.split_documents(documents)

    def get_embedding_function(self) -> None:
        embeddings = OllamaEmbeddings(model='nomic-embed-text')
        return embeddings

    def add_chunk_id(self, chunks: str) -> None:
        last_page_id = None
        current_chunk_index = 0
        for chunk in chunks:
            source = chunk.metadata.get('source')
            page = chunk.metadata.get('page')
            current_page_id = f'{source}:{page}'
            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0
            chunk_id = f'{current_page_id}:{current_chunk_index}'
            last_page_id = current_page_id
            chunk.metadata['id'] = chunk_id
        return chunks

    def add_to_chroma(self, chunks: list[Document]) -> None:
        db = Chroma(persist_directory=self.chroma_path, embedding_function=self.get_embedding_function())
        chunks_with_ids = self.add_chunk_id(chunks)
        existing_items = db.get(include=[])
        existing_ids = set(existing_items['ids'])
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata['id'] not in existing_ids:
                new_chunks.append(chunk)
        if len(new_chunks):
            print('adding new documents')
            new_chunk_ids = [chunk.metadata['id'] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
        else:
            print('no new documents to add')

    def get_from_chroma(self, query: str, chunck_nos: int=5) -> None:
        db = Chroma(persist_directory=self.chroma_path, embedding_function=self.get_embedding_function())
        results = db.similarity_search_with_score(query, k=chunck_nos)
        return results