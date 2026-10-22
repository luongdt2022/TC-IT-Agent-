#!/usr/bin/env python3
"""
TC IT AGENT ORCHESTRATOR - DAG ENGINE
=========================================
Bóc tách toàn bộ tasks từ SourceCode/specs/**/tasks.md và ROADMAP.md,
xây dựng đồ thị phụ thuộc DAG (Directed Acyclic Graph),
tính toán phân tầng Wave (Topological Sort),
xác định Critical Path và tự động tính toán trạng thái (BLOCKED, READY, RUNNING, DONE, NEEDS YOU).
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple

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
        self.category = category  # BE, FE, INFRA, KERNEL, TEST, SPEC, INT, DELTA
        self.is_done = is_done
        self.dependencies = dependencies or []
        self.dependents: List[str] = []
        self.duration_est_min = duration_est_min
        
        # Computed fields
        self.wave: int = 0
        self.status: str = "DONE" if is_done else "BLOCKED"  # DONE, READY, BLOCKED, RUNNING, NEEDS_YOU
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
        if root_dir is None:
            current = Path(__file__).resolve().parent
            for p in [current, *current.parents]:
                if (p / ".git").exists() or (p / "engine" / "policy.toml").exists() or (p / "AGENTS.md").exists():
                    current = p
                    break
            self.root_dir = current
        else:
            self.root_dir = Path(root_dir)

        if (self.root_dir / "SourceCode" / "specs").exists():
            self.specs_dir = self.root_dir / "SourceCode" / "specs"
        elif (self.root_dir / "specs").exists():
            self.specs_dir = self.root_dir / "specs"
        else:
            self.specs_dir = self.root_dir / "specs"

        for sf in [self.root_dir / ".tc-loop" / "state.json", self.root_dir / ".nacen-loop" / "state.json"]:
            if sf.parent.exists():
                self.state_file = sf
                break
        else:
            self.state_file = self.root_dir / ".tc-loop" / "state.json"
        self.nodes: Dict[str, TaskNode] = {}
        self.epic_order: List[str] = [
            "TASK-00", "TASK-06", "TASK-07", "TASK-02", 
            "TASK-04", "TASK-03", "TASK-05", "TASK-01", 
            "TASK-08", "TASK-09"
        ]

    def parse_tasks_file(self, file_path: Path, epic_id: str) -> List[TaskNode]:
        """Bóc tách các task từ một tệp tasks.md."""
        tasks: List[TaskNode] = []
        if not file_path.exists():
            return tasks

        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()

        # Regex nhận diện định dạng task:
        # e.g: - [x] `T-00.1` **[INFRA]** Rà soát và chuẩn hóa...
        # e.g: - [ ] **T-01.01** `[CONTRACT]` Định nghĩa bộ DTOs...
        # Regex nhận diện định dạng task linh hoạt (T-00.1, TASK-03-CR58, CR-01, v.v.):
        task_regex = re.compile(
            r"^\s*-\s*\[(?P<check>[ xX])\]\s*[`\*]*(?P<id>[A-Za-z0-9_.-]+)[`\*]*\s*(?:\[|`\[|\*\*)?(?P<cat>[A-Z_]+)?(?:\]|`\]|\*\*)?\s*(?:\[(?P<pri>P[0-9])\])?\s*(?P<title>.*)$"
        )
        
        # Regex linh hoạt hơn cho các định dạng khác nếu có
        fallback_regex = re.compile(
            r"^\s*-\s*\[(?P<check>[ xX])\]\s*(?P<content>.*)$"
        )

        # Regex nhận diện Section/Phase: ## Giai đoạn 1, ### Phase 1...
        phase_regex = re.compile(r"^\s*#{2,3}\s*(Giai đoạn|Phase)\s*(?P<num>[0-9]+)", re.IGNORECASE)
        
        current_phase_tasks: List[str] = []
        prev_phase_last_tasks: List[str] = []

        for line in lines:
            line_str = line.strip()
            
            # Kiểm tra chuyển Phase
            p_match = phase_regex.match(line_str)
            if p_match:
                if current_phase_tasks:
                    prev_phase_last_tasks = list(current_phase_tasks)
                    current_phase_tasks = []
                continue

            if not line_str.startswith("- ["):
                continue

            match = task_regex.match(line_str)
            if match and match.group("id"):
                is_done = match.group("check").lower() == "x"
                t_id = match.group("id")
                if not t_id.startswith(epic_id):
                    clean_id = f"{epic_id}-{t_id.replace('T-', '').replace('`', '')}"
                else:
                    clean_id = t_id
                
                cat = match.group("cat") or "DEV"
                title = match.group("title").strip(" `*:-")

                # Làm sạch tags phân loại hoặc người gửi lọt vào title
                m_cat = re.search(r"(\*\*|`)?\[(CR|TASK|FE|BE|TEST|DEV|DELTA|INFRA|CONTRACT|INT|KERNEL)\](\*\*|`)?", title, re.IGNORECASE)
                if m_cat:
                    cat = m_cat.group(2).upper()
                    title = re.sub(r"^\s*(\*\*|`)?\[(CR|TASK|FE|BE|TEST|DEV|DELTA|INFRA|CONTRACT|INT|KERNEL)\](\*\*|`)?\s*", "", title, flags=re.IGNORECASE)
                title = re.sub(r"^\s*\[P[0-9]\]\s*", "", title)
                title = re.sub(r"^\s*\(Người gửi:\s*[^)]+\)\s*", "", title, flags=re.IGNORECASE)
                title = title.strip(" `*:-—	")
                
                deps = list(prev_phase_last_tasks[:2]) if prev_phase_last_tasks else []

                node = TaskNode(
                    task_id=clean_id,
                    title=title,
                    epic_id=epic_id,
                    milestone=self._get_milestone_for_epic(epic_id),
                    category=cat,
                    is_done=is_done,
                    dependencies=deps
                )
                tasks.append(node)
                current_phase_tasks.append(clean_id)
            else:
                f_match = fallback_regex.match(line_str)
                if f_match:
                    is_done = f_match.group("check").lower() == "x"
                    content_str = f_match.group("content").strip()
                    id_search = re.search(r"[`\*]*([A-Za-z0-9_.-]+)[`\*]*", content_str)
                    raw_id = id_search.group(1) if id_search else f"T-{len(tasks)+1}"
                    if not raw_id.startswith(epic_id):
                        clean_id = f"{epic_id}-{raw_id.replace('T-', '').replace('`', '')}"
                    else:
                        clean_id = raw_id
                    
                    deps = list(prev_phase_last_tasks[:2]) if prev_phase_last_tasks else []
                    node = TaskNode(
                        task_id=clean_id,
                        title=content_str[:80],
                        epic_id=epic_id,
                        milestone=self._get_milestone_for_epic(epic_id),
                        category="DEV",
                        is_done=is_done,
                        dependencies=deps
                    )
                    tasks.append(node)
                    current_phase_tasks.append(clean_id)

        return tasks

    def _get_milestone_for_epic(self, epic_id: str) -> str:
        milestone_map = {
            "TASK-00": "M0",
            "TASK-06": "M1",
            "TASK-07": "M1",
            "TASK-02": "M2",
            "TASK-04": "M2",
            "TASK-03": "M3",
            "TASK-05": "M3",
            "TASK-01": "M4",
            "TASK-08": "M4",
            "TASK-09": "M5"
        }
        for k, v in milestone_map.items():
            if epic_id.startswith(k):
                return v
        return "M1"

    def scan_all_specs(self) -> Dict[str, TaskNode]:
        """Quét toàn bộ thư mục SourceCode/specs và xây dựng đồ thị liên kết."""
        self.nodes = {}
        if not self.specs_dir.exists():
            return self.nodes

        epic_first_tasks: Dict[str, str] = {}
        epic_last_tasks: Dict[str, str] = {}

        # 1. Quét từng thư mục Epic
        spec_dirs = sorted([d for d in self.specs_dir.iterdir() if d.is_dir() and d.name.startswith("TASK-")])
        for s_dir in spec_dirs:
            epic_id = s_dir.name.split("_")[0]  # vd: TASK-00
            tasks_file = s_dir / "tasks.md"
            if tasks_file.exists():
                parsed_tasks = self.parse_tasks_file(tasks_file, epic_id)
                if parsed_tasks:
                    epic_first_tasks[epic_id] = parsed_tasks[0].task_id
                    epic_last_tasks[epic_id] = parsed_tasks[-1].task_id
                    for t in parsed_tasks:
                        self.nodes[t.task_id] = t

        # 2. Liên kết Dependencies giữa các Epics theo Recommended Execution Sequence
        # TASK-00 -> TASK-06 -> TASK-07 -> TASK-02 -> TASK-04 -> TASK-03 -> TASK-05 -> TASK-01 -> TASK-08 -> TASK-09
        epic_sequence = [
            ("TASK-00", "TASK-06"),
            ("TASK-06", "TASK-07"),
            ("TASK-07", "TASK-02"),
            ("TASK-02", "TASK-04"),
            ("TASK-04", "TASK-03"),
            ("TASK-03", "TASK-05"),
            ("TASK-05", "TASK-01"),
            ("TASK-01", "TASK-08"),
            ("TASK-08", "TASK-09")
        ]

        for parent_epic, child_epic in epic_sequence:
            if parent_epic in epic_last_tasks and child_epic in epic_first_tasks:
                last_task_of_parent = epic_last_tasks[parent_epic]
                first_task_of_child = epic_first_tasks[child_epic]
                # Thêm dependency từ task cuối của parent sang task đầu của child
                child_node = self.nodes.get(first_task_of_child)
                if child_node and last_task_of_parent not in child_node.dependencies:
                    child_node.dependencies.append(last_task_of_parent)

        # 3. Điền ngược trường dependents cho từng node
        for node_id, node in self.nodes.items():
            for dep_id in node.dependencies:
                if dep_id in self.nodes:
                    if node_id not in self.nodes[dep_id].dependents:
                        self.nodes[dep_id].dependents.append(node_id)

        # 4. Tính toán Topological Sort & Wave
        self.compute_waves()

        # 5. Đọc runtime state để xác định RUNNING / NEEDS YOU
        self.apply_runtime_state()

        # 6. Tính toán Critical Path Method (CPM)
        self.compute_critical_path()

        return self.nodes

    def compute_waves(self):
        """Tính toán Wave (tầng topo) cho từng task."""
        # Wave của node = 0 nếu không có dependencies.
        # Ngược lại = 1 + max(wave của dependencies).
        # Sử dụng thuật toán đệ quy có ghi nhớ (Memoization) + kiểm tra Cycle.
        memo: Dict[str, int] = {}
        visiting: Set[str] = set()

        def get_wave(node_id: str) -> int:
            if node_id in memo:
                return memo[node_id]
            if node_id in visiting:
                # Phát hiện cycle, ngắt an toàn
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
        """Cập nhật trạng thái động từ .nacen-loop/state.json và quan hệ cha-con."""
        active_task_id = None
        loop_status = "IDLE"
        if self.state_file.exists():
            try:
                state_data = json.loads(self.state_file.read_text(encoding="utf-8"))
                active_task_id = state_data.get("active_task_id")
                loop_status = state_data.get("status", "IDLE")
            except Exception:
                pass

        for node_id, node in self.nodes.items():
            if node.is_done:
                node.status = "DONE"
                continue

            # Kiểm tra xem có đang running không
            if active_task_id and (node_id == active_task_id or node_id.endswith(str(active_task_id))):
                node.status = "RUNNING"
                continue

            # Kiểm tra xem các dependency cha đã xong hết chưa
            all_deps_done = True
            for dep_id in node.dependencies:
                dep_node = self.nodes.get(dep_id)
                if not dep_node or not dep_node.is_done:
                    all_deps_done = False
                    break

            if all_deps_done:
                node.status = "READY"
            else:
                node.status = "BLOCKED"

    def compute_critical_path(self):
        """Tính toán đường găng Critical Path Method (CPM)."""
        if not self.nodes:
            return

        # Forward pass (Tính Earliest Start & Earliest Finish)
        # Sắp xếp các node theo wave tăng dần
        sorted_nodes = sorted(self.nodes.values(), key=lambda n: n.wave)
        for node in sorted_nodes:
            if not node.dependencies:
                node.earliest_start = 0
            else:
                parent_finishes = [self.nodes[dep].earliest_finish for dep in node.dependencies if dep in self.nodes]
                node.earliest_start = max(parent_finishes) if parent_finishes else 0
            node.earliest_finish = node.earliest_start + node.duration_est_min

        max_finish = max((n.earliest_finish for n in self.nodes.values()), default=0)

        # Backward pass (Tính Latest Finish & Latest Start)
        rev_sorted_nodes = sorted(self.nodes.values(), key=lambda n: n.wave, reverse=True)
        for node in rev_sorted_nodes:
            if not node.dependents:
                node.latest_finish = max_finish
            else:
                child_starts = [self.nodes[dep].latest_start for dep in node.dependents if dep in self.nodes]
                node.latest_finish = min(child_starts) if child_starts else max_finish
            node.latest_start = node.latest_finish - node.duration_est_min
            node.slack = node.latest_finish - node.earliest_finish

            # Đường găng khi độ trễ slack == 0
            if node.slack == 0:
                node.is_critical = True

    def export_graph_data(self) -> Dict[str, Any]:
        """Xuất dữ liệu định dạng JSON chuẩn cho React Flow & Dashboard UI."""
        self.scan_all_specs()
        
        nodes_list = []
        edges_list = []
        waves_summary: Dict[int, Dict[str, int]] = {}
        status_counts = {
            "needs_you": 0,
            "running": 0,
            "in_review": 0,
            "under_way": 0,
            "ready": 0,
            "blocked": 0,
            "done": 0
        }

        for node_id, node in self.nodes.items():
            nodes_list.append(node.to_dict())
            
            # Thống kê Wave
            w = node.wave
            if w not in waves_summary:
                waves_summary[w] = {"total": 0, "done": 0}
            waves_summary[w]["total"] += 1
            if node.is_done:
                waves_summary[w]["done"] += 1

            # Thống kê trạng thái
            s = node.status.lower()
            if s in status_counts:
                status_counts[s] += 1
            else:
                status_counts["blocked"] += 1

            # Sinh Edges
            for dep_id in node.dependencies:
                if dep_id in self.nodes:
                    is_edge_critical = node.is_critical and self.nodes[dep_id].is_critical
                    edges_list.append({
                        "id": f"e-{dep_id}->{node_id}",
                        "source": dep_id,
                        "target": node_id,
                        "is_critical": is_edge_critical
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

if __name__ == "__main__":
    engine = DAGEngine()
    data = engine.export_graph_data()
    print(f"✅ Quét thành công {data['total_tasks']} tasks!")
    print(f"📊 Thống kê trạng thái: {data['status_summary']}")
    print(f"🌊 Các Waves ({len(data['waves'])} waves):")
    for w in data['waves'][:5]:
        print(f"   Wave {w['wave']}: {w['done']}/{w['total']} tasks hoàn thành")
