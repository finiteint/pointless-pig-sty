import bottle
import os
import sys
import re
import uuid
import os.path
from bottle import route, template, view, request

if sys.version_info.major == 2:
    from codecs import open

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_PATH, "data")


@route("/pig", method="GET")
def pig_redirect():
    bottle.redirect("/pig/")


@route("/pig/", method="GET")
@view("index")
def index():
    return {}


@route("/pig/new/", method="GET")
def pig_new_redirect():
    bottle.redirect("/pig/new")


@route("/pig/new", method="GET")
@route("/pig/<key:re:[0-9a-fA-F]{32}>/edit", method="GET")
@view("edit")
def edit_pig(key=None):
    doc = Document.get_or_new(key)
    return {"key": doc.key, "name": doc.name, "data": doc.data}


@route("/pig/<key:re:[0-9a-fA-F]{32}>/update", method="POST")
@view("update")
def update_pig(key):
    doc = Document.get_or_new(key)
    doc.name = request.forms.get("name")
    doc.data = request.forms.get("data")
    doc.save()
    return {"key": doc.key, "name": doc.name}


class Document:
    @classmethod
    def get_or_new(cls, key):
        doc = cls.load(key)
        return doc if doc else cls.new()

    @classmethod
    def new(cls):
        return cls(new_doc_key(), data="")

    @classmethod
    def load(cls, key):
        key = validated_document_key(key)
        if not key:
            return None

        try:
            name_path = os.path.join(DATA_DIR, key + ".name.txt")
            with open(name_path, "rt", encoding="utf-8") as file:
                name = file.read()
        except FileNotFoundError:
            name = "Unnamed Pig"

        try:
            data_path = os.path.join(DATA_DIR, key + ".data.txt")
            with open(data_path, "rt", encoding="utf-8") as file:
                data = file.read()

            return cls(key, name=name, data=data)
        except FileNotFoundError:
            return None

    def __init__(self, key, name="Unnamed Pig", data=""):
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

    def save(self):
        key = self.key
        name_path = os.path.join(DATA_DIR, key + ".name.txt")
        with open(name_path, "wt", encoding="utf-8") as file:
            file.write(self.name)

        data_path = os.path.join(DATA_DIR, key + ".data.txt")
        with open(data_path, "wt", encoding="utf-8") as file:
            file.write(self.data)

        return True


def validated_document_key(key):
    key = (key or "").lower().replace("-", "").strip()[:32]
    return key if re.search(r"^[0-9a-f]{32}$", key) else None


def new_doc_key():
    return uuid.uuid4().hex.lower()


def normalize_name(name):
    return re.sub(r"\s+", " ", name or "").strip()[:96] or "Unnamed Pig"


def normalize_data(data):
    return data or ""


def main():
    host, port, debug = parse_args()
    print("Running on http://" + host + ":" + str(port) + "/pig/")
    bottle.run(host=host, port=port, debug=debug)


def parse_args():
    import argparse

    p = argparse.ArgumentParser(description="pig-server")
    p.add_argument(
        "--debug", help="start in debug mode", action="store_true", default=False
    )
    p.add_argument(
        "--port", help="The port to run on (default: 7781)", type=int, default=7781
    )
    p.add_argument(
        "--host",
        help="The host/interface (IP or hostname) to bind (default: localhost)",
        default="localhost",
    )
    args = p.parse_args()
    return args.host, args.port, args.debug


if __name__ == "__main__":
    main()

