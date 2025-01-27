from typing import Any, Dict, NamedTuple
from pathlib import Path


from empuje.database import DatabaseHandler

class CurrentEmpuje(NamedTuple):
    empuje: Dict[str, Any]
    error: int
    

class Empujer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)
