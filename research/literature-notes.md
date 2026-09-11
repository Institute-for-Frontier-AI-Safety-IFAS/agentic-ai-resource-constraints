# Literature notes

This file records the focused literature review used to refine Pilot 1. It is a working research-design note, not a completed systematic review.

## Review questions

1. How are LLM agents evaluated on multi-step tasks?
2. What happens when tools or APIs fail?
3. What is known about memory, context, and task-state limitations?
4. How are inference, action, tool-call, and other budgets operationalised?
5. What trajectory-level measures capture recovery and reliability?
6. How should human oversight be represented?
7. Which environments support controlled, repeatable constraint injection?
8. Has prior work already compared several distinct resource classes under one common within-task framework?

## Emerging design conclusions

### Task success is not enough
Full trajectories matter because identical final outcomes can hide different failure paths.

### Tool/API failure is already an active research area
This remains useful as a reference condition, but cannot by itself support a broad novelty claim.

### Task-state loss is narrower than generic memory evaluation
The Pilot 1 question is what happens after task-relevant state that was previously available becomes unavailable or unreliable during execution.

### Budget constraints need precise operational definitions
A hard step cutoff can mechanically reduce completion, so budget pressure is deferred unless operationalised more carefully.

### Human oversight is not a simple scalar variable
Reviewer workload, timing, intervention policy, and trace presentation add variance. It is deferred from Pilot 1.

### ToolSandbox best fits Pilot 1
It provides stateful tool interaction, intermediate dependencies, executable evaluation, and controlled intervention points.

## High-priority sources

- Liu et al. (2023). *AgentBench: Evaluating LLMs as Agents*. https://arxiv.org/abs/2308.03688
- Mialon et al. (2023). *GAIA: a benchmark for General AI Assistants*. https://arxiv.org/abs/2311.12983
- Ruan et al. (2024). *Identifying the Risks of LM Agents with an LM-Emulated Sandbox*. https://arxiv.org/abs/2309.15817
- Zhang et al. (2024). *Agent-SafetyBench: Evaluating the Safety of LLM Agents*. https://arxiv.org/abs/2412.14470
- Jimenez et al. (2023). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* https://arxiv.org/abs/2310.06770
- Tang et al. (2025). *LM Agents May Fail to Act on Their Own Risk Knowledge*. https://arxiv.org/abs/2508.13465
- Gupta (2026). *ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress Conditions*. https://arxiv.org/abs/2601.06112
- Zhu et al. (2026). *When Tools Fail: Benchmarking Dynamic Replanning and Anomaly Recovery in LLM Agents*. https://arxiv.org/abs/2606.05806
- Hu, Wang, & McAuley (2025). *Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions*. https://arxiv.org/abs/2507.05257
- Li et al. (2026). *Benchmark Test-Time Scaling of General LLM Agents*. https://arxiv.org/abs/2602.18998
- Liu et al. (2025). *Budget-Aware Tool-Use Enables Effective Agent Scaling*. https://arxiv.org/abs/2511.17006
- Lu et al. (2024). *ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities*. https://arxiv.org/abs/2408.04682
- Yao et al. (2024). *tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains*. https://arxiv.org/abs/2406.12045

## Pilot implications

Selected environment: **ToolSandbox**

Core conditions:
- C0 baseline
- C1 controlled tool/API failure
- C2 controlled task-state loss

Methodological reference:
- ToolMaze for explicit/implicit and transient/persistent failure distinctions.

Deferred:
- human oversight
- independent connectivity construct
- action/tool-call budget unless operationalised non-mechanically

## Open questions before Protocol v0.2

- Which ToolSandbox tasks have the strongest state dependency?
- Can state loss be injected without changing the task objective?
- Which tasks support objectively identifying unsupported state assumptions?
- What recovery metrics can be automated?
- Should C1 include one or two failure types in the apparatus-validation pilot?
- What repeat count is required to separate treatment effects from stochastic variation?
- What exact cross-constraint novelty claim remains defensible after final source checking?
