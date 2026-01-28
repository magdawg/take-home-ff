# Portfolio Insights App


## Setup and usage

### 1. Start Everything with Docker
Ensure Docker is running on your machine, then run from the top level directory of the project:
```bash
make build
make up
```
Note: The build step can take up to a few of minutes when ran for the first time.

### 2. Use curl to add assets via the API 
```bash
curl -X POST http://localhost:8000/asset \
  -H "Content-Type: application/json" \
  -d '[
    {
      "id": "asset-1",
      "nominal_value": 100,
      "due_date": "2025-12-31",
      "interest_rate": 0.03
    },
    {
      "id": "asset-2",
      "nominal_value": 50,
      "due_date": "2026-06-15",
      "interest_rate": 0.05
    },
    {
      "id": "asset-4",
      "nominal_value": 200,
      "due_date": "2024-06-01",
      "interest_rate": 0.04
    }
  ]'
```

```bash
curl -X POST http://localhost:8000/asset \
  -H "Content-Type: application/json" \
  -d '[
    {
      "id": "asset-4",
      "nominal_value": 33,
      "due_date": "2025-12-31",
      "interest_rate": 0.07
    },
    {
      "id": "asset-5",
      "nominal_value": 43,
      "due_date": "2026-06-15",
      "interest_rate": 0.1
    }
  ]'
```

### 3. View the App
Open http://localhost:3000 in your browser to see the app


### 4. Run tests
```bash
make test
```

### 5. Stop Everything
```bash
make down
```

---

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **API**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **Health Check**: http://localhost:8000/health

---

## Reasoning and assumptions
This is a POC app. Prefer simplicity and document production requirements.

### Functional requirements/assumptions
- the UI only displays the assets/insights information; allow sorting and filtering
- pagination not supported in POC
- assets creation will not be supported in the UI for now
- defaulted asset is one who's due date has passed; active asset is one who's due date is in the future
- asset updates are idempotent (by ID)
- enforce data validation for creating new assets

### Non-functional requirements/assumptions
- assets information is stored in-memory and not persisted when the app shuts down
- authentication and security is not being considered for POC
- concurrency and scalability not an issue for POC
- pagination of GET /asset not an issue for POC
- graceful error handling; failed API requests don't crash the application
- adequate logging for debugging
- test coverage >80%


## Tradeoffs
1. **In-Memory Storage vs. Persistence**
   - Chosen: In-memory (faster, simpler for POC)
   - Future: Add PostgreSQL with connection pooling

2. **Client-Side Sorting vs. Server-Side**
   - Chosen: Client-side (faster, no API overhead)
   - Limit: < 10k rows before noticeable lag
   - Future: Server-side with database indexes for > 100k rows

3. **No Caching vs. Redis Cache**
   - Chosen: No caching (simpler)
   - Recalculates insights on every GET
   - Future: Cache insights (5-10 min TTL) for better performance

4. **CSR vs. SSR**
  - Chosen: CSR (simpler)
  - No SEO reqs; better interaction
  - Future: Stick to CSR or consider a hybrid approach if functionality eveloves

5. **Local Component State vs. Global State Management**
  - Chosen: Local State (simpler)
  - Current functionality does not require global state; too much boilerplate and complexity to involve Redux
  - Future: Consider Redux if complexity of the product increases


## Production readiness
- add authentication (JWT/OAuth2)
- add autorization (role-based access control)
- enable HTTPS/TLS
- add rate limiting per IP/User
- restrict CORS to frontend domain
- implement request logging and monitoring
- use structured logs
- add API versioning for backward compatibility
- add pagination to GET /asset endpoint
- consider POST for creation and PUT for updates of assets
- consider plural `assets` for GET and POST endpoints to follow REST conventions
- add database for data persistence (e.g. Postgres)
- add appropriate indexes for DB query performance
- add caching (Redis) for fast load of insights
- add E2E tests
- perform load testing
- improve UI design


## AI Usage
Including .github/copilot-instructions.md that shows how I utilised agentic workflow while working on this project
