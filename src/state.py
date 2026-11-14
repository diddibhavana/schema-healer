import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

class AgentState:
    """Runtime state shared by the SQL agent and its defensive tools."""

    def __init__(self) -> None:
        self.db_path = str(PROJECT_ROOT / "warehouse.db")
        self.attempted_hashes: set[int] = set()
        schema_path = PROJECT_ROOT / "schema_dict.json"
        with schema_path.open(encoding="utf-8") as schema_file:
            self.schema_registry: dict[str, str] = json.load(schema_file)
