# Back to School Mock Integration API

FastAPI implementation of the three supplied Back to School dashboard payloads plus current-user and AI-chat integration endpoints.

## What is implemented

- B2S1 Service Assurance dashboard, preserving the supplied route and response envelope.
- B2S2 Complaint Intelligence dashboard, preserving the supplied route and response envelope.
- B2S3 Service Operations dashboard, preserving the supplied route and response envelope.
- Time-bucketed live mock snapshots with deterministic variation.
- Optional `source`, `normal`, `warning`, and `critical` scenarios.
- `GET /api/v1/users/me` for chatbot greeting/personalization.
- `POST /api/v1/chat` as an AI integration adapter/proxy.
- Request correlation via `X-Request-ID`.
- Pydantic response-envelope validation and contract tests.
- Swagger/OpenAPI, Postman collection/environment, Docker, health/readiness routes, and CI.

## Quick start

### Python

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements-dev.txt
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/macOS
uvicorn app.main:app --reload
```

Open:

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

### Docker

```bash
cp .env.example .env
docker compose up --build
```

## Dashboard endpoints

```text
GET /api/ExternalService/get_back_to_school_service_assurance_dashboard_payload
GET /api/ExternalService/get_back_to_school_complaint_intelligence_dashboard_payload
GET /api/ExternalService/get_back_to_school_service_operations_dashboard_payload
```

## User & Auth endpoints

```text
POST /api/v1/auth/login
Content-Type: application/json

{
  "username_or_email": "hazem.hossam",
  "password": "password123"
}
```

```text
GET /api/v1/users/me
Authorization: Bearer <token>
```


## Chat endpoint

```text
POST /api/v1/chat
Authorization: Bearer <token>
Content-Type: application/json

{
  "message": "What is the current network status?",
  "conversation_id": "conv-001"
}
```


The project runs with `MOCK_AI_ENABLED=true` by default. When the AI team's service is ready:

```env
MOCK_AI_ENABLED=false
AI_SERVICE_URL=http://ai-service:8080
AI_CHAT_PATH=/chat
```

## Live mock behavior

The mock service does not produce unrelated random values on every request. It generates one stable snapshot per refresh bucket (`MOCK_DATA_REFRESH_SECONDS`, default 60s), updates timestamps/dates, changes selected live metrics, and recalculates directly related values where safe.

See `docs/MOCK_DATA_RULES.md` for details.

## Tests

```bash
pytest
```

Contract tests compare the generated payload shape against the exact supplied source fixtures, including nested keys, list lengths, and JSON value types.

## Postman

Import:

- `postman/Back-to-School.postman_collection.json`
- `postman/Back-to-School-Local.postman_environment.json`

The environment defines `base_url=http://localhost:8000`.

## Important compatibility decision

The three source responses return `DataCount: 0` even though `Data.returned_data` is populated. This implementation preserves `DataCount: 0` instead of redefining its meaning.
