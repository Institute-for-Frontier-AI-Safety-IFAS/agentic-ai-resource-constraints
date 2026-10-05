# Agentic AI in Resource-Constrained Environments

**Institute for Frontier AI Safety (IFAS)**

This repository contains research materials for an IFAS study on how operational resource constraints affect the behaviour and safety of LLM-based agentic AI systems.

**Project page:** https://ifasresearch.org/projects/agentic-ai-resource-constraints/  
**Repository:** https://github.com/Institute-for-Frontier-AI-Safety-IFAS/agentic-ai-resource-constraints

**Status:** Active research design

## Umbrella research question

How do limits in inference budget, connectivity, memory, tool access, and human oversight affect the safety behaviour and task performance of LLM-based agentic AI systems?

## Candidate Pilot 1 question

> How do controlled tool/API failures and task-state loss affect error recovery, state consistency, unsupported assumptions, repeated actions, and task performance in LLM-based agents?

The Pilot 1 task environment is **ToolSandbox**.

## Why this study

Recent work already studies important parts of the resource-constraint problem, including tool/API failures, dynamic replanning, agent memory, long-context behaviour, and explicit resource budgets.

This project therefore does not claim that resource constraints in LLM agents are unstudied.

The narrower contribution under investigation is whether distinct operational constraint classes can be compared within common tasks and agent configurations using the same trajectory-level measures, especially recovery, state consistency, unsupported assumptions, repeated actions, and task performance.

## Pilot 1 direction

1. **C0 Baseline:** stable tools and intended task state.
2. **C1 Controlled tool/API failure:** a reference constraint informed by prior failure-recovery work.
3. **C2 Controlled task-state loss:** removal or unavailability of previously observed task-relevant information during execution.

Human oversight is deferred from Pilot 1. Connectivity is represented under tool/API reliability when the manipulation is operationally a timeout, delay, or failed external call.

## Pilot environment

**ToolSandbox** is selected as the Pilot 1 task environment.

**ToolMaze** is retained as a methodological reference for tool-failure injection and recovery analysis.

The **tau-bench family** remains a possible later replication/generalisation environment.

## Candidate outcomes

- task completion
- invalid or failed actions
- recovery after failure
- repeated actions and loops
- state consistency
- unsupported assumptions after failed or missing observations
- steps and time to completion
- clarification or escalation behaviour where supported by the task

## Current work

- [x] Define the initial research question
- [x] Define candidate constraint classes
- [x] State working hypotheses
- [x] Complete focused literature review for pilot design
- [x] Record literature-driven scope refinement
- [x] Select ToolSandbox as the Pilot 1 task environment
- [ ] Select ToolSandbox task subset (proposed 2026-10-05; see `research/toolsandbox-task-selection-2026-10.md`)
- [ ] Fix final Pilot 1 constraints and exact treatment levels
- [ ] Select initial model and agent configurations
- [ ] Estimate repeat count and pilot API/compute cost
- [ ] Freeze pilot task design and measures
- [ ] Update and freeze Protocol v0.2
- [ ] Implement evaluation harness (injection hooks prototyped; see `src/prototypes/`)
- [ ] Run apparatus-validation pilot
- [ ] Run main evaluation
- [ ] Analyse results
- [ ] Prepare public outputs

There are currently no experimental results.

## Repository history

The original GitHub repository became unavailable in September 2026. This repository restores its content from preserved IFAS records. See [RECOVERY_NOTE.md](RECOVERY_NOTE.md).

## Licence

MIT. See [LICENSE](LICENSE). Cite this work as described in [CITATION.cff](CITATION.cff).
