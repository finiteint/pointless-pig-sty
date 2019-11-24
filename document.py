import os.path
import re
import os
import uuid
from pathlib import Path
from typing import Optional, List

MAX_KEY_LEN: int = 32
MAX_NAME_LEN: int = 64


class Document:
    def __init__(
        self, key: str, name: Optional[str] = None, data: Optional[str] = None
    ):
        self._key = key
        self._name = normalize_name(name)
        self._data = normalize_data(data)

    def __repr__(self) -> str:
        return "Document(key=" + repr(self.key) + ", data=" + repr(self.data) + ")"

    @property
    def key(self) -> str:
        return self._key

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: Optional[str]):
        self._name = normalize_name(name)

    @property
    def data(self) -> str:
        return self._data

    @data.setter
    def data(self, data: Optional[str]):
        self._data = normalize_data(data)


class DocumentStore:
    def __init__(self, base_path: Path):
        self.base_path = base_path

    def inititalize(self):
        self.base_path.mkdir(parents=True, exist_ok=True)

    def keys(self) -> List[str]:
        return [
            path.name[: -len(".name.txt")].lower()
            for path in self.base_path.iterdir()
            if path.name.endswith(".name.txt")
        ]

    def load(self, key: str) -> Optional[Document]:
        try:
            name_path = os.path.join(self.base_path, key + ".name.txt")
            with open(name_path, "rt", encoding="utf-8") as file:
                name = file.read()
        except FileNotFoundError:
            name = None

        try:
            data_path = os.path.join(self.base_path, key + ".data.txt")
            with open(data_path, "rt", encoding="utf-8") as file:
                data = file.read()

            return Document(key, name=name, data=data)
        except FileNotFoundError:
            return None

    def store(self, document: Document) -> bool:
        key = document.key
        name_path = os.path.join(self.base_path, key + ".name.txt")
        with open(name_path, "wt", encoding="utf-8") as file:
            file.write(document.name)

        data_path = os.path.join(self.base_path, key + ".data.txt")
        with open(data_path, "wt", encoding="utf-8") as file:
            file.write(document.data)

        return True


class DocumentManager:
    def __init__(self, doc_store: DocumentStore):
        self.doc_store = doc_store

    def inititalize(self):
        self.doc_store.inititalize()

    def get_or_new(self, key: Optional[str]) -> Document:
        doc = self.load(key)
        return doc if doc else self.new()

    def new(self) -> Document:
        key = uuid.uuid4().hex.lower()
        return Document(key)

    def load(self, key: Optional[str]) -> Optional[Document]:
        key = validated_document_key(key)
        if not key:
            return None

        return self.doc_store.load(key)

    def store(self, document: Document):
        self.doc_store.store(document)

    def keys(self) -> List[str]:
        return self.doc_store.keys()


def validated_document_key(key: Optional[str]) -> Optional[str]:
    key = (key or "").lower().replace("-", "").strip()[:MAX_KEY_LEN]
    return key if re.search(r"^[0-9a-f]{32}$", key) else None





def normalize_name(name: Optional[str]) -> str:
    return (
        re.sub(r"\s+", " ", name or "").strip()[:MAX_NAME_LEN].strip() or "Unnamed Pig"
    )


def normalize_data(data: Optional[str]) -> str:
    return data or ""
