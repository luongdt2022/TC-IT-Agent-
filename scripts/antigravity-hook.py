#!/usr/bin/env python3
"""
TC IT AGENT — ANTIGRAVITY LIFECYCLE HOOK ADAPTER
Chuẩn hóa giao tiếp JSON stdin/stdout cho .agents/hooks.json theo đặc tả Antigravity:
- PreToolUse (run_command): Chặn --no-verify, -n, core.hooksPath override qua block-no-verify.
- PreToolUse (write_file|edit_file): Kiểm tra Tier-1 Fact-Forcing trước khi cho phép sửa tệp lõi.
"""

import json
import os
import sys
import importlib.util
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def _load_module(name: str, filename: str):
    path = SCRIPT_DIR / filename
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def handle_pre_tool_use(payload: dict) -> dict:
    tool_call = payload.get("toolCall") or {}
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args") or {}
    cwd = payload.get("cwd") or str(SCRIPT_DIR.parent)

    # 1. Zero-Bypass Guard cho run_command
    if tool_name == "run_command":
        cmd_line = args.get("CommandLine", "")
        if cmd_line:
            bnv = _load_module("block_no_verify", "block-no-verify.py")
            is_violation, reason = bnv.scan_command_string(cmd_line)
            if is_violation:
                bnv.log_violation("HOOK_PRETOOLUSE", cmd_line, reason)
                return {
                    "decision": "deny",
                    "reason": f"[Zero-Bypass Guard] {reason}. Nghiêm cấm --no-verify hoặc vô hiệu hóa Git hooks."
                }
        return {"decision": "allow"}

    # 2. Fact-Forcing Guard cho write_file / edit_file trên tệp Tier-1
    if tool_name in ("write_file", "edit_file"):
        target_path = args.get("Path", "")
        if target_path:
            ffg = _load_module("fact_forcing_guard", "fact-forcing-guard.py")
            ffg.PROJECT_ROOT = os.path.abspath(cwd)
            ffg.FACTS_DIR = os.path.join(ffg.PROJECT_ROOT, ".facts")
            try:
                rel = os.path.relpath(target_path, ffg.PROJECT_ROOT)
            except ValueError:
                rel = target_path
            if ffg.is_tier_1_file(rel):
                valid, msg = ffg.verify_facts_for_file(rel)
                if not valid:
                    return {
                        "decision": "deny",
                        "reason": f"[Fact-Forcing Guard] Chặn sửa tệp lõi Tier-1 '{rel}'. {msg}"
                    }
        return {"decision": "allow"}

    return {"decision": "allow"}


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"decision": "allow"}))
        return

    try:
        payload = json.loads(raw)
    except Exception:
        print(json.dumps({"decision": "allow"}))
        return

    event = payload.get("hookEventName", "PreToolUse")
    if event == "PreToolUse":
        result = handle_pre_tool_use(payload)
    else:
        result = {}

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
