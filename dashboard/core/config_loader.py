#!/usr/bin/env python3
"""
TC IT AGENT — UNIFIED PROJECT CONFIG LOADER
Đọc cấu hình chuẩn từ engine/policy.toml để loại bỏ hoàn toàn hardcode đường dẫn.
"""

from pathlib import Path
from typing import Dict, Any, List

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None


def find_root_dir() -> Path:
    current = Path(__file__).resolve().parent
    for p in [current, *current.parents]:
        if (p / "engine" / "policy.toml").exists() or (p / ".git").exists() or (p / "AGENTS.md").exists():
            return p
    return current.parent.parent


def load_project_policy(root_dir: Path | None = None) -> Dict[str, Any]:
    root = root_dir or find_root_dir()
    policy: Dict[str, Any] = {
        "project": {
            "name": "TC IT Enterprise Project",
            "docs_dir": "docs",
            "wireframes_dir": "docs/wireframes",
            "src_dir": "src",
            "frontend_dir": "src/WebApp",
            "backend_dir": "src",
            "tests_dir": "tests",
        },
        "loop": {
            "task_specs_dir": "specs",
            "backlog_file": "backlog/BACKLOG.md",
            "basic_design_dir": "docs/01-basic-design",
            "state_dir": ".tc-loop",
        },
        "verify": {
            "commands": ["bash scripts/guard-rails.sh"]
        },
    }
    cfg_path = root / "engine" / "policy.toml"
    if cfg_path.exists() and tomllib:
        try:
            with open(cfg_path, "rb") as f:
                loaded = tomllib.load(f)
            for sec, vals in loaded.items():
                if sec in policy and isinstance(vals, dict):
                    policy[sec].update(vals)
                else:
                    policy[sec] = vals
        except Exception:
            pass
    return policy


def resolve_project_paths(root_dir: Path | None = None) -> Dict[str, Any]:
    root = root_dir or find_root_dir()
    policy = load_project_policy(root)
    proj = policy.get("project", {})
    loop_cfg = policy.get("loop", {})

    def _pick_dir(candidates: List[str], default_rel: str) -> Path:
        for rel in candidates:
            p = root / rel
            if p.exists() and p.is_dir():
                return p
        return root / default_rel

    def _pick_file(candidates: List[str], default_rel: str) -> Path:
        for rel in candidates:
            p = root / rel
            if p.exists() and p.is_file():
                return p
        return root / default_rel

    specs_dir = _pick_dir([loop_cfg.get("task_specs_dir", "specs"), "specs", "SourceCode/specs"], "specs")
    backlog_file = _pick_file([loop_cfg.get("backlog_file", "backlog/BACKLOG.md"), "backlog/BACKLOG.md", "BACKLOG.md"], "backlog/BACKLOG.md")
    wireframes_dir = _pick_dir([proj.get("wireframes_dir", "docs/wireframes"), "docs/wireframes", "wireframes"], "docs/wireframes")
    frontend_dir = _pick_dir([proj.get("frontend_dir", "src/WebApp"), "src/WebApp", "frontend", "apps/web"], proj.get("frontend_dir", "src/WebApp"))
    backend_dir = _pick_dir([proj.get("backend_dir", "src"), "src", "backend"], proj.get("backend_dir", "src"))
    tests_dir = _pick_dir([proj.get("tests_dir", "tests"), "tests"], "tests")
    state_dir = root / loop_cfg.get("state_dir", ".tc-loop")
    docs_dir = _pick_dir([proj.get("docs_dir", "docs"), "docs"], "docs")

    return {
        "root_dir": root,
        "policy": policy,
        "project_name": proj.get("name", "TC IT Enterprise Project"),
        "specs_dir": specs_dir,
        "backlog_file": backlog_file,
        "wireframes_dir": wireframes_dir,
        "frontend_dir": frontend_dir,
        "backend_dir": backend_dir,
        "tests_dir": tests_dir,
        "state_dir": state_dir,
        "docs_dir": docs_dir,
        "verify_commands": policy.get("verify", {}).get("commands", ["bash scripts/guard-rails.sh"]),
    }
