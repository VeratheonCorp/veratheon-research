# Crash Contingency Plan for Research Job Status Updates

## Context
- **Main Flow Orchestration**: `src/flows/research_flow.py`
- **Job Tracking Layer**: `src/lib/supabase_job_tracker.py`
- **API Background Runner**: `server/api.py`
- **UI Realtime Consumer**: `agent-ui/src/routes/+page.svelte`

This plan preserves progress if the execution stack (background task, Supabase writer, or UI listener) crashes before job statuses are fully propagated.

## Objectives
- **Maintain Observability**: Ensure `research_jobs` rows reflect accurate state even after a crash.
- **Protect Partial Output**: Persist intermediate artifacts in `volumes/` and the reporting directory created by `ensure_reporting_directory_exists()`.
- **Enable Quick Recovery**: Provide exact restart and validation steps for the main flow and each subflow.

## Pre-Flight Checklist
- **Environment**: Confirm `.env` contains Supabase credentials (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`) and Alpha Vantage keys.
- **Dependencies**: Run `uv sync` if the environment was reset.
- **Database Access**: Verify Supabase connectivity via `uv run python -c "from src.lib.supabase_job_tracker import get_job_tracker; print(get_job_tracker().list_jobs(limit=1))"`.
- **Reporting Directory**: Ensure the path created by `src/tasks/common/reporting_directory_setup_task.py` exists (usually `volumes/logs/`).

## Crash Detection Signals
- **Background Task Traceback**: Inspect `server/api.py` logs (`uv run python server.py`) for unhandled exceptions in `run_research_background()`.
- **Supabase Row Stagnation**: `research_jobs.status` stuck at `running` with no new `metadata.steps` entries.
- **UI Silence**: `agent-ui/src/routes/+page.svelte` console shows no Realtime events after a subflow should have finished.
- **Partial Files**: Generated PDFs/markdown in report directories without corresponding Supabase updates.

## Immediate Stabilization Steps
1. **Freeze New Runs**: Temporarily disable the "Start Research" button in the UI (toggle feature flag or communicate to users).
2. **Capture Logs**: Export API logs and any CLI output for post-mortem.
3. **Snapshot Job Table**: In Supabase SQL editor, run `select * from research_jobs where main_job_id = '<affected-id>';` and save results.
4. **Check Cache Artifacts**: If using cache tasks (e.g., `historical_earnings_cache_retrieval_task`), ensure results are not partially written.

## Recovery Procedure
- **Step 1 – Identify Progress**
  - Query `metadata.steps` for the main job to see the last completed subflow.
  - Check subjob rows (`sub_job_id is not null`) for their `status` column.

- **Step 2 – Resume Flow**
  - If the failure happened in the background task:
    - Restart the FastAPI server: `uv run python server.py` (or redeploy container if using Docker Compose).
    - Re-trigger the flow with `uv run python run.py --symbol <SYMBOL>` (modify script to accept CLI args if necessary) while passing the existing `job_id` to `main_research_flow()` to avoid duplicate jobs. If reusing the job is impossible, create a new job and mark the old one `failed` via `get_job_tracker().update_job_status(old_id, JobStatus.FAILED, step="Superseded by rerun")`.

- **Step 3 – Manual Status Corrections**
  - For each completed subflow whose status remained `running`, call `update_job_status_task(existing_main_job_id, JobStatus.COMPLETED, "<flow> complete", "<flow>", symbol)` interactively (e.g., open a Python REPL via `uv run python`).
  - Ensure the main job receives a final `JobStatus.COMPLETED` or `JobStatus.FAILED` update with a descriptive `step` and (if completed) attach the `result` payload returned from the rerun.

- **Step 4 – Synchronize UI**
  - Once Supabase rows are corrected, confirm Realtime emits updates by watching the browser console. If not, instruct operators to reload the page and re-open the subscription.

## Validation Checklist
- **Supabase Data**: `research_jobs` contains one `main_flow` row with `status = 'completed'` or `'failed'`, and subjobs accurately reflect success/failure.
- **Result Artifacts**: Comprehensive report and key insights files exist and match the latest Supabase result metadata.
- **UI Consistency**: `agent-ui/src/routes/+page.svelte` shows subflow progress and final summary without reload loops.
- **Tests**: Execute `uv run pytest tests/unit/flows/test_research_flow.py -k main_research_flow_success` to confirm orchestration integrity.

## Post-Recovery Actions
- **Retrospective**: Document root cause and remediation in `docs/ai_todo_lists/` for future reference.
- **Add Monitoring**: Consider instrumenting `update_job_status_task()` to push alerts if a step remains `running` longer than expected.
- **Automation Idea**: Add a watchdog coroutine that periodically verifies Supabase status alignment while `main_research_flow()` runs.

## Future Hardening Ideas
- **Transactional Updates**: Wrap job status updates in retries/backoff to handle transient Supabase outages.
- **Heartbeats**: Emit heartbeat entries from `main_research_flow()` so the UI can detect stalls.
- **Idempotent Restart Hooks**: Expose an endpoint to resume at a specific subflow using cached artifacts, minimizing recomputation.
