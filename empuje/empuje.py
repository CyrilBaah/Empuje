from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from empuje import DB_READ_ERROR, ID_ERROR
from empuje.database import DatabaseHandler


class CurrentEmpuje(NamedTuple):
    empuje: Dict[str, Any]
    error: int


class Empujer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    # Add empuje
    def add(self, description: List[str], priority: int = 2) -> CurrentEmpuje:
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        empuje = {
            "Description": description_text,
            "Priority": priority,
            "Done": False,
        }
        read = self._db_handler.read_empuje()
        if read.error == DB_READ_ERROR:
            return CurrentEmpuje(empuje, read.error)
        read.empuje_list.append(empuje)
        write = self._db_handler.write_empuje(read.empuje_list)
        return CurrentEmpuje(empuje, write.error)

    # List all empuje
    def get_all_empuje(self) -> List[Dict[str, Any]]:
        read = self._db_handler.read_empuje()
        return read.empuje_list
    

