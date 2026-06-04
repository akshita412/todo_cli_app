---
agent-notes:
  ctx: "technical debt register, persists across sprints"
  deps: []
  state: stub
  last: "grace@2026-02-15"
  key: ["Grace tracks, Pat prioritizes against features"]
---
# Technical Debt Register

<!-- Grace maintains this register. Pat prioritizes debt against feature work. -->
<!-- This persists across sprints — board items get closed, but debt lives here until resolved. -->

**Project:** todo-cli
**Last reviewed:** 2026-06-04

## Active Debt

| ID | Description | Incurred | Why (business reason) | Est. cost to fix | Risk if left | Sprint to fix | Status |
|----|-------------|----------|----------------------|-----------------|-------------|--------------|--------|
| TD-001 | `datetime.utcnow()` is deprecated in 3.12 and returns a naive datetime; used in `models.py:19` (`created_at`) and `service.py` (`completed_at`). Migrate project-wide to `datetime.now(timezone.utc)`. | M3 (2026-06-04) | Matched existing `models.py` pattern to keep M3 consistent rather than mix tz-aware/naive in one record. | S (<1 day) | Low now (warnings only); naive timestamps risk off-by-tz bugs once timestamps are displayed/compared. | TBD | Open |
| TD-002 | `JsonStorageBackend._save` truncates the real file in-place (non-atomic) and `_load`/`_deserialize` have no guard against a corrupt/truncated `tasks.json` — a crash mid-write or hand-edited file surfaces a raw `JSONDecodeError`/`KeyError`. Use temp-file + `os.replace()` and wrap load in a domain error. | M3 review (2026-06-04), pre-existing in M2 | Storage shipped as the happy-path MVP. | M (1-2 days) | Medium: data loss / unrecoverable store on crash or disk-full. | TBD | Open |

## Resolved Debt

| ID | Description | Incurred | Resolved | How it was fixed |
|----|-------------|----------|----------|-----------------|
| | | | | |

## Debt Categories

Tag each debt item to track patterns:

| Category | Count | Trend |
|----------|-------|-------|
| Missing tests | | |
| Hardcoded values | | |
| Missing error handling | | |
| Copy-paste duplication | | |
| Outdated dependencies | | |
| Missing docs | | |
| Performance | | |
| Security | | |
| Accessibility | | |

## Review Cadence

- **Sprint boundary:** Grace reviews the register. New debt discovered during the sprint is added. Pat decides what to pay down next sprint.
- **Every 3 sprints:** Full debt review. Re-estimate costs. Re-assess risks. Anything that's been open for 3+ sprints gets escalated.
