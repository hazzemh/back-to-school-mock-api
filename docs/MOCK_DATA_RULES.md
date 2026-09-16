# Mock Data Rules

The source fixtures are exact copies of the supplied B2S1/B2S2/B2S3 successful responses.

A snapshot is generated once per `MOCK_DATA_REFRESH_SECONDS` bucket. All requests inside the same bucket receive the same snapshot, which makes UI and AI testing deterministic enough to reproduce while still behaving like live data.

Generation rules:

1. Preserve the complete JSON shape and field types.
2. Shift ISO timestamps and date-only fields forward relative to the source snapshot.
3. Update `meta.data_as_of` and `meta.generated_at` to the current snapshot bucket.
4. Jitter only selected operational metrics instead of randomizing every field.
5. Recalculate directly related percentages/totals where the relationship is clear.
6. Revalidate the final payload against the common Pydantic envelope before returning it.
7. Keep `DataCount` at the supplied value (`0`) for compatibility.

## Scenario mode

`MOCK_SCENARIO` can be `source`, `normal`, `warning`, or `critical`.

`source` is the safest default: it keeps the source section-level status semantics while live values evolve. The other modes are intended for demonstrations and QA; they override section-level presentation status/color without changing the JSON contract.
