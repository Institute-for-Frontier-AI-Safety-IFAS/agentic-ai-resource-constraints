# Evaluation harness

Planned components:

- task loader
- agent configuration loader
- ToolSandbox wrapper/adapter
- resource-constraint injector
- run controller
- structured logger
- basic scorer
- run-manifest export

Requirements:

- same task can run under baseline and constrained conditions
- constraint parameters are configuration-driven
- model and agent versions are recorded for every run
- action traces and tool observations are logged where permitted
- apparatus-validation and main-study runs are separated
- secrets and credentials are excluded from logs and commits
