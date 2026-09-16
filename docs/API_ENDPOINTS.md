# Back to School Mock API Endpoint Documentation

## Overview

- **Base URL:** `http://localhost:8000`
- **OpenAPI:** `GET /openapi.json`
- **Swagger UI:** `GET /docs`
- **ReDoc:** `GET /redoc`
- **Authentication:** None in the mock implementation.
- **Content type:** JSON responses use `Content-Type: application/json`.
- **Correlation:** Every request may include `X-Request-ID`. The API echoes the supplied value or generates a UUID and returns it in the response header.

All endpoints have no path parameters or query parameters unless stated otherwise.

## Common Headers

### Request headers

| Header | Required | Description |
|---|---:|---|
| `X-Request-ID` | No | Caller-supplied correlation ID. A UUID is generated when omitted. |
| `Content-Type` | POST only | Must be `application/json` for requests with a JSON body. |

### Response headers

| Header | Description |
|---|---|
| `Content-Type` | `application/json` for JSON responses. |
| `X-Request-ID` | Correlation ID associated with the request. |

## Endpoint Summary

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness probe. |
| `GET` | `/ready` | Readiness probe. |
| `GET` | `/api/v1/users/me` | Return the current mock user. |
| `GET` | `/api/ExternalService/get_back_to_school_service_assurance_dashboard_payload` | B2S1 service assurance dashboard. |
| `GET` | `/api/ExternalService/get_back_to_school_complaint_intelligence_dashboard_payload` | B2S2 complaint intelligence dashboard. |
| `GET` | `/api/ExternalService/get_back_to_school_service_operations_dashboard_payload` | B2S3 service operations dashboard. |
| `GET` | `/api/ExternalService/get_back_to_school_ftth_maturity_index_dashboard_payload` | B2S4 FTTH maturity index dashboard. |
| `POST` | `/api/v1/chat` | Send a message through the AI integration boundary. |

---

## 1. Health

### `GET /health`

Liveness probe used to confirm that the application process is responding.

**Parameters:** None

**Example request:**

```bash
curl -i \
  -H "X-Request-ID: health-check-001" \
  http://localhost:8000/health
```

**Success response: `200 OK`**

```json
{
  "status": "healthy"
}
```

---

## 2. Readiness

### `GET /ready`

Readiness probe used to confirm that the application is ready to serve requests.

**Parameters:** None

**Example request:**

```bash
curl -i \
  -H "X-Request-ID: readiness-check-001" \
  http://localhost:8000/ready
```

**Success response: `200 OK`**

```json
{
  "status": "ready"
}
```

---

## 3. Current User

### `GET /api/v1/users/me`

Returns the current mock user for chatbot greeting and personalization. Authentication is not implemented; the response is currently sourced from mock data.

**Parameters:** None

**Example request:**

```bash
curl -i \
  -H "X-Request-ID: user-request-001" \
  http://localhost:8000/api/v1/users/me
```

**Success response: `200 OK`**

| Field | Type | Description |
|---|---|---|
| `id` | string | User identifier. |
| `username` | string | User login name. |
| `first_name` | string | User's first name. |
| `last_name` | string | User's last name. |
| `display_name` | string | Display-ready full name. |
| `email` | string | Valid email address. |
| `role` | string | User role. |
| `preferred_language` | string | Preferred language; defaults to `en`. |

```json
{
  "id": "USR-001",
  "username": "hazem.hossam",
  "first_name": "Hazem",
  "last_name": "Hossam",
  "display_name": "Hazem Hossam",
  "email": "hazem.hossam@example.com",
  "role": "Network Operations",
  "preferred_language": "en"
}
```

---

## 4. Dashboard APIs

The three dashboard endpoints preserve the supplied legacy URLs and response envelope. They accept no request body, query parameters, or path parameters.

### Common dashboard request

```bash
curl -i \
  -H "X-Request-ID: dashboard-request-001" \
  http://localhost:8000/api/ExternalService/{dashboard-endpoint}
```

### Common success response: `200 OK`

```json
{
  "StatusCode": 200,
  "Messages": null,
  "Data": {
    "returned_data": {
      "meta": {
        "commands": [],
        "timezone": "Asia/Riyadh",
        "data_as_of": "2026-09-15T15:00:00+03:00",
        "special_day": {
          "events": [],
          "is_special_day": false
        },
        "generated_at": "2026-09-15T15:00:00+03:00",
        "configuration": {},
        "applied_filters": {},
        "payload_version": "0.6.0-draft"
      },
      "sections": []
    }
  },
  "DataCount": 0
}
```

### Dashboard response fields

| Field | Type | Description |
|---|---|---|
| `StatusCode` | integer | Legacy application status value. Successful responses use `200`. |
| `Messages` | any or null | Legacy message field; normally `null` for successful responses. |
| `Data.returned_data.meta.commands` | array | Dashboard commands. Each command has `order`, `title`, `subtitle`, and `command_id`. |
| `Data.returned_data.meta.timezone` | string | Timezone used by the dashboard data. |
| `Data.returned_data.meta.data_as_of` | string | ISO 8601 timestamp describing data freshness. |
| `Data.returned_data.meta.special_day` | object | Contains `events` and `is_special_day`. |
| `Data.returned_data.meta.generated_at` | string | ISO 8601 timestamp when the snapshot was generated. |
| `Data.returned_data.meta.configuration` | object | Dashboard-specific configuration and thresholds. |
| `Data.returned_data.meta.applied_filters` | object | Filters applied to the response. |
| `Data.returned_data.meta.payload_version` | string | Version of the dashboard payload contract. |
| `Data.returned_data.sections` | array | Dashboard-specific sections containing cards, KPIs, tables, or other supplied structures. |
| `DataCount` | integer | Preserved legacy value. It may be `0` even when `sections` contains populated data. Do not use it as a presence check. |

### 4.1 B2S1 Service Assurance

#### `GET /api/ExternalService/get_back_to_school_service_assurance_dashboard_payload`

Returns network health, readiness, and digital service exposure data.

```bash
curl -i \
  -H "X-Request-ID: b2s1-request-001" \
  http://localhost:8000/api/ExternalService/get_back_to_school_service_assurance_dashboard_payload
```

The response uses the common dashboard envelope. Its payload version and `sections` content are dashboard-specific and may change within the documented contract shape as the controlled mock snapshot refreshes.

### 4.2 B2S2 Complaint Intelligence

#### `GET /api/ExternalService/get_back_to_school_complaint_intelligence_dashboard_payload`

Returns customer impact, complaint trends, experience health, and operational response data.

```bash
curl -i \
  -H "X-Request-ID: b2s2-request-001" \
  http://localhost:8000/api/ExternalService/get_back_to_school_complaint_intelligence_dashboard_payload
```

The response uses the common dashboard envelope. Its payload version and `sections` content are dashboard-specific.

### 4.3 B2S3 Service Operations

#### `GET /api/ExternalService/get_back_to_school_service_operations_dashboard_payload`

Returns live workload, ownership, ticket execution, and resolution-control data.

```bash
curl -i \
  -H "X-Request-ID: b2s3-request-001" \
  http://localhost:8000/api/ExternalService/get_back_to_school_service_operations_dashboard_payload
```

The response uses the common dashboard envelope. Its payload version and `sections` content are dashboard-specific.

### 4.4 B2S4 FTTH Maturity Index

#### `GET /api/ExternalService/get_back_to_school_ftth_maturity_index_dashboard_payload`

Returns FTTH network maturity data: regional alarm/service index averages, overall index breakdowns, worst-performing FDT rankings, daily index trends, alarm trends, a district-level map summary, and a per-FDT detail table.

**Parameters:** None

```bash
curl -i \
  -H "X-Request-ID: b2s4-request-001" \
  http://localhost:8000/api/ExternalService/get_back_to_school_ftth_maturity_index_dashboard_payload
```

Unlike the other three dashboards, this endpoint does **not** use the common `StatusCode` / `Data.returned_data` / `sections` envelope. The supplied source payload is a flat object of named report blocks, and the response mirrors that shape as-is.

**Success response: `200 OK`**

| Field | Type | Description |
|---|---|---|
| `FDT Alarm Index Avg` | object | Regional average alarm index for FDTs, with a `Data` array of `{region, avg_pi}`. |
| `TB Alarm Index Avg` | object | Regional average alarm index for terminal boxes, with a `Data` array of `{region, avg_pi}`. |
| `Customer Alarm Index Avg` | object | Regional average alarm index for customers, with a `Data` array of `{region, avg_pi}`. |
| `Service Index Average` | object | Overall service index average, `{average}`. |
| `FDT Overall Service Index` | array | Breakdown of FDTs by `Optimal` / `Good` / `Bad` service index percentage. |
| `Alarm Index Average` | object | Overall alarm index average, `{average}`. |
| `FDT Overall Alarm Index` | array | Breakdown of FDTs by `Optimal` / `Good` / `Bad` alarm index percentage. |
| `Top 10 worst FDT Service Index` | object | `Data` array of the 10 worst-performing FDTs by `service_index`. |
| `Top 10 worst FDT Alarm Index` | object | `Data` array of the 10 worst-performing FDTs by `power_index`. |
| `Daily FDT Indexes` | object | `Data` array of historical/live service and alarm index values per `row_version` date. |
| `Alarms` | object | Same shape as `Daily FDT Indexes`, used for the alarms trend chart. |
| `map` | object | `Data` array of per-district network status counts and percentages, plus `tp_pi`/`fdt_pi` index values. |
| `Table` | object | `Data` array of per-FDT detail rows (region, district, hay, counts, fault rate, power/service index). |

```json
{
  "Service Index Average": { "average": 99.5 },
  "Alarm Index Average": { "average": 99.5 },
  "FDT Overall Service Index": [
    { "Optimal": 99.81 },
    { "Good": 0.18 },
    { "Bad": 0.01 }
  ]
}
```

---

## 5. Chat

### `POST /api/v1/chat`

Application-side adapter for the AI team's chatbot service. Mock mode is enabled by default. When external forwarding is enabled, the API forwards the request to the configured AI service and passes through the same `X-Request-ID`.

### Request headers

| Header | Required | Value |
|---|---:|---|
| `Content-Type` | Yes | `application/json` |
| `X-Request-ID` | No | Caller-supplied correlation ID. |

### Request body

| Field | Type | Required | Constraints | Description |
|---|---|---:|---|---|
| `message` | string | Yes | 1 to 8,000 characters | User message sent to the AI service. |
| `conversation_id` | string or null | No | No fixed format | Existing conversation identifier. If omitted, one is generated. |

**Example request:**

```bash
curl -i -X POST \
  http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: chat-request-001" \
  -d '{
    "message": "What is the current network status?",
    "conversation_id": "conv-001"
  }'
```

### Success response: `200 OK`

| Field | Type | Description |
|---|---|---|
| `conversation_id` | string | Conversation identifier, supplied or generated. |
| `message_id` | string | Identifier for the generated response message. |
| `answer` | string | AI response text. |
| `generated_at` | string | ISO 8601 timestamp with timezone. |
| `provider` | string | `mock` in mock mode or `external` when forwarded. |

```json
{
  "conversation_id": "conv-001",
  "message_id": "msg-example",
  "answer": "Mock AI response. The integration endpoint is working.",
  "generated_at": "2026-09-15T15:00:00+03:00",
  "provider": "mock"
}
```

### Configuration behavior

- Mock mode is enabled by default with `MOCK_AI_ENABLED=true`.
- To forward requests, set `MOCK_AI_ENABLED=false` and configure `AI_SERVICE_URL`.
- The upstream path is configured with `AI_CHAT_PATH`.
- The adapter sends the JSON request body and `X-Request-ID` to the upstream service.

---

## Error Responses

### Standard application error

Application errors use the following envelope:

```json
{
  "error": {
    "code": "AI_SERVICE_UNAVAILABLE",
    "message": "The AI service is temporarily unavailable.",
    "request_id": "chat-request-001"
  }
}
```

| HTTP status | Error code | When it occurs |
|---:|---|---|
| `404` | `DASHBOARD_NOT_FOUND` or `USER_NOT_FOUND` | A requested application resource cannot be found. |
| `502` | `AI_SERVICE_UNAVAILABLE` | The configured external AI service cannot be reached or returns an unusable response. |
| `500` | Application-specific | An unhandled application error is represented by the configured application error handler. |

### Request validation error

Invalid request bodies return `422 Unprocessable Entity`:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "request_id": "chat-request-001",
    "details": []
  }
}
```

For example, `POST /api/v1/chat` returns `422` when `message` is missing, empty, or longer than 8,000 characters, or when the JSON body is invalid.

## Mock Data and Refresh Behavior

Dashboard responses are generated from controlled snapshots. Within one `MOCK_DATA_REFRESH_SECONDS` bucket, requests receive the same snapshot. Timestamps and selected operational metrics may change between buckets while the response structure remains stable.

The dashboard scenario can be selected with `MOCK_SCENARIO`: `source`, `normal`, `warning`, or `critical`.
