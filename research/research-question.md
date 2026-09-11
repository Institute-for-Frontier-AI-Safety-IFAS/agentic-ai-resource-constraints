# Research question and scope

## Umbrella research question

How do limits in inference budget, connectivity, memory, tool access, and human oversight affect the safety behaviour and task performance of LLM-based agentic AI systems?

## Candidate Pilot 1 question

> How do controlled tool/API failures and task-state loss affect error recovery, state consistency, unsupported assumptions, repeated actions, and task performance in LLM-based agents?

## Study aim

Measure how selected operating constraints change observable agent behaviour relative to a baseline condition while holding task, model, framework, prompt, scoring rules, and other environment settings fixed where possible.

## Unit of analysis

One agent run on a defined task under a defined operating condition.

Each run should record:
- model/version
- agent framework/version
- prompts
- task ID
- condition
- tool availability and injected failures
- context/state settings
- action trace
- tool calls/responses
- environment observations
- final task outcome
- runtime and step count

## Candidate dependent variables

1. Task completion
2. Invalid or failed actions
3. Recovery after failure
4. Repeated actions and loops
5. State consistency
6. Unsupported assumptions after failed or missing observations
7. Steps and time to completion
8. Clarification or escalation behaviour where supported

## Pilot 1 environment

ToolSandbox is selected.

The next task is to select a small ToolSandbox subset with multi-step state dependency, necessary tool use, objective scoring, injectable failure points, and manageable cost.

## Provisional Pilot 1 hypotheses

**P1-H1.** Controlled tool/API failures will reduce task completion and increase recovery attempts relative to baseline.

**P1-H2.** Implicit or ambiguous tool failures will produce more unsupported assumptions and repeated actions than explicit tool errors.

**P1-H3.** Controlled loss of previously observed task state will increase state inconsistency and repeated attempts relative to baseline.

**P1-H4.** Agents will differ in their tendency to recognise missing information and seek recovery or clarification rather than continuing as if the missing state were known.

## Deferred from Pilot 1

- human oversight
- independent connectivity construct where equivalent to API/tool failure
- broad action/inference budget manipulation unless operationalised non-mechanically

## Status

The focused literature review is complete enough to support pilot selection. ToolSandbox is selected. Protocol v0.1 remains a design draft until task subset, exact treatments, model configurations, repeat count, and final measures are selected.
