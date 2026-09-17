# Back to School Mock API Endpoint Documentation

## Overview

- **Base URL:** `http://localhost:8000`
- **OpenAPI:** `GET /openapi.json`
- **Swagger UI:** `GET /docs`
- **ReDoc:** `GET /redoc`
- **Authentication:** Bearer JWT authentication for protected endpoints (`/api/v1/users/me`, `/api/v1/chat`, `/api/v1/chat/history/{conversation_id}`).
- **Content type:** JSON responses use `Content-Type: application/json`.
- **Correlation:** Every request may include `X-Request-ID`. The API echoes the supplied value or generates a UUID and returns it in the response header.

All endpoints have no path parameters or query parameters unless stated otherwise.

## Common Headers

### Request headers

| Header | Required | Description |
|---|---:|---|
| `X-Request-ID` | No | Caller-supplied correlation ID. A UUID is generated when omitted. |
| `Content-Type` | POST only | Must be `application/json` for requests with a JSON body. |
| `Authorization` | Protected routes | `Bearer <access_token>` retrieved from `/api/v1/auth/login`. |

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
| `POST` | `/api/v1/auth/login` | Authenticate user credentials and issue JWT token. |
| `GET` | `/api/v1/users/me` | Return the current authenticated user profile. |
| `GET` | `/api/ExternalService/get_back_to_school_service_assurance_dashboard_payload` | B2S1 service assurance dashboard. |
| `GET` | `/api/ExternalService/get_back_to_school_complaint_intelligence_dashboard_payload` | B2S2 complaint intelligence dashboard. |
| `GET` | `/api/ExternalService/get_back_to_school_service_operations_dashboard_payload` | B2S3 service operations dashboard. |
| `GET` | `/api/ExternalService/get_back_to_school_ftth_maturity_index_dashboard_payload` | B2S4 FTTH maturity index dashboard. |
| `POST` | `/api/v1/chat` | Send a message through the AI integration boundary. |
| `GET` | `/api/v1/chat/history/{conversation_id}` | Retrieve history of conversation with the AI chatbot. |
| `POST` | `/api/v1/chat/welcome` | Retrieve initial welcome greeting and starter prompts. |

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

## 3. User Authentication

### `POST /api/v1/auth/login`

Authenticates user credentials and returns a JWT Bearer access token.

**Request headers:**

| Header | Required | Value |
|---|---:|---|
| `Content-Type` | Yes | `application/json` |
| `X-Request-ID` | No | Caller-supplied correlation ID. |

**Request body:**

| Field | Type | Required | Description |
|---|---|---:|---|
| `username_or_email` | string | Yes | Username or email address of the user. |
| `password` | string | Yes | User password. |

**Example request:**

```bash
curl -i -X POST \
  http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: auth-login-001" \
  -d '{
    "username_or_email": "hazem.hossam",
    "password": "password123"
  }'
```

**Success response: `200 OK`**

| Field | Type | Description |
|---|---|---|
| `access_token` | string | JWT Bearer access token. |
| `token_type` | string | Token type (always `bearer`). |
| `expires_in` | integer | Access token expiration in seconds. |

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## 4. Current User

### `GET /api/v1/users/me`

Returns the authenticated user details for chatbot greeting and personalization. Requires Bearer token authentication.

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

Returns the Back to School **Service Assurance** dashboard model. The dashboard focuses on network health, readiness, major outages, content-delivery traffic, and digital-application experience.

**Observed payload version:** `0.6.0-draft`  
**Command ID:** `service_assurance`  
**Timezone:** `Asia/Riyadh`

```bash
curl -i \
  -H "X-Request-ID: b2s1-request-001" \
  http://localhost:8000/api/ExternalService/get_back_to_school_service_assurance_dashboard_payload
```

#### Dashboard purpose

This dashboard gives the consumer a network-oriented operational view. It can be used by the UI or AI assistant to answer questions such as:

- What is the overall network status?
- Are there active outages or MDTs?
- Is Internet gateway capacity healthy?
- Are BRAS/authentication services stable?
- Which regions are currently affected by outages?
- Which CDN providers are saturated?
- Are major digital applications showing abnormal traffic or reported issues?

#### Section inventory

| Order | `section_id` | Display title | Observed status | Purpose |
|---:|---|---|---|---|
| 1 | `service_overview` | Service Assurance Overview | `warning` | Headline network KPIs and a compact status strip for monitored network layers. |
| 2 | `internet_service_watch` | Internet Service Watch | `optimal` | Internet gateway capacity plus BRAS authentication/subscriber indicators. |
| 3 | `logical_access_outages` | Logical & Access Major Outages | `warning` | Outage totals, regional impact, logical events, MDTs, and active outages. |
| 4 | `content_delivery_applications` | Content Delivery & Applications Watch | `warning` | CDN-provider traffic and digital-application experience. |

#### 4.1.1 `service_overview` — Service Assurance Overview

Provides the quickest summary of current network state.

**Important response blocks**

| Field | Type | Meaning |
|---|---|---|
| `cards` | array | Headline service-assurance KPI cards. |
| `cards[].label` | string | KPI display name, such as `Overall status`, `Active MDTs`, `Active outages`, or `Congestion incidents`. |
| `cards[].value` | integer or string | KPI value. |
| `cards[].kpi_id` | string | Stable KPI identifier such as `overall_network_status`, `active_mdts`, `active_outages`. |
| `cards[].status` | string | Semantic state such as `warning` or `optimal`. |
| `cards[].caption` | string | Human-readable explanation of the KPI. |
| `layer_strip` | array | Compact health view across monitored network layers. |
| `layer_strip[].name` | string | Layer short name such as `IGW`, `BRAS`, `MPLS`, `ACCESS`, `NNI`. |
| `layer_strip[].label` | string | Human-readable layer name. |
| `layer_strip[].signal` | string | Short current signal such as `Stable` or `4 congested`. |
| `layer_strip[].status` | string | Layer semantic status. |

**Example interpretation**

If `cards[kpi_id=overall_network_status].value` is `WARNING`, while `active_outages` or `active_mdts` is greater than zero, the AI assistant can describe the network as having an active operational risk and then use the other B2S1 sections to explain where it is occurring.

#### 4.1.2 `internet_service_watch` — Internet Service Watch

Contains two major components: `igw` and `bras`.

##### IGW — Internet Gateway

| Field | Type | Meaning |
|---|---|---|
| `igw.title` | string | Internet gateway component title. |
| `igw.status` | string | Current IGW semantic status. |
| `igw.trend.unit` | string | Traffic unit, observed as `Tbps`. |
| `igw.trend.times` | array[string] | Ordered time labels. |
| `igw.trend.values` | array[number] | Traffic values aligned positionally with `times`. |
| `igw.trend.granularity` | string | Observed as `hourly`. |
| `igw.trend.active_event_ids` | array[array] | Event IDs aligned to trend points. |
| `igw.compact_metrics` | array | Summary metrics for average traffic, peak utilization, links down, congestion, total links, and capacity. |
| `igw.compact_metrics[].label` | string | Metric label. |
| `igw.compact_metrics[].value` | integer or string | Display value, sometimes already including units. |
| `igw.compact_metrics[].status` | string | Metric status. |

**Important integration rule:** arrays such as `times`, `values`, and `active_event_ids` are positionally aligned and should preserve the same length/order.

##### BRAS — Authentication / Subscriber View

| Field | Type | Meaning |
|---|---|---|
| `bras.title` | string | BRAS component title. |
| `bras.status` | string | Current BRAS status. |
| `bras.trend.times` | array[string] | Ordered 15-minute time labels. |
| `bras.trend.dropped.latest` | integer | Latest dropped-session value. |
| `bras.trend.dropped.values` | array[integer] | Dropped-session time series. |
| `bras.trend.connected.latest` | integer | Latest connected-session value. |
| `bras.trend.connected.values` | array[integer] | Connected-session time series. |
| `bras.trend.granularity` | string | Observed as `15_minutes`. |
| `bras.auth_util` | array | Status buckets such as Normal / Warning / Critical. |
| `bras.auth_scale` | array | Estate-scale metrics such as BRAS nodes, uplinks, and active subscribers. |

This section is the main source for AI questions about Internet gateway load, BRAS readiness, subscriber authentication, connected sessions, or dropped sessions.

#### 4.1.3 `logical_access_outages` — Logical & Access Major Outages

Provides outage state and geographical impact.

##### Summary

| Field | Type | Meaning |
|---|---|---|
| `summary.aaa_count` | integer | AAA-related outage count. |
| `summary.total_count` | integer | Total outage-group record count. |
| `summary.logical_count` | integer | Logical outage/escalation count. |
| `summary.with_rtts_count` | integer | Records associated with RTTS. |
| `summary.open_critical_count` | integer | Currently open critical records. |
| `summary.latest_detection_time` | string or null | Latest detection timestamp when available. |

##### Regional outage map

`regional_outage_map.regions` contains one record per returned region/district view.

| Field | Type | Meaning |
|---|---|---|
| `region` | string | Region name. |
| `region_id` | string | Stable region code, e.g. `SA-01`. |
| `display_name` | string or null | Consumer-facing location name. |
| `status` | string | Region state. |
| `active_outages` | integer | Active outage count. |
| `outage_types` | string | Formatted breakdown such as `PON: 61, Single: 1`. |
| `impacted_services` | integer | Number of impacted services. |
| `has_active_mdt` | boolean | Whether an MDT is active. |
| `active_mdt_count` | integer | Active MDT count. |
| `is_raining` | boolean | Weather context. |
| `weather_status` | string | Weather description such as `Clear` or `Rain`. |

##### Active outage collections

- `active_logical_events.events`: active logical-event records. The supplied sample is empty, therefore item shape is not fully demonstrated.
- `combined_active_outages.outages`: combined MDT/logical/physical outage records.
- `combined_active_outages.total_count`: total combined active outages.
- `combined_active_outages.mdt_count`, `logical_count`, `physical_count`, `agg_count`: counts by source/type.

Typical outage records may include fields such as `node`, `type`, `status`, `district`, `severity`, `reference`, `created_at`, `closed_at`, `description`, `source_type`, `initiated_by`, and `impacted_customers`.

#### 4.1.4 `content_delivery_applications` — Content Delivery & Applications Watch

Contains both CDN-provider traffic and digital-application experience.

##### CDN provider data

| Field | Type | Meaning |
|---|---|---|
| `cdn.title` | string | CDN component title. |
| `cdn.status` | string | Overall CDN status. |
| `cdn.providers` | array | Provider-level traffic records. |
| `cdn.providers[].name` | string | Provider name, e.g. Google, Meta, Amazon, Akamai, etc. |
| `cdn.providers[].traffic` | string | Current formatted traffic value. |
| `cdn.providers[].share_pct` | number | Provider share of traffic. |
| `cdn.providers[].saturated` | boolean | Saturation flag. |
| `cdn.providers[].utilization_pct` | number or null | Utilization percentage when available. |
| `cdn.providers[].trend.times` | array[string] | Ordered time labels. |
| `cdn.providers[].trend.values` | array[number] | Current traffic time series. |
| `cdn.providers[].trend.past_week_values` | array[number] | Comparison series from the previous week. |
| `cdn.saturated_count` | integer | Number of saturated providers. |
| `cdn.rotation_hint_seconds` | integer | UI rotation/display hint. |

##### Application tower data

`applications.towers` groups applications by experience tower.

Each tower contains:

- `title`
- `tone`
- `apps`

Each app may include:

| Field | Type | Meaning |
|---|---|---|
| `name` | string | Application/service name. |
| `status` | string | Application semantic status. |
| `traffic` | string | Formatted observed traffic. |
| `deviation_pct` | number | Traffic deviation percentage. |
| `downdetector_status` | string | External issue signal such as `no issue`. |
| `image` | string or null | Optional image path. |
| `color` | string | Presentation color token. |

For the AI assistant, this section is useful when asked whether a particular content provider or digital application appears degraded, saturated, or abnormal.

---

### 4.2 B2S2 Complaint Intelligence

#### `GET /api/ExternalService/get_back_to_school_complaint_intelligence_dashboard_payload`

Returns the Back to School **Complaint Intelligence** dashboard model. It combines live complaint behavior, customer journey KPIs, operational-team efficiency, active events, AI root-cause output, and historical comparison data.

**Observed payload version:** `0.6.0-draft`  
**Command ID:** `complaint_intelligence`  
**Timezone:** `Asia/Riyadh`

```bash
curl -i \
  -H "X-Request-ID: b2s2-request-001" \
  http://localhost:8000/api/ExternalService/get_back_to_school_complaint_intelligence_dashboard_payload
```

#### Dashboard purpose

This dashboard is the main data source for AI questions such as:

- Are complaints currently above normal?
- Which complaint category is increasing?
- How does today compare with the moving baseline?
- What is the customer journey health score?
- Which operational team is handling complaints best/worst?
- Are there active network events that may explain complaint growth?
- What does the RCA analysis say?
- How do actual complaint volumes compare with historical/predicted behavior?

#### Section inventory

| Order | `section_id` | Display title | Observed status | Purpose |
|---:|---|---|---|---|
| 1 | `complaint_performance` | Live Hourly Complaints | `optimal` | Live cards, hourly category heatmap, daily trend, and hourly trend. |
| 2 | `customer_journey_kpis` | Customer Journey Health | `optimal` | Journey KPI values and calculated health score. |
| 3 | `team_kpis` | Team Handling Efficiency | `optimal` | Operational-team KPI values and team scores. |
| 4 | `active_events` | Active Events (Possible Risk) | `optimal` | Active events that may affect complaints/customer experience. |
| 6 | `ai_rca_insights` | AI RCA Insights | `optimal` | AI RCA analysis period, anomaly outcome, and generated HTML analysis. |
| 7 | `load_history_analysis` | Load History Analysis | `optimal` | Actual/predicted complaint history, event windows, journey history, and team-efficiency history. |
| 8 | `non_operational_teams` | Non-Operational Teams | `optimal` | KPI data for teams outside the primary operational group. |

#### 4.2.1 `complaint_performance` — Live Hourly Complaints

##### Summary cards

Observed cards include:

- Complaint status
- Total Open (Live)
- Total Created Today
- Deviation %
- On Hold Tickets

Each card may contain:

| Field | Meaning |
|---|---|
| `unit` | Unit such as `status`, `tickets`, `complaints`, or `%`. |
| `label` | Display label. |
| `value` | Actual KPI value. |
| `kpi_id` | Stable KPI identifier. |
| `status` / `color` | Semantic/presentation state. |
| `window.start`, `window.end`, `window.end_rule` | Time-window definition. |
| `baseline` | Moving-baseline object when applicable. |
| `comparison.absolute` | Signed absolute delta from baseline. |
| `comparison.direction` | `lower_is_better` or `higher_is_better`. |
| `comparison.percentage` | Signed percent difference where defined. |

##### Heatmap

`heatmap.categories` contains complaint categories, each with hourly values.

Observed categories include FTTH Physical, FTTH Logical, Copper, and OLO.

Each hourly point contains:

- `hour`
- `value`
- `baseline`
- `status`
- `color`

`heatmap.granularity` is `hourly`, and `window_hours` is `24`.

##### Daily trend

`daily_trend.points[]` contains:

- `date`
- `actual`
- `baseline`
- `status`
- `color`
- `active_event_ids`

The sample uses a 30-day daily window and `moving_same_weekday` baseline mode.

##### Hourly trend

`hourly_trend.points[]` contains:

- `hour`
- `actual`
- `baseline`
- `status`
- `color`
- `active_event_names`

This is useful to correlate complaint behavior with special events during the day.

#### 4.2.2 `customer_journey_kpis` — Customer Journey Health

Contains journey-level KPIs such as:

- Created Tickets
- Total Open
- Aged >24 Hours
- Total Closure
- Single Referral Closure

Common KPI structure includes:

`unit`, `label`, `value`, `kpi_id`, `status`, `color`, `window`, `baseline`, `comparison`, and in some cases `sample_size`.

##### Health score

`health_score` contains:

| Field | Meaning |
|---|---|
| `mode` | How the score was produced, observed as `calculated`. |
| `value` | Composite journey health score. |
| `status` | Semantic state. |
| `color` | Presentation state. |
| `basis` | KPI IDs contributing to the score. |
| `note` | Explanation of the current scoring methodology. |

The supplied sample describes the score as a calculated composite based on demand-adjusted load absorption, aged-ticket exposure, and first-referral behavior.

#### 4.2.3 `team_kpis` — Team Handling Efficiency

Contains KPI records for operational teams such as `SOC-T2`, `CSDD`, and `FOC`.

Observed KPI families include:

- Closure
- Aged Tickets
- First-Referral Closure Rate
- Closure Rate

Important fields include:

`team_id`, `kpi_id`, `label`, `value`, `count`, `sample_size`, `total_at_stage`, `window`, `baseline`, and `comparison`.

##### Team scores

`team_scores` contains:

- `mode`
- `note`
- `scores[]`

Each score includes:

- `team_id`
- `score`
- `status`
- `color`

This is the most direct block for AI questions comparing current operational-team handling performance, while detailed KPI values should be used to explain the reason behind a score.

#### 4.2.4 `active_events` — Active Events (Possible Risk)

`events[]` may include:

| Field | Meaning |
|---|---|
| `risk` | Risk classification. |
| `type` | Event type, e.g. `MDT`. |
| `status` / `color` | Current state. |
| `location` | Event location. |
| `operator` | Associated operator. |
| `start_at` | Event start timestamp. |
| `reference` | External reference/change ID. |
| `impacted_services` | Number of impacted services. |
| `latitude`, `longitude` | Optional geolocation; null in the supplied sample. |

This section should be checked before the AI attributes unusual complaint volumes to a network event.

#### 4.2.5 `ai_rca_insights` — AI RCA Insights

Contains the AI-generated root-cause analysis output already supplied by the source dashboard.

| Field | Meaning |
|---|---|
| `output_key` | Identifier for the generated analysis output. |
| `generated_at` | Generation timestamp. |
| `selected_date` | Date analyzed. |
| `selected_hour` | Hour analyzed. |
| `anomaly_status` | Result of anomaly qualification, e.g. `NO_QUALIFYING_INCREASE`. |
| `note` | Optional note. |
| `ai_section_html` | HTML fragment containing the RCA narrative and visual evidence. |

**Security/integration note:** `ai_section_html` is HTML content. A consumer that renders it should apply an agreed HTML trust/sanitization policy rather than injecting arbitrary HTML without validation.

#### 4.2.6 `load_history_analysis` — Load History Analysis

This section provides historical/comparison context rather than only the current snapshot.

Its role is to expose:

- actual complaint history
- predicted/baseline complaint history
- event windows/context
- customer-journey history
- team-efficiency history

Consumers should use this section for trend-oriented questions such as “is today unusual compared with previous periods?” instead of relying only on current KPI cards.

#### 4.2.7 `non_operational_teams` — Non-Operational Teams

Contains KPI values for teams outside the primary operational-team grouping.

Observed KPI records include fields such as:

`unit`, `label`, `value`, `kpi_id`, `status`, `window`, `team_id`, `baseline`, `comparison`, `count`, and `total_at_stage`.

Observed labels include examples such as Pending Tickets, Closures, and Closure Rate.

---

### 4.3 B2S3 Service Operations

#### `GET /api/ExternalService/get_back_to_school_service_operations_dashboard_payload`

Returns the Back to School **Service Operations** dashboard model, covering deviation metrics, workload composition, daily ticket load, deviation drivers, district workload, ageing/ownership, and CST escalation trends.

**Observed payload version:** `0.1.0-draft`  
**Command ID:** `service_operations`  
**Timezone:** `Asia/Riyadh`

```bash
curl -i \
  -H "X-Request-ID: b2s3-request-001" \
  http://localhost:8000/api/ExternalService/get_back_to_school_service_operations_dashboard_payload
```

#### Dashboard purpose

This dashboard is the main source for questions such as:

- Which operational entities have the largest deviation from baseline?
- How is the open workload split by technology?
- How many tickets are open versus reopened?
- Is the ticket workload increasing or decreasing?
- Which OLT/FDT/HAY/ONT entities are driving complaint deviation?
- Which district has the highest current ticket load?
- How many tickets are older than one or three days?
- Which operational stage owns the aged workload?
- What is the current CST escalation pattern by operator?

#### Section inventory

| Order | `section_id` | Display title | Observed status | Purpose |
|---:|---|---|---|---|
| 1 | `top_metrics` | Operational Deviation Watch | `critical` | Worst-performing entities by hierarchy dimension relative to baseline. |
| 2 | `workload_distribution` | Operational Workload Distribution | `optimal` | Workload composition and reopen exposure as donut datasets. |
| 3 | `daily_load_trend` | Daily Load Trend | `optimal` | Daily created, closed, and still-open ticket counts. |
| 4 | `deviation_drivers` | Complaint Deviation Drivers | `critical` | Ranked entities whose complaint volumes deviate from baseline. |
| 5 | `district_ticket_workload` | District Ticket Workload | `optimal` | Currently open ticket counts by district/region. |
| 6 | `execution_ownership_ageing` | Execution Ownership & Ageing | `warning` | Ticket-age exposure totals and values by operational stage. |
| 7 | `cst_escalation_watch` | CST Escalation Watch | `optimal` | Ten-day CST escalation totals and operator/reason trends. |

#### 4.3.1 `top_metrics` — Operational Deviation Watch

`kpis[]` identifies the most notable entity in each operational hierarchy dimension.

Observed dimensions:

- `olt`
- `fdt`
- `hay`
- `ont_type`

Each KPI may include:

| Field | Meaning |
|---|---|
| `kpi_id` | Stable KPI identifier. |
| `label` | KPI label. |
| `dimension` | Operational hierarchy dimension. |
| `entity_id` | Stable entity identifier. |
| `entity_label` | Display label. |
| `count` | Current ticket/complaint count. |
| `baseline` | Baseline count. |
| `deviation_pct` | Percent difference from baseline. |
| `status` | Semantic state. |
| `unit` | Observed as `tickets`. |

This is the fastest section for identifying the current top deviation per hierarchy.

#### 4.3.2 `workload_distribution` — Operational Workload Distribution

Contains donut chart datasets.

Observed charts:

- `technology_mix`
- `open_vs_reopen`

Each chart contains:

- `chart_id`
- `type` (`donut`)
- `total`
- `segments[]`

Each segment contains:

- `key`
- `label`
- `count`
- `pct`

Technology segments observed include FTTH, OLO, and Copper. Open/reopen segments show the current open-ticket population versus reopened tickets.

#### 4.3.3 `daily_load_trend` — Daily Load Trend

`trend[]` contains one record per date:

| Field | Meaning |
|---|---|
| `date` | Calendar date. |
| `created` | Tickets created that day. |
| `closed` | Tickets closed that day. |
| `still_open` | Tickets created that day which remain open. |

This is useful for workload trajectory and backlog questions.

#### 4.3.4 `deviation_drivers` — Complaint Deviation Drivers

`driver_groups[]` ranks entities by operational hierarchy.

Observed groups include:

- Top 5 OLTs
- Top 5 FDTs
- Top 5 HAY
- Top 5 ONT Types

Each group includes:

`label`, `dimension`, `status`, `color`, and `items[]`.

Each item includes:

| Field | Meaning |
|---|---|
| `entity_id` / `entity_label` | Entity identity. |
| `count` | Current complaint/ticket count. |
| `baseline` | Baseline count. |
| `deviation_pct` | Percent difference from baseline; may be null when baseline is zero. |
| `load_pct` | Entity share of applicable workload. |
| `status` | Entity status. |

For AI explanations, this section is more detailed than `top_metrics` because it provides ranked lists instead of only one entity per dimension.

#### 4.3.5 `district_ticket_workload` — District Ticket Workload

`regions[]` contains current open workload by district.

Each record contains:

- `region`
- `region_id`
- `region_ord`
- `district_display_name`
- `ticket_count`

This is the primary section for questions such as “which district currently has the most open tickets?”

#### 4.3.6 `execution_ownership_ageing` — Execution Ownership & Ageing

##### Overall summary

`summary` contains:

- `days_1_3`
- `over_1_day`
- `over_3_days`

##### By-stage breakdown

`by_stage[]` contains:

- `team_id`
- `stage_id`
- `days_1_3`
- `over_1_day`
- `over_3_days`

Observed stages include `CSDD`, `SOC-FTR`, `IVR`, `FOC`, `SOC-Quality`, and `SOC-T2`.

This section should be used when the AI needs to explain both the size of aged-ticket exposure and which stage/team currently owns that exposure.

#### 4.3.7 `cst_escalation_watch` — CST Escalation Watch

Contains current totals plus a ten-day operator trend.

Top-level fields include:

- `stc_total`
- `total_cst`
- `window_days`
- `olo_total_trend`
- `operator_trends`
- `operators_summary`

##### Trend point structure

Each trend point contains:

- `date`
- `total`
- `logical`
- `mdt/mso`
- `physical`

Note that `mdt/mso` is a literal JSON property name and should be accessed exactly as supplied.

##### Operator trend structure

Each operator trend contains:

- `operator_id`
- `label`
- `current_total`
- `trend[]`

Observed operators include STC, Dawiyat, ITC, Mobily, ACES, and Unknown.

`operators_summary[]` provides a compact current count per operator.

---

#### AI consumption guidance for B2S1–B2S3

When the chatbot needs dashboard context, it should prefer stable identifiers over display text.

| User intent | Recommended dashboard/section |
|---|---|
| Overall network status | B2S1 `service_overview` |
| Internet gateway load/capacity | B2S1 `internet_service_watch.igw` |
| BRAS/authentication/subscribers | B2S1 `internet_service_watch.bras` |
| Regional outages / MDTs | B2S1 `logical_access_outages` |
| CDN/application health | B2S1 `content_delivery_applications` |
| Current complaint volume | B2S2 `complaint_performance` |
| Complaint baseline/deviation | B2S2 `complaint_performance` |
| Customer journey health | B2S2 `customer_journey_kpis` |
| Operational team performance | B2S2 `team_kpis` |
| Possible external/network cause | B2S2 `active_events` |
| Existing dashboard RCA narrative | B2S2 `ai_rca_insights` |
| Historical complaint analysis | B2S2 `load_history_analysis` |
| Non-primary team KPIs | B2S2 `non_operational_teams` |
| Largest operational deviation | B2S3 `top_metrics` |
| Workload technology split | B2S3 `workload_distribution` |
| Created/closed/open trend | B2S3 `daily_load_trend` |
| Ranked deviation causes | B2S3 `deviation_drivers` |
| District workload | B2S3 `district_ticket_workload` |
| Ticket ageing/ownership | B2S3 `execution_ownership_ageing` |
| CST/operator escalations | B2S3 `cst_escalation_watch` |

**General interpretation rules**

- Use `data_as_of` to tell the user how fresh the dashboard snapshot is.
- Use `generated_at` as payload-generation time, not necessarily the effective measurement time.
- Treat `baseline` and `comparison` together when explaining deviations.
- Respect `comparison.direction`; a negative delta is not automatically “good” or “bad”.
- Do not infer semantic status from `color` alone. The payload carries both status and presentation color.
- Preserve null values instead of fabricating missing data.
- `DataCount` may remain `0` while the dashboard is fully populated.
- For time-series structures, preserve positional alignment between timestamps and corresponding arrays.
- B2S3 currently uses payload version `0.1.0-draft`, while B2S1/B2S2 use `0.6.0-draft`; clients should not assume identical schema evolution.

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

## 6. Chat & AI Integration

### 6.1 Send Chat Message

#### `POST /api/v1/chat`

Application-side adapter for the AI team's chatbot service. Mock mode is enabled by default. Requires Bearer token authentication.

**Request headers:**

| Header | Required | Value |
|---|---:|---|
| `Authorization` | Yes | `Bearer <access_token>` |
| `Content-Type` | Yes | `application/json` |
| `X-Request-ID` | No | Caller-supplied correlation ID. |

**Request body:**

| Field | Type | Required | Constraints | Description |
|---|---|---:|---|---|
| `message` | string | Yes | 1 to 8,000 characters | User message sent to the AI service. |
| `conversation_id` | string or null | No | No fixed format | Existing conversation identifier. If omitted, one is generated. |

**Example request:**

```bash
curl -i -X POST \
  http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: chat-request-001" \
  -d '{
    "message": "What is the current network status?",
    "conversation_id": "conv-001"
  }'
```

**Success response: `200 OK`**

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

### 6.2 Get Conversation History

#### `GET /api/v1/chat/history/{conversation_id}`

Retrieves the message history for a given conversation ID with the AI chatbot. Requires Bearer token authentication.

**Path parameters:**

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `conversation_id` | string | Yes | Conversation identifier. |

**Request headers:**

| Header | Required | Value |
|---|---:|---|
| `Authorization` | Yes | `Bearer <access_token>` |
| `X-Request-ID` | No | Caller-supplied correlation ID. |

**Example request:**

```bash
curl -i \
  http://localhost:8000/api/v1/chat/history/conv-001 \
  -H "Authorization: Bearer <access_token>" \
  -H "X-Request-ID: chat-history-001"
```

**Success response: `200 OK`**

| Field | Type | Description |
|---|---|---|
| `conversation_id` | string | Conversation identifier. |
| `messages` | array | List of chat messages in chronological order. |
| `messages[].message_id` | string | Message identifier. |
| `messages[].role` | string | Role of the sender (`user` or `assistant`). |
| `messages[].content` | string | Message text content. |
| `messages[].timestamp` | string | ISO 8601 timestamp. |

```json
{
  "conversation_id": "conv-001",
  "messages": [
    {
      "message_id": "msg-001",
      "role": "user",
      "content": "Hello, I need assistance with network status.",
      "timestamp": "2026-09-17T12:00:00+03:00"
    },
    {
      "message_id": "msg-002",
      "role": "assistant",
      "content": "Hello Hazem! Mock AI response history for conversation 'conv-001'. All systems in Network Operations and Service Operations are running normally.",
      "timestamp": "2026-09-17T12:00:05+03:00"
    }
  ]
}
```

### 6.3 Welcome Message

#### `POST /api/v1/chat/welcome`

Fetches an initial personalized welcome greeting and starter prompts for a new or existing chatbot session. Requires Bearer token authentication.

**Request headers:**

| Header | Required | Value |
|---|---:|---|
| `Authorization` | Yes | `Bearer <access_token>` |
| `Content-Type` | Yes | `application/json` |
| `X-Request-ID` | No | Caller-supplied correlation ID. |

**Request body:**

| Field | Type | Required | Description |
|---|---|---:|---|
| `conversation_id` | string or null | No | Optional existing conversation identifier. If omitted, one is generated. |

**Example request:**

```bash
curl -i -X POST \
  http://localhost:8000/api/v1/chat/welcome \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: chat-welcome-001" \
  -d '{
    "conversation_id": "conv-001"
  }'
```

**Success response: `200 OK`**

| Field | Type | Description |
|---|---|---|
| `conversation_id` | string | Conversation identifier. |
| `message_id` | string | Message identifier for the welcome message. |
| `welcome_message` | string | Personalized greeting message. |
| `suggested_prompts` | array | List of starter/recommended prompt strings. |
| `generated_at` | string | ISO 8601 timestamp with timezone. |
| `provider` | string | `mock` in mock mode or `external` when forwarded. |

```json
{
  "conversation_id": "conv-001",
  "message_id": "msg-welcome-001",
  "welcome_message": "Hello Hazem! Welcome to the B2S Operations Assistant. How can I assist you with network assurance, complaints, or service operations today?",
  "suggested_prompts": [
    "What is the current network status?",
    "Show complaint intelligence overview",
    "View FTTH maturity index dashboard"
  ],
  "generated_at": "2026-09-17T13:35:00+03:00",
  "provider": "mock"
}
```

### Configuration behavior

- Mock mode is enabled by default with `MOCK_AI_ENABLED=true`.
- To forward requests, set `MOCK_AI_ENABLED=false` and configure `AI_SERVICE_URL`.
- The upstream path is configured with `AI_CHAT_PATH`.
- The adapter sends request headers and `X-Request-ID` to the upstream service.


---


## Dashboard Contract Notes

The detailed B2S1–B2S3 descriptions above are based on the supplied Back to School Interface Specification and the observed dashboard response samples. They describe the currently observed contract rather than a final normative schema. Fields marked nullable, mixed-type, or represented only by empty collections should remain compatible with the source payload until the API owner confirms a stricter production contract.

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
