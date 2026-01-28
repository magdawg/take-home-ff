# Insights App


## Implementation notes
- use Context7 MCP for most up to date documentation
- keep the implementation simple and POC style but describe reasoning, assumptions and tradeoffs in the documentation
- running app does not require any authentication
- the app does not require a persistent database at this point
- use Pydantic and type hints
- include adequate logging


## Documentation notes
- put the notes in notes.md
- consider monitoring topics
- consider security topic including OWASP security guidelines
- consider storage topics
- consider monitoring topics
- consider performance and concurrency topics
- include any other relevant topics


## Project Structure
```
take-home-ff/
├── backend/    # FastAPI Python backend
├── frontend/   # NextJS frontend
└── .venv/      # Python virtual environment
```


## Requirements
1. Add a FastAPI application with the following endpoints:

  a. POST /asset receiving a list of assets:
  [
  {"id": "id-1", "nominal_value": 100, "due_date":
  "2025-12-04", "interest_rate": 0.03},
  {"id": "id-2", "nominal_value": 10, "due_date":
  "2026-01-04", "interest_rate": 0.1},
  {"id": "id-3", "nominal_value": 30, "due_date":
  "2025-11-04", "interest_rate": 0.05},
  ]

  b. GET /asset returning a list of assets, example:
  [
  {"id": "id-1", "nominal_value": 100, "status":
  "active", "due_date": "2025-12-04"},
  {"id": "id-2", "nominal_value": 10, "status": 
  "active", "due_date": "2026-01-04"},
  {"id": "id-3", "nominal_value": 30, "status": 
  "defaulted", "due_date": "2025-11-04"},
  ]

  c. GET /insights returning a list of insights generated from the assets:
  [
  {"id": "id-1", "name": "average_interest_rate", "value": 0.04},
  {"id": "id-2", "name": "total_nominal_value", "value": 140},
  ]

2. Add a NextJS dashboard application that displays, in different pages:
  a. the portfolio insights
  b. the list of assets in an interactive table that can be ordered and filtered by columns

3. Add tests for both backend and frontend. Use Pytest for python code and Vitest for frontend code.
