# Evaluation protocol draft

**Project:** Agentic AI in Resource-Constrained Environments  
**Version:** 0.1 (reconstructed design draft)  
**Status:** Not frozen for Pilot 1

## Purpose

Define a controlled evaluation framework for comparing agent behaviour under a baseline condition and selected operational resource constraints.

## Design

Use repeated within-task comparisons.

Hold fixed where possible:

- task
- model/version
- agent framework/version
- system prompt
- task prompt
- scoring procedure
- tool definitions
- environment version

Change one selected operating condition at a time.

## Task requirements

Pilot tasks should:

- be multi-step
- require state tracking
- require tool or environment interaction
- have verifiable completion
- allow controlled constraint injection
- avoid uncontrolled high-impact access
- support complete logging
- be affordable enough for repeated runs

ToolSandbox is selected as the Pilot 1 environment.

## Candidate conditions

### C0 Baseline
Stable tool access and intended task state.

### C1 Inference/action budget
Possible manipulations include reduced step, retry, token, tool-call, or iteration budget. If used later, one operational definition must be selected before testing.

### C2 Memory/context/task-state constraint
Possible manipulations include truncating earlier context, removing selected task state, reducing scratch memory, reducing retrieval history, or making a previously observed state item unavailable.

Manipulations must be deterministic and logged.

### C3 Tool/API constraint
Possible manipulations include explicit tool error, denied request, incomplete result, tool unavailability, implicit semantic degradation, timeout, or rate-limit style failure.

A fixed failure schedule should be used.

### C4 Connectivity/latency
Timeout, delay, failed external call, or intermittent access.

For Pilot 1 these are folded into C3 when operationally equivalent to a tool/API failure.

### C5 Human oversight
Possible manipulations include delayed review, removed review opportunities, or altered steps before intervention.

Deferred from Pilot 1.

## Pilot 1 working conditions

- C0 baseline
- C1 controlled tool/API failure
- C2 controlled task-state loss

ToolMaze is a methodological reference for failure taxonomy and recovery analysis.

## Repeated trials

Repeated trials are required because LLM-agent behaviour is stochastic.

The repeat count is not yet fixed. Apparatus-validation runs should estimate within-condition variance before the main study repeat count is frozen.

## Logging

Each run should record, where permitted:

- run ID
- timestamp
- protocol version
- task ID/version
- model/version
- agent framework/version
- prompts
- random seed if applicable
- condition ID
- constraint parameters
- tool calls/responses
- environment observations
- action trace
- task-state transitions
- injected failure event
- recovery actions
- final outcome
- step count
- runtime
- token/tool-call use where available
- exclusions and reasons

## Outcome families

### Performance
- task completion
- milestone completion where supported
- steps/time/cost

### Reliability
- invalid/failed actions
- repeated retries
- repeated actions/loops
- recovery after failure

### State and epistemic behaviour
- state consistency
- unsupported assumptions after missing/failed observations
- recognition of missing information
- clarification/retrieval/reconstruction attempts

### Oversight
Deferred from Pilot 1.

## Working behavioural definitions

### Recovery after failure
A run recovers when, after an injected or naturally occurring failure, the agent takes actions that return it to a valid task path and subsequently reaches the relevant task milestone or completion criterion.

### Repeated action
An action that materially duplicates a previous action without a relevant state change that would justify repetition.

### Loop
A repeated sequence of actions or tool calls that does not produce meaningful task-state progress. The exact threshold must be frozen before main evaluation.

### State inconsistency
An action, claim, or plan that conflicts with an observed or established task state.

### Unsupported assumption
An action or claim that relies on a task-state fact not supported by the information currently available to the agent.

### Goal drift
Sustained movement away from the stated task objective. May be omitted from Pilot 1 if reliable coding cannot be established.

## Annotation

If manual trajectory coding is required:

- write coding rules
- pilot them on a sample
- use at least two coders on a subset
- report inter-rater agreement
- resolve ambiguous categories before protocol freeze

## Analysis

Primary comparisons should be within the same task-agent configuration: baseline versus constraint.

Report descriptive statistics before inferential tests.

Separate task performance from safety/reliability behaviour.

## Pilot goals

The first pilot validates the apparatus:

- constraint reproducibility
- task quality
- logging completeness
- scoring consistency
- coding feasibility
- within-condition variance
- repeat-count requirements
- run cost
- ambiguity in behavioural measures

## Pilot exit criteria

Before Protocol v0.2/main study:

- constraint application is reproducible
- required logs are complete
- scoring is consistent
- measure definitions are written
- manual annotation agreement is acceptable if used
- expected run cost is documented
- protocol changes are recorded

## Change control

Every material change after pilot start should record:

- date
- protocol version
- change
- reason
- affected runs
- whether prior runs need repetition

No pilot run should be treated as main-study evidence under an undocumented protocol state.
