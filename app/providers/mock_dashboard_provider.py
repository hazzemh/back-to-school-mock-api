from __future__ import annotations

import copy
import hashlib
import json
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
from typing import Any
from zoneinfo import ZoneInfo

from app.core.config import settings
from app.core.exceptions import DashboardNotFoundError
from app.schemas.common import DashboardEnvelope, FTTHMaturityIndexEnvelope

RIYADH = ZoneInfo("Asia/Riyadh")
ISO_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
NAIVE_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class MockDashboardProvider:
    """Loads source fixtures and emits deterministic, time-bucketed live snapshots.

    The response shape is always revalidated with Pydantic before it leaves this provider.
    """

    _files = {
        "service_assurance": "service_assurance.json",
        "complaint_intelligence": "complaint_intelligence.json",
        "service_operations": "service_operations.json",
        "ftth_maturity_index": "ftth_maturity_index.json",
    }
    _validators = {
        "service_assurance": DashboardEnvelope,
        "complaint_intelligence": DashboardEnvelope,
        "service_operations": DashboardEnvelope,
        "ftth_maturity_index": FTTHMaturityIndexEnvelope,
    }

    def __init__(self, data_dir: Path | None = None) -> None:
        self.data_dir = data_dir or Path(__file__).resolve().parents[1] / "mock_data"
        self._base: dict[str, dict[str, Any]] = {}
        self._cache: dict[str, tuple[int, dict[str, Any]]] = {}
        self._lock = Lock()
        for name, filename in self._files.items():
            with (self.data_dir / filename).open("r", encoding="utf-8") as f:
                payload = json.load(f)
                self._validators[name].model_validate(payload)
                self._base[name] = payload

    @property
    def dashboards(self) -> tuple[str, ...]:
        return tuple(self._files)

    def get(self, dashboard: str) -> dict[str, Any]:
        if dashboard not in self._base:
            raise DashboardNotFoundError(dashboard)

        now = datetime.now(tz=RIYADH)
        bucket = int(now.timestamp()) // settings.mock_data_refresh_seconds
        with self._lock:
            cached = self._cache.get(dashboard)
            if cached and cached[0] == bucket:
                return copy.deepcopy(cached[1])

            snapshot_time = datetime.fromtimestamp(
                bucket * settings.mock_data_refresh_seconds,
                tz=RIYADH,
            )
            payload = self._build_snapshot(dashboard, snapshot_time, bucket)
            self._cache[dashboard] = (bucket, payload)
            return copy.deepcopy(payload)

    def _build_snapshot(self, dashboard: str, snapshot_time: datetime, bucket: int) -> dict[str, Any]:
        payload = copy.deepcopy(self._base[dashboard])
        if dashboard == "ftth_maturity_index":
            self._shift_ftth_dates(payload, snapshot_time)
        else:
            meta = payload["Data"]["returned_data"]["meta"]
            anchor = datetime.fromisoformat(meta["data_as_of"])
            delta = snapshot_time - anchor
            self._shift_dates(payload, delta)
            meta = payload["Data"]["returned_data"]["meta"]
            meta["data_as_of"] = snapshot_time.isoformat()
            meta["generated_at"] = snapshot_time.isoformat()

        seed_bytes = hashlib.sha256(f"{dashboard}:{bucket}:{settings.mock_scenario}".encode()).digest()
        rng = random.Random(int.from_bytes(seed_bytes[:8], "big"))
        if dashboard == "service_assurance":
            self._mutate_service_assurance(payload, rng)
        elif dashboard == "complaint_intelligence":
            self._mutate_complaint_intelligence(payload, rng)
        elif dashboard == "service_operations":
            self._mutate_service_operations(payload, rng)
        elif dashboard == "ftth_maturity_index":
            self._mutate_ftth_maturity_index(payload, rng)

        if dashboard != "ftth_maturity_index":
            self._apply_scenario(payload, settings.mock_scenario)
        self._validators[dashboard].model_validate(payload)
        return payload

    def _shift_dates(self, node: Any, delta: timedelta) -> None:
        if isinstance(node, dict):
            for key, value in list(node.items()):
                if isinstance(value, str):
                    if ISO_DATETIME_RE.match(value):
                        try:
                            node[key] = (datetime.fromisoformat(value.replace("Z", "+00:00")) + delta).isoformat()
                        except ValueError:
                            pass
                    elif NAIVE_DATETIME_RE.match(value):
                        try:
                            node[key] = (datetime.strptime(value, "%Y-%m-%dT%H:%M:%S") + delta).strftime(
                                "%Y-%m-%dT%H:%M:%S"
                            )
                        except ValueError:
                            pass
                    elif DATE_RE.match(value):
                        try:
                            d = datetime.strptime(value, "%Y-%m-%d").date()
                            node[key] = (d + timedelta(days=delta.days)).isoformat()
                        except ValueError:
                            pass
                else:
                    self._shift_dates(value, delta)
        elif isinstance(node, list):
            for value in node:
                self._shift_dates(value, delta)

    def _shift_ftth_dates(self, payload: dict[str, Any], snapshot_time: datetime) -> None:
        rows = payload.get("Daily FDT Indexes", {}).get("Data", [])
        row_versions = []
        for row in rows:
            try:
                row_versions.append(datetime.strptime(row["row_version"], "%Y-%m-%dT%H:%M:%S"))
            except (KeyError, ValueError):
                continue
        if not row_versions:
            return
        delta = snapshot_time.replace(tzinfo=None) - max(row_versions)
        self._shift_dates(payload, delta)

    @staticmethod
    def _jitter_int(value: int, rng: random.Random, pct: float = 0.04, floor: int = 0) -> int:
        spread = max(1, round(abs(value) * pct))
        return max(floor, value + rng.randint(-spread, spread))

    @staticmethod
    def _jitter_float(value: float, rng: random.Random, pct: float = 0.01, floor: float = 0.0, ceil: float = 100.0) -> float:
        spread = max(0.01, abs(value) * pct)
        return round(max(floor, min(ceil, value + rng.uniform(-spread, spread))), 2)

    @staticmethod
    def _sections(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
        sections = payload["Data"]["returned_data"]["sections"]
        return {s["section_id"]: s for s in sections}

    def _mutate_service_assurance(self, payload: dict[str, Any], rng: random.Random) -> None:
        sections = self._sections(payload)
        overview = sections.get("service_overview", {})
        cards = {c.get("kpi_id"): c for c in overview.get("cards", [])}
        for kpi in ("active_outages", "congestion_incidents"):
            card = cards.get(kpi)
            if card and isinstance(card.get("value"), int):
                card["value"] = self._jitter_int(card["value"], rng, 0.08)
                if kpi == "congestion_incidents":
                    card["caption"] = f"{card['value']} incidents"

        watch = sections.get("internet_service_watch", {})
        igw = watch.get("igw", {})
        values = igw.get("trend", {}).get("values", [])
        if values:
            last = values[-1]
            if isinstance(last, (int, float)):
                values[-1] = round(max(0.0, last * (1 + rng.uniform(-0.025, 0.025))), 2)
        bras = watch.get("bras", {}).get("trend", {})
        for series_name in ("dropped", "connected"):
            series = bras.get(series_name, {})
            vals = series.get("values", [])
            if vals and isinstance(vals[-1], int):
                vals[-1] = self._jitter_int(vals[-1], rng, 0.06)
                series["latest"] = vals[-1]

        outages = sections.get("logical_access_outages", {}).get("regional_outage_map", {}).get("regions", [])
        for region in outages:
            if isinstance(region.get("active_outages"), int) and region["active_outages"] > 0:
                region["active_outages"] = self._jitter_int(region["active_outages"], rng, 0.06)
            if isinstance(region.get("impacted_services"), int) and region["impacted_services"] > 0:
                region["impacted_services"] = self._jitter_int(region["impacted_services"], rng, 0.05)

    def _mutate_complaint_intelligence(self, payload: dict[str, Any], rng: random.Random) -> None:
        sections = self._sections(payload)
        performance = sections.get("complaint_performance", {})
        cards = {c.get("kpi_id"): c for c in performance.get("cards", [])}
        values: dict[str, int] = {}
        for kpi in ("journey_total_open_live", "total_created_today", "journey_on_hold_tickets"):
            card = cards.get(kpi)
            if card and isinstance(card.get("value"), int):
                card["value"] = self._jitter_int(card["value"], rng, 0.04)
                values[kpi] = card["value"]
                baseline = card.get("baseline")
                comparison = card.get("comparison")
                if isinstance(baseline, dict) and isinstance(baseline.get("value"), int) and isinstance(comparison, dict):
                    b = baseline["value"]
                    comparison["absolute"] = card["value"] - b
                    comparison["percentage"] = round(((card["value"] - b) / b) * 100) if b else None

        # Synchronize equivalent journey KPIs with the headline values.
        journey = sections.get("customer_journey_kpis", {})
        for kpi in journey.get("kpis", []):
            if kpi.get("kpi_id") == "journey_created_tickets" and "total_created_today" in values:
                kpi["value"] = values["total_created_today"]
            elif kpi.get("kpi_id") == "journey_total_open" and "journey_total_open_live" in values:
                kpi["value"] = values["journey_total_open_live"]

        # Move the current endpoint of trend series slightly while retaining shape and type.
        for trend_key in ("daily_trend", "hourly_trend"):
            points = performance.get(trend_key, {}).get("points", [])
            actual_points = [p for p in points if isinstance(p.get("actual"), int)]
            if actual_points:
                actual_points[-1]["actual"] = self._jitter_int(actual_points[-1]["actual"], rng, 0.035)

        teams = sections.get("team_kpis", {}).get("kpis", [])
        for kpi in teams:
            if kpi.get("kpi_id") in {"team_closure", "team_aged_tickets"} and isinstance(kpi.get("value"), int):
                kpi["value"] = self._jitter_int(kpi["value"], rng, 0.04)

    def _mutate_service_operations(self, payload: dict[str, Any], rng: random.Random) -> None:
        sections = self._sections(payload)
        top = sections.get("top_metrics", {})
        for kpi in top.get("kpis", []):
            if isinstance(kpi.get("count"), int):
                kpi["count"] = self._jitter_int(kpi["count"], rng, 0.06)
                baseline = kpi.get("baseline")
                if isinstance(baseline, int):
                    kpi["deviation_pct"] = round(((kpi["count"] - baseline) / baseline) * 100, 1) if baseline else None

        workload = sections.get("workload_distribution", {})
        for chart in workload.get("charts", []):
            segments = chart.get("segments", [])
            for seg in segments:
                if isinstance(seg.get("count"), int):
                    seg["count"] = self._jitter_int(seg["count"], rng, 0.035)
            total = sum(seg.get("count", 0) for seg in segments if isinstance(seg.get("count"), int))
            chart["total"] = total
            if total:
                for seg in segments:
                    if isinstance(seg.get("count"), int):
                        seg["pct"] = round(seg["count"] / total * 100, 1)

        districts = sections.get("district_ticket_workload", {}).get("regions", [])
        for region in districts:
            if isinstance(region.get("ticket_count"), int):
                region["ticket_count"] = self._jitter_int(region["ticket_count"], rng, 0.05)

        ageing = sections.get("execution_ownership_ageing", {})
        for key in ("days_1_3", "over_1_day", "over_3_days"):
            if isinstance(ageing.get("summary", {}).get(key), int):
                ageing["summary"][key] = self._jitter_int(ageing["summary"][key], rng, 0.04)
        for stage in ageing.get("by_stage", []):
            for key in ("days_1_3", "over_1_day", "over_3_days"):
                if isinstance(stage.get(key), int):
                    stage[key] = self._jitter_int(stage[key], rng, 0.05)

        cst = sections.get("cst_escalation_watch", {})
        for key in ("stc_total", "total_cst"):
            if isinstance(cst.get(key), int):
                cst[key] = self._jitter_int(cst[key], rng, 0.08)

    @staticmethod
    def _jitter_breakdown(items: list[dict[str, float]], rng: random.Random) -> None:
        """Jitter a list of single-key {label: percentage} entries while keeping them summing to 100."""
        if not items:
            return
        pairs = [(k, v) for item in items for k, v in item.items()]
        jittered = [
            MockDashboardProvider._jitter_float(v, rng, 0.15, floor=0.0, ceil=100.0) if isinstance(v, (int, float)) else v
            for _, v in pairs
        ]
        total = sum(v for v in jittered if isinstance(v, (int, float)))
        if total:
            jittered = [round(v / total * 100, 2) if isinstance(v, (int, float)) else v for v in jittered]
            jittered[-1] = round(100 - sum(jittered[:-1]), 2)
        for item, (key, _), value in zip(items, pairs, jittered):
            item[key] = value

    def _mutate_ftth_maturity_index(self, payload: dict[str, Any], rng: random.Random) -> None:
        for key in ("FDT Alarm Index Avg", "TB Alarm Index Avg", "Customer Alarm Index Avg"):
            for row in payload.get(key, {}).get("Data", []):
                if isinstance(row.get("avg_pi"), (int, float)):
                    row["avg_pi"] = self._jitter_float(row["avg_pi"], rng, 0.01)

        for key in ("Service Index Average", "Alarm Index Average"):
            block = payload.get(key, {})
            if isinstance(block.get("average"), (int, float)):
                block["average"] = self._jitter_float(block["average"], rng, 0.005)

        for key in ("FDT Overall Service Index", "FDT Overall Alarm Index"):
            self._jitter_breakdown(payload.get(key, []), rng)

        for key in ("Top 10 worst FDT Service Index", "Top 10 worst FDT Alarm Index"):
            for row in payload.get(key, {}).get("Data", []):
                for field in ("service_index", "power_index"):
                    if isinstance(row.get(field), (int, float)):
                        row[field] = self._jitter_float(row[field], rng, 0.015)

        for key in ("Daily FDT Indexes", "Alarms"):
            for row in payload.get(key, {}).get("Data", []):
                for field in (
                    "historical_service_index",
                    "historical_alarm_index",
                    "live_service_index",
                    "live_alarm_index",
                ):
                    if isinstance(row.get(field), (int, float)):
                        row[field] = self._jitter_float(row[field], rng, 0.01)

        for row in payload.get("map", {}).get("Data", []):
            total = row.get("total")
            for count_field, pct_field in (
                ("down", "down_percent"),
                ("degraded", "degraded_percent"),
                ("up_unstable", "up_unstable_percent"),
                ("up_stable", "up_stable_percent"),
            ):
                if isinstance(row.get(count_field), int):
                    row[count_field] = self._jitter_int(row[count_field], rng, 0.05)
                    if isinstance(total, (int, float)) and total:
                        row[pct_field] = round(row[count_field] / total * 100, 6)
            if isinstance(row.get("fdt_pi"), (int, float)):
                row["fdt_pi"] = self._jitter_float(row["fdt_pi"], rng, 0.005)

        for row in payload.get("Table", {}).get("Data", []):
            for field in ("up_stable", "down", "degraded", "up_unstable", "faults", "mso", "cst"):
                if isinstance(row.get(field), int):
                    row[field] = self._jitter_int(row[field], rng, 0.06)
            for field in ("fault_rate", "mso_rate", "power_index", "service_index"):
                if isinstance(row.get(field), (int, float)):
                    row[field] = self._jitter_float(row[field], rng, 0.02)

    def _apply_scenario(self, payload: dict[str, Any], scenario: str) -> None:
        if scenario in {"source", ""}:
            return
        if scenario not in {"normal", "warning", "critical"}:
            return
        color = {"normal": "green", "warning": "orange", "critical": "red"}[scenario]
        status = {"normal": "optimal", "warning": "warning", "critical": "critical"}[scenario]
        sections = payload["Data"]["returned_data"]["sections"]
        # Scenario mode intentionally changes section-level presentation state only;
        # field-level source semantics remain intact so the contract stays realistic.
        for section in sections:
            if "status" in section:
                section["status"] = status
            if "color" in section:
                section["color"] = color
