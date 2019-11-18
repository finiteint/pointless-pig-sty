import os.path
import re
import os
import uuid

MAX_KEY_LEN = 32
MAX_NAME_LEN = 64


class Document:
    def __init__(self, key, name=None, data=None):
        self._key = key
        self._name = normalize_name(name)
        self._data = normalize_data(data)

    def __repr__(self):
        return "Document(key=" + repr(self.key) + ", data=" + repr(self.data) + ")"

    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = normalize_name(name)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = normalize_data(data)


class DocumentStore:
    def __init__(self, base_path):
        self.base_path = base_path

    def inititalize(self):
        os.makedirs(self.base_path, exist_ok=True)

    def keys(self):
        return [
            name[: -len(".name.txt")].lower()
            for name in os.listdir(self.base_path)
            if name.endswith(".name.txt")
        ]

    def load(self, key):
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

    def store(self, document):
        key = document.key
        name_path = os.path.join(self.base_path, key + ".name.txt")
        with open(name_path, "wt", encoding="utf-8") as file:
            file.write(document.name)

        data_path = os.path.join(self.base_path, key + ".data.txt")
        with open(data_path, "wt", encoding="utf-8") as file:
            file.write(document.data)

        return True


class DocumentManager:
    def __init__(self, doc_store):
        self.doc_store = doc_store

    def inititalize(self):
        self.doc_store.inititalize()

    def get_or_new(self, key):
        doc = self.load(key)
        return doc if doc else self.new()

    def new(self):
        return Document(new_doc_key())

    def load(self, key):
        key = validated_document_key(key)
        if not key:
            return None

        return self.doc_store.load(key)

    def store(self, document):
        self.doc_store.store(document)

    def keys(self):
        return self.doc_store.keys()


def validated_document_key(key):
    key = (key or "").lower().replace("-", "").strip()[:MAX_KEY_LEN]
    return key if re.search(r"^[0-9a-f]{32}$", key) else None


def new_doc_key():
    return uuid.uuid4().hex.lower()


def normalize_name(name):
    return (
        re.sub(r"\s+", " ", name or "").strip()[:MAX_NAME_LEN].strip() or "Unnamed Pig"
    )


def normalize_data(data):
    return data or ""
