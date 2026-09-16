# API Contract Notes

## Supplied dashboard contracts

The three legacy dashboard routes intentionally preserve the supplied URLs and success envelope:

```json
{
  "StatusCode": 200,
  "Messages": null,
  "Data": {
    "returned_data": {
      "meta": {},
      "sections": []
    }
  },
  "DataCount": 0
}
```

Do **not** use `DataCount` as a presence check. The supplied successful samples contain populated data while `DataCount` remains `0`.

### B2S1
`GET /api/ExternalService/get_back_to_school_service_assurance_dashboard_payload`

### B2S2
`GET /api/ExternalService/get_back_to_school_complaint_intelligence_dashboard_payload`

### B2S3
`GET /api/ExternalService/get_back_to_school_service_operations_dashboard_payload`

## New integration endpoints

### Current user
`GET /api/v1/users/me`

Returns structured user identity for chatbot personalization. It deliberately returns user data rather than a preformatted greeting.

### Chat
`POST /api/v1/chat`

```json
{
  "message": "Why are complaints high today?",
  "conversation_id": "conv-001"
}
```

Mock mode is enabled by default. When the AI team publishes its endpoint, configure `AI_SERVICE_URL`, `AI_CHAT_PATH`, and set `MOCK_AI_ENABLED=false`.

## Error contract for new endpoints

```json
{
  "error": {
    "code": "AI_SERVICE_UNAVAILABLE",
    "message": "The AI service is temporarily unavailable.",
    "request_id": "..."
  }
}
```

The legacy dashboard failure contract is intentionally not invented because the supplied specification marks it TBD.
