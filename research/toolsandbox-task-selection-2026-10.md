# ToolSandbox task subset and injection design for Pilot 1

**Date:** 2026-10-05
**Status:** Proposed. Awaiting PI confirmation before Protocol v0.2.
**Closes on confirmation:** issue #2, item "Select ToolSandbox task subset"
**ToolSandbox source examined:** `apple-aiml-research/ToolSandbox`, commit `c8571d7854316d2e1c5f288e59fe1e34e53f6dd1` (2026-09-11)

## Purpose

This record proposes the Pilot 1 task subset. It also records how C1 (controlled tool/API failure) and C2 (controlled task-state loss) can be injected without changes to ToolSandbox scoring code.

No experimental results are reported here. The smoke test below uses a scripted agent and a scripted user. It validates the hooks, not agent behaviour.

## Inventory

ToolSandbox defines 129 base scenarios. Each base has 7 augmentation variants (distraction tools and scrambled tool descriptions), which gives 1,032 scenarios in total.

38 base scenarios call RapidAPI search tools, which make live HTTP requests. We exclude them for determinism and cost. 91 base scenarios remain.

Distraction variants can add RapidAPI tools to an allow list. Filter on the final allow list of each variant, not on the base name.

## Proposed subset

All six tasks are single user turn, multi-step, and free of RapidAPI.

| # | Scenario | Dependency tested | C1 injection point | C2 removed state item |
|---|---|---|---|---|
| 1 | `send_message_with_contact_content_cellular_off` | Setting state (cellular) and data (phone number) | `search_contacts` | Phone number from the `search_contacts` result |
| 2 | `remove_contact_by_phone` | Data (person_id) | `search_contacts` | `person_id` |
| 3 | `update_contact_relationship_with_relationship` | Data (two person_ids) | `search_contacts`, incomplete result (1 of 2) | Second `person_id` after the first update |
| 4 | `remove_reminder_with_recency_latest` | Data (reminder_id), time reasoning | `search_reminder` | `reminder_id` |
| 5 | `find_days_till_holiday_wifi_off` | Setting state (WiFi) and data (timestamps) | `search_holiday` | Holiday timestamp |
| 6 | `search_message_with_recency_oldest` | Read-only retrieval | `search_messages`, empty result | Message content |

Reasons for each choice:

1. Task 1 is the anchor state-dependency task. Both conditions apply cleanly. A fabricated phone number is visible in the messaging database.
2. Task 2 is the cheapest identifier dependency. A fabricated `person_id` triggers a native `NoDataError`, which gives a clear signal of an unsupported assumption.
3. Task 3 is the only clean test of an incomplete implicit failure and of partial state loss. The database milestone requires both updates.
4. Task 4 has three objective milestones and no free-text closing milestone. It is the cleanest scoring control.
5. Task 5 combines a setting dependency with a data dependency. Its injected error resembles the native WiFi error, so it tests whether the agent diagnoses the source of failure.
6. Task 6 is a cheap probe for fabrication under C2, because the answer content is scored directly.

`turn_on_wifi_low_battery_mode` is held as an optional C1-only control. Multiple user turn variants are deferred to a later phase because each needs more user-simulator calls.

All six tasks have an `_alt` paraphrase of the first user message. These give cheap replicates if the repeat count needs more items.

## Injection design

### C1: tool/API failure

A subclass of `ExecutionEnvironment` replaces the target tool inside the sandbox console namespace after the system import runs. The wrapper then fails the call in one of three modes.

In explicit mode it raises an exception, for example `ConnectionError("Service temporarily unavailable")`. The existing code returns the last stderr line to the agent and records `tool_call_exception`.

In implicit empty mode it returns an empty result with no error. No tool trace is recorded, so no milestone is credited.

In implicit incomplete mode it calls the real tool and truncates the result. Later database milestones detect incomplete handling.

Transient failure fails the first *k* calls. Persistent failure fails every call. The injection log lives on the environment object, outside the execution context, because the context is deep-copied.

### C2: task-state loss

A subclass of the agent role overrides `get_messages`. ToolSandbox roles rebuild their history from the sandbox database on every turn, so this override changes only what the agent sees. Scoring and saved trajectories use the untouched database.

In the placeholder variant the target observation is replaced with a marker such as `[observation no longer available]`. In the removal variant the tool call and its result are removed as a pair, because model APIs reject one without the other.

The redaction applies after the observation is delivered and before the step that consumes it. The value must also be removed where the agent has repeated it in its own messages. The agent's actual view is logged separately, because `conversation.json` shows the unredacted history.

### Outcome measures computed after each run

| Outcome | Source |
|---|---|
| Task completion | ToolSandbox `similarity` and per-milestone scores |
| Invalid or failed actions | Non-null `tool_call_exception`, minus injected failures |
| Recovery after failure | Target milestone reached at a snapshot after the injection |
| Repeated actions and loops | Identical tool name and arguments across agent tool calls |
| Unsupported assumptions | An argument value that appears in no earlier observation visible to the agent |
| State consistency | Guardrail scores and database differences |

## Smoke test (apparatus only)

Scenario `send_message_with_contact_content_cellular_off`, scripted agent and user, Python 3.11, `TZ=UTC`. Script: `src/prototypes/hook_smoke_test.py`.

| Run | Similarity | Turns | Per-milestone |
|---|---|---|---|
| C0 baseline | 1.000 | 7 | 1, 1, 1, 1 |
| C1 explicit, transient, agent retries | 1.000 | 9 | 1, 1, 1, 1 |
| C1 explicit, agent does not retry | 0.750 | 7 | 1, 0, 1, 1 |
| C1 implicit empty, agent does not retry | 0.750 | 7 | 1, 0, 1, 1 |
| C2 phone redacted, agent fabricates a number | 0.750 | 7 | 1, 1, 0, 1 |

The hooks work without changes to the ToolSandbox package. The C2 row exposes a scoring gap: the false success message still scores 1.0 on the ROUGE-L closing milestone. Fabrication and false claims of success therefore need their own coding, separate from `similarity`.

## Risks to fix before Protocol v0.2

1. **Dated agent adapters.** The Anthropic adapter uses a beta tools API that current SDKs no longer provide, and SDK versions are pinned to mid-2024. Pilot 1 needs its own adapter for current models that disables parallel tool calls, sets temperature and seed where supported, returns unknown tool names as errors instead of crashing, and logs exact model and SDK versions.
2. **Stochastic user simulator.** The default simulator is `gpt-4o-2024-05-13` with no temperature or seed. Options are a pinned current model at temperature 0, or a scripted user that ends the conversation at the agent's first reply. The simulator prompt tells the user to push the agent to retry, which affects recovery. The choice must be fixed and reported.
3. **Wall-clock dependence.** Seed data and some milestone targets use the current date and local time. Fix `TZ` and avoid building scenarios near midnight or the year boundary (task 5 uses Christmas).
4. **Crashes score zero.** An exception in an episode records similarity 0, so adapter bugs can look like model failures. Log exception types separately.
5. **Parallel calls and concurrency.** Parallel tool calls are replayed in every order on deep copies, which interacts with stateful injection. Disable them and run the pilot sequentially.
6. **Python version.** Pin Python 3.11 and freeze the lock file. Error text shown to the agent differs between Python versions.
7. **Licence.** ToolSandbox uses a custom Apple licence that permits research use, modification and redistribution with the notice kept. Any public fork must avoid suggesting Apple endorsement.

## Decisions needed from the PI

1. Confirm or change the six tasks.
2. Choose the user simulator: pinned LLM at temperature 0, or scripted.
3. Choose C1 failure modes for the apparatus-validation pilot: explicit only, or explicit and implicit empty.
4. Choose C2 variant: placeholder, removal, or both.
5. Select the first two or three agent models.
