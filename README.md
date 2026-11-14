# Schema Healer

Schema Healer is a Python text-to-SQL demo that uses Pydantic AI and SQLite to answer analytical questions. It routes requests, gives the SQL agent access to schema descriptions, checks generated SQL, and limits the agent to three execution attempts.

## Features

- Rewrites a request into a self-contained analytical question.
- Retrieves matching table descriptions from `schema_dict.json`.
- Uses SQLGlot AST parsing to detect repeated logical queries during a session.
- Checks SQLite query plans before execution and reports database errors to the agent.
- Stops after a fixed number of attempts.
- Reports a clear setup error when `OPENROUTER_API_KEY` is missing.

## Requirements

- Python 3.10 or newer.
- An OpenRouter API key for running the AI workflow.

## Setup

```bash
git clone https://github.com/diddibhavana/schema-healer.git
cd schema-healer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Set the key in the environment or create a `.env` file in the project root:

```dotenv
OPENROUTER_API_KEY=your-openrouter-api-key
```

Initialize the sample database and run the engine from the project root:

```bash
python setup_db.py
python -m src.engine
```

The demo prompt is defined in `src/engine.py`. To run the standard-library unit tests:

```bash
python -m unittest discover -s tests -v
```

## Example

The included prompt asks for total spending by user email ordered by account creation date. The sample schema has no account creation date, so the agent receives SQLite's error and can retry with an available query.

## Project structure

```text
.
├── schema_dict.json       # Searchable table and column descriptions
├── setup_db.py            # Creates the sample SQLite database
├── src/
│   ├── agents.py          # Context router and SQL agent setup
│   ├── engine.py          # Bounded session orchestration
│   ├── state.py           # Per-session state and project resource paths
│   └── tools.py           # Schema lookup and guarded SQL execution
└── tests/
    └── test_state.py      # Agent state tests
```

## Credits

This derivative is based on [schema-healer by Sainath Manda](https://github.com/sainathmanda7/schema-healer). The upstream repository and its author are credited here; its original history remains in the upstream Git history.

## License

This checkout contains no license file. Contact the original rights holder for permission before redistributing or publishing this derivative.
