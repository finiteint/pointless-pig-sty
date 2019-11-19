import bottle
import os
import sys
import re
import random
import uuid
from pathlib import Path
from typing import Optional
from bottle import route, view, request
from document import DocumentManager, DocumentStore


BASE_PATH = Path(__file__).parent.resolve()


doc_mgr = DocumentManager(doc_store=DocumentStore(base_path=BASE_PATH / "data"))


@route("/pig", method="GET")
def pig_redirect():
    bottle.redirect("/pig/")


@route("/pig/", method="GET")
@view("index")
def index():
    keys = doc_mgr.keys()
    random_pigs = set(random.choice(keys) for _ in range(10))
    return {"random_pigs": random_pigs}


@route("/pig/new/", method="GET")
def pig_new_redirect():
    bottle.redirect("/pig/new")


@route("/pig/new", method="GET")
@route("/pig/<key:re:[0-9a-fA-F]{32}>/edit", method="GET")
@view("edit")
def edit_pig(key: Optional[str] = None):
    doc = doc_mgr.get_or_new(key)
    return {"key": doc.key, "name": doc.name, "data": doc.data}


@route("/pig/<key:re:[0-9a-fA-F]{32}>/update", method="POST")
@view("update")
def update_pig(key: str):
    doc = doc_mgr.get_or_new(key)
    doc.name = request.forms.get("name")
    doc.data = request.forms.get("data")
    if doc_mgr.store(doc):
        return {"key": doc.key, "name": doc.name}
    else:
        return {"key": doc.key, "name": doc.name, "err": "Failed to store document."}


def main():
    host, port, debug = parse_args()
    doc_mgr.inititalize()
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

