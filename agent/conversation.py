"""Manual agentic loop with a human-in-the-loop save gate (Spec 2 §3, §6).

Session.send(text) runs the tool loop until the model finishes OR wants to call
save_quote. save_quote pauses the loop and returns state 'awaiting_save_approval';
the caller (cli.py or web) collects the sales user's y/n and calls approve_save().
Reusable as the web backend (Spec 3) — no CLI dependency here.
"""
from __future__ import annotations

import json
import os

from .prompts import SYSTEM_PROMPT
from .tools import TOOL_DEFS, execute_tool

DEFAULT_MODEL = os.environ.get("AGENT_MODEL", "claude-sonnet-4-6")  # Spec 2 §3.1
MAX_TOKENS = 16000


class Session:
    def __init__(self, client=None, model: str = DEFAULT_MODEL, effort: str = "medium"):
        if client is None:
            import anthropic
            client = anthropic.Anthropic()  # ANTHROPIC_API_KEY from env
        self.client = client
        self.model = model
        self.effort = effort
        self.messages: list[dict] = []
        self._pending: dict | None = None  # set while awaiting save approval

    # -- public API ---------------------------------------------------------
    def send(self, text: str) -> dict:
        if self._pending is not None:
            return {"state": "awaiting_save_approval",
                    "text": "Đang chờ bạn duyệt lưu báo giá (approve_save).",
                    "pending_save": self._pending["save_args"]}
        self.messages.append({"role": "user", "content": text})
        return self._loop()

    def approve_save(self, approved: bool) -> dict:
        if self._pending is None:
            return {"state": "error", "text": "Không có báo giá nào đang chờ duyệt."}
        pending = self._pending
        self._pending = None
        results = []
        for tu_id, name, args, precomputed in pending["calls"]:
            res = precomputed if precomputed is not None else \
                execute_tool(name, args, approved=approved)
            results.append({"type": "tool_result", "tool_use_id": tu_id,
                            "content": json.dumps(res, ensure_ascii=False)})
        self.messages.append({"role": "user", "content": results})
        return self._loop()

    # -- internal loop ------------------------------------------------------
    def _create(self):
        return self.client.messages.create(
            model=self.model, max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT, tools=TOOL_DEFS, messages=self.messages,
            thinking={"type": "adaptive"},
            output_config={"effort": self.effort},
        )

    def _loop(self) -> dict:
        while True:
            resp = self._create()
            # preserve full content (incl. thinking) for multi-turn correctness
            self.messages.append({"role": "assistant", "content": resp.content})

            if resp.stop_reason != "tool_use":
                return {"state": "done", "text": _text(resp.content)}

            tool_uses = [b for b in resp.content if b.type == "tool_use"]
            calls, results = [], []
            has_save = False
            for tu in tool_uses:
                if tu.name == "save_quote":
                    has_save = True
                    calls.append((tu.id, tu.name, dict(tu.input), None))  # defer
                else:
                    res = execute_tool(tu.name, dict(tu.input))
                    calls.append((tu.id, tu.name, dict(tu.input), res))
                    results.append({"type": "tool_result", "tool_use_id": tu.id,
                                    "content": json.dumps(res, ensure_ascii=False)})

            if has_save:
                save_args = next(dict(tu.input) for tu in tool_uses
                                 if tu.name == "save_quote")
                self._pending = {"calls": calls, "save_args": save_args}
                return {"state": "awaiting_save_approval",
                        "text": _text(resp.content), "pending_save": save_args}

            self.messages.append({"role": "user", "content": results})


def _text(content) -> str:
    return "\n".join(b.text for b in content if getattr(b, "type", None) == "text").strip()
