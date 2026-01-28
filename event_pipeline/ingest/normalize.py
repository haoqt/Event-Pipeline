import re

ID_RE = re.compile(r"/\d+")

def normalize_endpoint(ep: str) -> str:
    return ID_RE.sub("/{id}", ep)