from typing import Any
from tabulate import tabulate

def model_to_dict(instance) -> dict[str, str]:
    return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}

def tabulate_db_objects(db_objects: list[Any]) -> str: 
    if len(db_objects) == 0:
        return ""

    rows = [model_to_dict(obj) for obj in db_objects]
    return tabulate(rows, headers="keys")

