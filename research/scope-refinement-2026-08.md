# Scope refinement after focused literature review

**Date:** 2026-08-14  
**Status:** Research-design decision record

## Why this note exists

The project began with a broad question about inference budget, connectivity, memory, tool access, and human oversight. The literature review identified substantial prior work across several parts of this space.

This note records a literature-driven scope refinement.

## What changed

### Tool/API failure
Prior work already studies controlled tool and API failure. Generic fault injection alone is not a defensible novelty claim.

### Memory/context/task state
The more useful question is how agents behave when previously observed task-relevant state becomes unavailable, inaccessible, or stale during execution.

### Inference/action budget
Budget-aware work already exists. A later study may examine skipped verification, unsupported assumptions, retries, or premature stopping under pressure.

### Human oversight
Deferred because reviewer workload, timing, intervention policy, and trace presentation add additional variance.

## Revised Pilot 1 direction

1. Controlled tool/API failure as a reference constraint.
2. Controlled task-state loss as the main second constraint.
3. Action/tool-call budget retained for possible later study.

Connectivity is folded into tool/API reliability where operationally equivalent.

## Environment decision

ToolSandbox is selected as the Pilot 1 environment because it supports stateful tool execution, intermediate state dependencies, executable evaluation, and controlled multi-step interaction.

ToolMaze remains a methodological reference for failure injection and recovery analysis.

The tau-bench family is deferred as a possible later replication/generalisation environment.

## Defensible contribution under investigation

The project does not claim that resource constraints in agents are generally unstudied.

The narrower contribution under investigation is a common controlled comparison of distinct operational constraint classes within the same tasks and agent configurations using shared trajectory-level measures.

A stronger novelty claim should wait until final source checking.
