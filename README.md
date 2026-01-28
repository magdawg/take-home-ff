# Portfolio Insights App

<img width="1499" height="658" alt="Screenshot 2026-01-28 at 15 09 03" src="https://github.com/user-attachments/assets/5db3f695-97b7-476d-a656-dcd97370a32d" />
<img width="1502" height="752" alt="Screenshot 2026-01-28 at 15 09 15" src="https://github.com/user-attachments/assets/37f813f3-e01c-4647-ae41-f8c4d3a918c9" />


## Setup and usage

### 1. Start Everything with Docker
Ensure Docker is running on your machine, then run:
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
This is a POC app

### Functional requirements
- assets information is stored in-memory and not perssited when the app shuts down
- the UI only displays the assets/insights information
- assets creation will not be supported in the UI for now
- defaulted asset is one who's due date has passed; active asset is one who's due date is in the future
- asset updates are idempotent (by ID)

### Non-functional requirements
- concurrency and scalability not an issue for POC
- pagination of endpoints not an issue for POC
- graceful error handling; failed API requests don't creash the application
- test coverage >80%
