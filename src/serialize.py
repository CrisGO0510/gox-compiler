import json
from dataclasses import asdict
from typing import Any


def remove_none(d: Any) -> Any:
    """Elimina los atributos con valor None de un diccionario anidado."""
    if isinstance(d, dict):
        return {k: remove_none(v) for k, v in d.items() if v is not None}
    if isinstance(d, list):
        return [remove_none(v) for v in d]
    return d


def to_json(obj: Any, indent: int = 4) -> str:
    """Convierte un objeto de dataclass a JSON, eliminando valores None."""
    return json.dumps(remove_none(asdict(obj)), indent=indent)
