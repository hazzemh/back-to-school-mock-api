# AI Integration Guide

## Recommended flow

The AI service should consume the same dashboard APIs as any other client instead of receiving a separately duplicated data model.

- Network assurance/outages: call B2S1.
- Complaint/customer experience questions: call B2S2.
- Ticket workload/operations questions: call B2S3.
- Greeting/personalization: call `GET /api/v1/users/me`.

The application frontend can send chat messages to `POST /api/v1/chat`. This FastAPI endpoint is the stable application-side adapter and forwards to the AI team's service once its contract is available.

## Correlation

Every response contains an `X-Request-ID` header. A caller may provide its own `X-Request-ID`; otherwise the API generates one. The same ID is forwarded to the external AI service.

## OpenAPI

- Swagger: `/docs`
- ReDoc: `/redoc`
- OpenAPI document: `/openapi.json`

The Postman collection under `/postman` contains all routes and examples.
