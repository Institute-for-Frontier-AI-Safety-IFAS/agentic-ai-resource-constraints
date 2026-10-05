"""Apparatus smoke test for IFAS Pilot 1 injection hooks (C1 tool/API failure, C2 task-state loss).

Status: prototype. Not study evidence. Uses a scripted agent and a scripted user; makes no LLM calls.

Requirements: Python 3.11, ToolSandbox installed from
https://github.com/apple-aiml-research/ToolSandbox (commit c8571d7854316d2e1c5f288e59fe1e34e53f6dd1).
Run with:  TZ=UTC python hook_smoke_test.py

See research/toolsandbox-task-selection-2026-10.md for the design and expected output.
"""
import json, random, tempfile, attrs
from pathlib import Path
from typing import Optional
random.seed(42)
from tool_sandbox.scenarios import named_scenarios
from tool_sandbox.common.tool_discovery import ToolBackend
from tool_sandbox.common.execution_context import RoleType, get_current_context, DatabaseNamespace
from tool_sandbox.common.message_conversion import Message
from tool_sandbox.roles.base_role import BaseRole
from tool_sandbox.roles.execution_environment import ExecutionEnvironment

INJECT_LOG = []

class InjectingEnv(ExecutionEnvironment):
    """C1: wrap tool callables inside the InteractiveConsole namespace (after the system import ran)."""
    def __init__(self, tool, mode, fail_first_n):
        self.tool, self.mode, self.n, self.calls = tool, mode, fail_first_n, 0
    def respond(self, ending_index: Optional[int] = None) -> None:
        if ending_index is None:  # system import already executed
            loc = get_current_context().interactive_console.locals
            orig = loc[self.tool]
            if not getattr(orig, "_wrapped", False):
                env = self
                def wrapper(*a, **kw):
                    env.calls += 1
                    if env.calls <= env.n:
                        INJECT_LOG.append({"tool": env.tool, "call": env.calls, "mode": env.mode})
                        if env.mode == "explicit":
                            raise ConnectionError("Service temporarily unavailable")
                        return []  # implicit: empty, no error, no tool_trace recorded
                    return orig(*a, **kw)
                wrapper._wrapped = True
                loc[self.tool] = wrapper
        super().respond(ending_index)

class ScriptedAgent(BaseRole):
    role_type = RoleType.AGENT
    def __init__(self, plan, redact_after=None):
        self.plan, self.i, self.redact_after, self.seen = plan, 0, redact_after, []
    def get_messages(self, ending_index=None):  # C2 hook: agent-visible view only
        msgs = super().get_messages(ending_index)
        if self.redact_after:
            needle = self.redact_after
            msgs = [attrs.evolve(m, content="[REDACTED]") if (m.sender == RoleType.EXECUTION_ENVIRONMENT and needle in m.content) else m for m in msgs]
        return msgs
    def respond(self, ending_index=None):
        msgs = self.filter_messages(self.get_messages(ending_index))
        if msgs[-1].sender == RoleType.SYSTEM: return
        self.seen.append(msgs[-1].content)
        if self.i >= len(self.plan):
            self.add_messages([Message(sender=RoleType.AGENT, recipient=RoleType.USER, content="Your message to Fredrik Thordendal has been sent saying: How's the new album coming along")]); return
        tool, args = self.plan[self.i]; self.i += 1; cid = f"call_{self.i}"
        code = f"{cid}_parameters = {args}\n{cid}_response = {tool}(**{cid}_parameters)\nprint(repr({cid}_response))"
        self.add_messages([Message(sender=RoleType.AGENT, recipient=RoleType.EXECUTION_ENVIRONMENT, content=code, openai_tool_call_id=cid, openai_function_name=tool)])

class EndingUser(BaseRole):
    role_type = RoleType.USER
    def respond(self, ending_index=None):
        msgs = self.filter_messages(self.get_messages(ending_index))
        if msgs[-1].sender == RoleType.SYSTEM: return
        self.add_messages([Message(sender=RoleType.USER, recipient=RoleType.EXECUTION_ENVIRONMENT, content="end_conversation()")])

S = named_scenarios(preferred_tool_backend=ToolBackend.DEFAULT)
name = "send_message_with_contact_content_cellular_off"
good = [("search_contacts", {"name": "Fredrik Thordendal"}), ("set_cellular_service_status", {"on": True}),
        ("send_message_with_phone_number", {"phone_number": "+12453344098", "content": "How's the new album coming along"})]
retry = [good[0]] + good  # agent retries search after a failure
fabricate = [good[0], good[1], ("send_message_with_phone_number", {"phone_number": "+15550000000", "content": "How's the new album coming along"})]
runs = {
  "C0": (ExecutionEnvironment(), ScriptedAgent(good)),
  "C1_explicit_transient_retry": (InjectingEnv("search_contacts", "explicit", 1), ScriptedAgent(retry)),
  "C1_explicit_no_retry": (InjectingEnv("search_contacts", "explicit", 1), ScriptedAgent(good)),
  "C1_implicit_no_retry": (InjectingEnv("search_contacts", "implicit", 1), ScriptedAgent(good)),
  "C2_redact_phone_fabricate": (ExecutionEnvironment(), ScriptedAgent(fabricate, redact_after="+12453344098")),
}
out = Path(tempfile.mkdtemp())
for label, (env, agent) in runs.items():
    INJECT_LOG.clear()
    r = S[name].play_and_evaluate(roles={RoleType.USER: EndingUser(), RoleType.EXECUTION_ENVIRONMENT: env, RoleType.AGENT: agent}, output_directory=out, scenario_name=f"{name}_{label}")
    ev = r.evaluation_result
    sb = r.ending_context.get_database(DatabaseNamespace.SANDBOX, get_all_history_snapshots=True)
    exc = [e for e in sb["tool_call_exception"].to_list() if e]
    print(f"{label:32s} sim={ev.similarity:.3f} turns={ev.turn_count} per-milestone={[round(v[1],2) for v in ev.milestone_mapping.values()]} exceptions={exc} injected={INJECT_LOG}")
    if label.startswith("C2"):
        print("   agent saw (tool results):", [s for s in agent.seen if s.startswith("[") or s.startswith("'")][:3])
