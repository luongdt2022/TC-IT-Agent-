#!/usr/bin/env python3
"""
TC IT AGENT ORCHESTRATOR - DAG ENGINE (v4.0)
=============================================
Bóc tách toàn bộ tasks từ specs/**/tasks.md (hỗ trợ cả EPIC-*, TASK-*, hoặc mọi thư mục có tasks.md),
xây dựng đồ thị phụ thuộc DAG (Directed Acyclic Graph) dựa trên Phase & Depends-On tường minh,
tính toán phân tầng Wave (Topological Sort), Critical Path (CPM) và trạng thái thực thi.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set, Any, Optional

from config_loader import resolve_project_paths


class TaskNode:
    def __init__(
        self,
        task_id: str,
        title: str,
        epic_id: str,
        milestone: str = "M1",
        category: str = "DEV",
        is_done: bool = False,
        dependencies: Optional[List[str]] = None,
        duration_est_min: int = 30
    ):
        self.task_id = task_id
        self.title = title
        self.epic_id = epic_id
        self.milestone = milestone
        self.category = category
        self.is_done = is_done
        self.dependencies = dependencies or []
        self.dependents: List[str] = []
        self.duration_est_min = duration_est_min

        self.wave: int = 0
        self.status: str = "DONE" if is_done else "BLOCKED"
        self.is_critical: bool = False
        self.earliest_start: int = 0
        self.earliest_finish: int = 0
        self.latest_start: int = 0
        self.latest_finish: int = 0
        self.slack: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.task_id,
            "title": self.title,
            "epic_id": self.epic_id,
            "milestone": self.milestone,
            "category": self.category,
            "is_done": self.is_done,
            "status": self.status,
            "wave": self.wave,
            "is_critical": self.is_critical,
            "dependencies": self.dependencies,
            "dependents": self.dependents,
            "duration_est_min": self.duration_est_min,
            "slack": self.slack
        }


class DAGEngine:
    def __init__(self, root_dir: Optional[Path] = None):
        paths = resolve_project_paths(root_dir)
        self.root_dir: Path = paths["root_dir"]
        self.specs_dir: Path = paths["specs_dir"]
        self.state_dir: Path = paths["state_dir"]
        self.state_file: Path = self.state_dir / "state.json"
        self.nodes: Dict[str, TaskNode] = {}

    def _normalize_task_id(self, raw_id: str, epic_id: str) -> str:
        clean = raw_id.replace("`", "").replace("*", "").strip()
        if clean.startswith(epic_id):
            return clean
        return f"{epic_id}-{clean.replace('T-', '')}"

    def parse_tasks_file(self, file_path: Path, epic_id: str) -> List[TaskNode]:
        """Bóc tách các task từ một tệp tasks.md, hỗ trợ Phase tuần tự và Depends on."""
        tasks: List[TaskNode] = []
        if not file_path.exists():
            return tasks

        lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        task_regex = re.compile(
            r"^\s*-\s*\[(?P<check>[ xX])\]\s*[`\*]*(?P<id>[A-Za-z0-9_.-]+)[`\*]*\s*(?:\[|`\[|\*\*)?(?P<cat>[A-Za-z_-]+)?(?:\]|`\]|\*\*)?\s*(?:\[(?P<pri>P[0-9])\])?\s*(?P<title>.*)$"
        )
        phase_regex = re.compile(r"^\s*#{2,3}\s*(Giai đoạn|Phase|Wave)\s*(?P<num>[0-9]+)", re.IGNORECASE)
        deps_regex = re.compile(r"(?:Depends(?:\s+on)?|Deps)\s*:\s*([A-Za-z0-9_.,\s-]+)", re.IGNORECASE)

        current_phase_tasks: List[str] = []
        prev_phase_last_tasks: List[str] = []

        for line in lines:
            line_str = line.strip()
            if phase_regex.match(line_str):
                if current_phase_tasks:
                    prev_phase_last_tasks = list(current_phase_tasks)
                    current_phase_tasks = []
                continue

            if not line_str.startswith("- ["):
                continue

            match = task_regex.match(line_str)
            if not match or not match.group("id"):
                continue

            is_done = match.group("check").lower() == "x"
            clean_id = self._normalize_task_id(match.group("id"), epic_id)
            cat = (match.group("cat") or "DEV").upper()
            title = match.group("title").strip(" `*:-")

            m_cat = re.search(r"(\*\*|`)?\[(CR|TASK|FE|BE|TEST|DEV|DELTA|INFRA|CONTRACT|INT|KERNEL|DOC)\](?:\*\*|`)?", title, re.IGNORECASE)
            if m_cat:
                cat = m_cat.group(2).upper()
                title = re.sub(r"^\s*(\*\*|`)?\[(CR|TASK|FE|BE|TEST|DEV|DELTA|INFRA|CONTRACT|INT|KERNEL|DOC)\](\*\*|`)?\s*", "", title, flags=re.IGNORECASE)

            explicit_deps: List[str] = []
            dm = deps_regex.search(title)
            if dm:
                raw_deps = [d.strip() for d in dm.group(1).split(",") if d.strip()]
                explicit_deps = [self._normalize_task_id(d, epic_id) for d in raw_deps]
                title = deps_regex.sub("", title).strip(" `*:-[];")

            title = re.sub(r"^\s*\[P[0-9]\]\s*", "", title)
            title = re.sub(r"^\s*\(Người gửi:\s*[^)]+\)\s*", "", title, flags=re.IGNORECASE)
            title = title.strip(" `*:-—\t")

            deps = explicit_deps if explicit_deps else (list(prev_phase_last_tasks[:2]) if prev_phase_last_tasks else [])
            node = TaskNode(
                task_id=clean_id,
                title=title or clean_id,
                epic_id=epic_id,
                milestone=self._get_milestone_for_epic(epic_id),
                category=cat,
                is_done=is_done,
                dependencies=deps
            )
            tasks.append(node)
            current_phase_tasks.append(clean_id)

        return tasks

    def _get_milestone_for_epic(self, epic_id: str) -> str:
        m = re.search(r"(\d+)", epic_id)
        if m:
            num = int(m.group(1))
            if num == 0:
                return "M0"
            return f"M{(num - 1) // 2 + 1}"
        return "M1"

    def scan_all_specs(self) -> Dict[str, TaskNode]:
        """Quét toàn bộ thư mục specs/ và xây dựng đồ thị liên kết động."""
        self.nodes = {}
        if not self.specs_dir.exists():
            return self.nodes

        spec_dirs = sorted([
            d for d in self.specs_dir.iterdir()
            if d.is_dir() and not d.name.startswith(".") and (d / "tasks.md").exists()
        ])

        for s_dir in spec_dirs:
            epic_id = s_dir.name.split("_")[0]
            parsed_tasks = self.parse_tasks_file(s_dir / "tasks.md", epic_id)
            for t in parsed_tasks:
                self.nodes[t.task_id] = t

        for node_id, node in self.nodes.items():
            for dep_id in node.dependencies:
                if dep_id in self.nodes and node_id not in self.nodes[dep_id].dependents:
                    self.nodes[dep_id].dependents.append(node_id)

        self.compute_waves()
        self.apply_runtime_state()
        self.compute_critical_path()
        return self.nodes

    def compute_waves(self):
        memo: Dict[str, int] = {}
        visiting: Set[str] = set()

        def get_wave(node_id: str) -> int:
            if node_id in memo:
                return memo[node_id]
            if node_id in visiting:
                return 0
            visiting.add(node_id)
            node = self.nodes.get(node_id)
            if not node or not node.dependencies:
                wave = 0
            else:
                valid_dep_waves = [get_wave(dep_id) for dep_id in node.dependencies if dep_id in self.nodes]
                wave = 1 + max(valid_dep_waves) if valid_dep_waves else 0
            visiting.remove(node_id)
            memo[node_id] = wave
            if node:
                node.wave = wave
            return wave

        for node_id in self.nodes:
            get_wave(node_id)

    def apply_runtime_state(self):
        active_task_id = None
        if self.state_file.exists():
            try:
                state_data = json.loads(self.state_file.read_text(encoding="utf-8"))
                active_task_id = state_data.get("active_task_id")
            except Exception:
                pass

        for node_id, node in self.nodes.items():
            if node.is_done:
                node.status = "DONE"
                continue
            if active_task_id and (node_id == active_task_id or node_id.endswith(str(active_task_id))):
                node.status = "RUNNING"
                continue
            all_deps_done = all(
                (dep_id in self.nodes and self.nodes[dep_id].is_done)
                for dep_id in node.dependencies
            )
            node.status = "READY" if all_deps_done else "BLOCKED"

    def compute_critical_path(self):
        if not self.nodes:
            return
        sorted_nodes = sorted(self.nodes.values(), key=lambda n: n.wave)
        for node in sorted_nodes:
            if not node.dependencies:
                node.earliest_start = 0
            else:
                parent_finishes = [self.nodes[dep].earliest_finish for dep in node.dependencies if dep in self.nodes]
                node.earliest_start = max(parent_finishes) if parent_finishes else 0
            node.earliest_finish = node.earliest_start + node.duration_est_min

        max_finish = max((n.earliest_finish for n in self.nodes.values()), default=0)
        rev_sorted_nodes = sorted(self.nodes.values(), key=lambda n: n.wave, reverse=True)
        for node in rev_sorted_nodes:
            if not node.dependents:
                node.latest_finish = max_finish
            else:
                child_starts = [self.nodes[dep].latest_start for dep in node.dependents if dep in self.nodes]
                node.latest_finish = min(child_starts) if child_starts else max_finish
            node.latest_start = node.latest_finish - node.duration_est_min
            node.slack = node.latest_finish - node.earliest_finish
            if node.slack == 0:
                node.is_critical = True

    def export_graph_data(self) -> Dict[str, Any]:
        self.scan_all_specs()
        nodes_list = []
        edges_list = []
        waves_summary: Dict[int, Dict[str, int]] = {}
        status_counts = {
            "needs_you": 0, "running": 0, "in_review": 0,
            "under_way": 0, "ready": 0, "blocked": 0, "done": 0
        }

        for node_id, node in self.nodes.items():
            nodes_list.append(node.to_dict())
            w = node.wave
            waves_summary.setdefault(w, {"total": 0, "done": 0})
            waves_summary[w]["total"] += 1
            if node.is_done:
                waves_summary[w]["done"] += 1

            s = node.status.lower()
            status_counts[s if s in status_counts else "blocked"] += 1

            for dep_id in node.dependencies:
                if dep_id in self.nodes:
                    edges_list.append({
                        "id": f"e-{dep_id}->{node_id}",
                        "source": dep_id,
                        "target": node_id,
                        "is_critical": node.is_critical and self.nodes[dep_id].is_critical
                    })

        return {
            "total_tasks": len(self.nodes),
            "waves": [
                {"wave": w, "done": waves_summary[w]["done"], "total": waves_summary[w]["total"]}
                for w in sorted(waves_summary.keys())
            ],
            "status_summary": status_counts,
            "nodes": nodes_list,
            "edges": edges_list
        }
