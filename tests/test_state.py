"""Tests for project resource paths and initial agent state."""

import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.state import AgentState, PROJECT_ROOT


class AgentStateTests(unittest.TestCase):
    def test_loads_schema_and_uses_project_database_path(self) -> None:
        original_directory = Path.cwd()
        with TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                state = AgentState()
            finally:
                os.chdir(original_directory)

        self.assertIn("enterprise_users", state.schema_registry)
        self.assertEqual(state.db_path, str(PROJECT_ROOT / "warehouse.db"))
        self.assertEqual(state.attempted_hashes, set())


if __name__ == "__main__":
    unittest.main()
