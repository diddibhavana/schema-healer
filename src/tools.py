"""Schema lookup and guarded SQL execution tools for the SQL agent."""

import sqlite3
from contextlib import closing
import sqlglot
from sqlglot.errors import ParseError
from pydantic_ai import RunContext
from src.state import AgentState
from src.agents import sql_agent

@sql_agent.tool
def search_schema(ctx: RunContext[AgentState], keywords: str) -> str:
    """Mock RAG: Returns only table schemas matching the keywords."""
    terms = keywords.split()
    results = {
        name: description
        for name, description in ctx.deps.schema_registry.items()
        if any(term.lower() in description.lower() for term in terms)
    }
    return str(results) if results else "No matching tables found. Broaden search."

@sql_agent.tool
def safe_execute_sql(ctx: RunContext[AgentState], query: str) -> str:
    """Safely executes SQL with AST Hashing and EXPLAIN cost checks."""
    print(f"\n[Engine] Intercepting Query: {query}")
    
    try:
        ast_hash = hash(sqlglot.parse_one(query).sql())
        if ast_hash in ctx.deps.attempted_hashes:
            return "SYSTEM REJECTION: You already tried this exact logical query. Change your JOINs or filtering strategy."
        ctx.deps.attempted_hashes.add(ast_hash)
    except ParseError:
        return "SYSTEM REJECTION: Invalid SQL syntax."

    try:
        with closing(sqlite3.connect(ctx.deps.db_path)) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(f"EXPLAIN QUERY PLAN {query}")
                plan = str(cursor.fetchall())
                if "SCAN TABLE enterprise_users" in plan:
                    return (
                        "SYSTEM REJECTION: Query requires a full table scan on "
                        "enterprise_users. Add a LIMIT or indexed WHERE clause."
                    )
            except sqlite3.Error:
                # Preserve execution behavior when SQLite cannot explain a query.
                pass

            cursor.execute(query)
            results = cursor.fetchall()
        print(f"[Engine] Success: {results}")
        return str(results)
    except sqlite3.Error as error:
        error_msg = f"DATABASE ERROR: {error}"
        print(f"[Engine] {error_msg}")
        return error_msg
