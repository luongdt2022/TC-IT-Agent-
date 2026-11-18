#!/usr/bin/env python3
"""
TC IT AGENT FRAMEWORK v4.0 — SELF-INTEGRITY TEST SUITE
Kiểm định tự động cấu trúc Subagents, Hooks, Core Skills, Loop Engine, DAG & Server Security.
"""

import os
import re
import sys
import json
import pathlib
import tempfile
import unittest
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _load_mod(name: str, rel_path: str):
    path = ROOT / rel_path
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestSubagentsAndHooks(unittest.TestCase):
    EXPECTED_AGENTS = {"ps", "po-pm", "ba", "sa", "dev", "qc", "qa"}

    def test_canonical_subagents_exist_and_valid(self):
        agents_dir = ROOT / ".agents" / "agents"
        self.assertTrue(agents_dir.is_dir())
        found = {p.stem for p in agents_dir.glob("*.md")}
        self.assertEqual(found, self.EXPECTED_AGENTS)

        for p in agents_dir.glob("*.md"):
            raw = p.read_bytes()
            self.assertNotIn(b"\r", raw, f"Corrupted CR in {p.name}")
            txt = raw.decode("utf-8")
            m = re.match(r"^---\s*\n(.*?)\n---", txt, re.DOTALL)
            self.assertIsNotNone(m, f"Missing YAML frontmatter in {p.name}")
            fm = m.group(1)
            self.assertIn(f"name: {p.stem}", fm)
            self.assertIn('model: "inherit"', fm)
            self.assertNotIn("view_file", fm)
            self.assertNotIn("write_to_file", fm)
            self.assertNotIn("replace_file_content", fm)

    def test_hooks_json_and_adapter(self):
        hooks_file = ROOT / ".agents" / "hooks.json"
        self.assertTrue(hooks_file.is_file())
        data = json.loads(hooks_file.read_text(encoding="utf-8"))
        self.assertIn("zero-bypass-guard", data)
        self.assertIn("fact-forcing-tier1-guard", data)

        hook_mod = _load_mod("antigravity_hook", "scripts/antigravity-hook.py")
        res_deny = hook_mod.handle_pre_tool_use({
            "hookEventName": "PreToolUse",
            "cwd": str(ROOT),
            "toolCall": {"name": "run_command", "args": {"CommandLine": "git commit --no-verify -m test"}}
        })
        self.assertEqual(res_deny["decision"], "deny")

        res_allow = hook_mod.handle_pre_tool_use({
            "hookEventName": "PreToolUse",
            "cwd": str(ROOT),
            "toolCall": {"name": "run_command", "args": {"CommandLine": "git status"}}
        })
        self.assertEqual(res_allow["decision"], "allow")


class TestCoreSkillsIntegrity(unittest.TestCase):
    def test_core_skills_no_duplicates_and_no_leaks(self):
        skills_dir = ROOT / "skills"
        dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        self.assertGreaterEqual(len(dirs), 50)
        self.assertLessEqual(len(dirs), 60)

        seen = set()
        leak_re = re.compile(r"(nacen-|NacenTech|NacenTwin|TracePro|XUAT_MAN_HINH_WEB_HTML)", re.I)
        for d in dirs:
            sk = d / "SKILL.md"
            self.assertTrue(sk.is_file(), f"Missing SKILL.md in {d.name}")
            txt = sk.read_text(encoding="utf-8")
            m = re.match(r"^---\s*\n(.*?)\n---", txt, re.DOTALL)
            self.assertIsNotNone(m, f"Missing frontmatter in {d.name}")
            nm = re.search(r'^name:\s*["\']?([^"\'\n]+)["\']?', m.group(1), re.MULTILINE)
            self.assertIsNotNone(nm, f"Missing name in {d.name}")
            self.assertEqual(nm.group(1).strip(), d.name)
            self.assertNotIn(d.name, seen)
            seen.add(d.name)
            self.assertIsNone(leak_re.search(txt), f"Customer leak in {d.name}/SKILL.md")


class TestEngineAndDashboard(unittest.TestCase):
    def test_tc_loop_has_record_telemetry_and_waiter(self):
        tc_loop = _load_mod("tc_loop", "engine/tc-loop.py")
        self.assertTrue(hasattr(tc_loop.LoopEngine, "record_telemetry"))
        self.assertTrue(hasattr(tc_loop.LoopEngine, "_wait_antigravity_conversation"))
        self.assertTrue(hasattr(tc_loop.LoopEngine, "ensure_isolation_branch"))

    def test_dag_engine_supports_epic_and_deps(self):
        sys.path.insert(0, str(ROOT / "dashboard" / "core"))
        dag_mod = _load_mod("dag_engine", "dashboard/core/dag_engine.py")
        with tempfile.TemporaryDirectory() as td:
            troot = pathlib.Path(td)
            epic_dir = troot / "specs" / "EPIC-01_AUTH"
            epic_dir.mkdir(parents=True)
            (epic_dir / "tasks.md").write_text(
                "## Phase 1\n- [x] `T-01` [BE] Init auth\n- [ ] `T-02` [FE] Login UI (Depends on: T-01)\n",
                encoding="utf-8"
            )
            eng = dag_mod.DAGEngine(root_dir=troot)
            data = eng.export_graph_data()
            self.assertEqual(data["total_tasks"], 2)
            nodes = {n["id"]: n for n in data["nodes"]}
            self.assertEqual(nodes["EPIC-01-01"]["status"], "DONE")
            self.assertEqual(nodes["EPIC-01-02"]["status"], "READY")
            self.assertIn("EPIC-01-01", nodes["EPIC-01-02"]["dependencies"])

    def test_public_portal_blocks_admin(self):
        os.environ["TC_PUBLIC_PORTAL"] = "1"
        try:
            sys.path.insert(0, str(ROOT / "dashboard" / "core"))
            srv = _load_mod("dash_server", "dashboard/api/server.py")
            from fastapi import HTTPException
            from starlette.requests import Request
            req = Request({"type": "http", "headers": [], "client": ("127.0.0.1", 1234)})
            with self.assertRaises(HTTPException) as ctx:
                srv.require_admin(req, x_tc_admin_token=srv.ADMIN_TOKEN)
            self.assertEqual(ctx.exception.status_code, 403)
        finally:
            os.environ.pop("TC_PUBLIC_PORTAL", None)


if __name__ == "__main__":
    unittest.main()
