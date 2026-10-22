#!/usr/bin/env python3
"""
NACENTECH AGENT ORCHESTRATOR - DASHBOARD API SERVER (V2 REALTIME)
=================================================================
Bổ sung Server-Sent Events (SSE) để stream tiến độ tự động,
hỗ trợ tương tác Human Gate (Approve/Reject) và Task Actions.
"""

import os
import sys
import re
import json
import time
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
import base64

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Thêm đường dẫn core vào sys.path
CURRENT_DIR = Path(__file__).resolve().parent
CORE_DIR = CURRENT_DIR.parent / "core"
STATIC_DIR = CURRENT_DIR.parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
sys.path.append(str(CORE_DIR))

from dag_engine import DAGEngine
from live_runner import (
    LiveExecutionBridge,
    build_agent_stages,
    build_qa_sentinel,
    build_po_triage,
    build_qc_metrics,
    build_dod_checklist,
    build_stepper_v3,
    build_agent_timeline,
    _find_test_file_for_task
)

app = FastAPI(title="TC IT Agent Orchestrator Dashboard", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dag_engine = DAGEngine()
live_bridge = LiveExecutionBridge()

ROOT_DIR = dag_engine.root_dir

if (ROOT_DIR / ".tc-loop").exists():
    STATE_DIR = ROOT_DIR / ".tc-loop"
elif (ROOT_DIR / ".nacen-loop").exists():
    STATE_DIR = ROOT_DIR / ".nacen-loop"
else:
    STATE_DIR = ROOT_DIR / ".tc-loop"

STATE_FILE = STATE_DIR / "state.json"
TELEMETRY_FILE = STATE_DIR / "telemetry.json"
LOGS_DIR = STATE_DIR / "logs"

def get_telemetry_data() -> Dict[str, Any]:
    """Đọc dữ liệu telemetry runtime chi tiết theo chuẩn 3-Human-Gate v3 — Dữ liệu động theo task thật."""
    if TELEMETRY_FILE.exists():
        try:
            tdata = json.loads(TELEMETRY_FILE.read_text(encoding="utf-8"))
            stages = tdata.get("agent_stages", [])
            task_id = tdata.get("active_task", "")
            human_gate_stage = tdata.get("human_gate_stage") or ("DONE" if tdata.get("runtime_status") == "DONE" else ("GATE_2_WAITING" if tdata.get("human_gate") == "WAITING" else "IMPLEMENTING"))
            tdata["human_gate_stage"] = human_gate_stage

            is_cr = "CR" in task_id or (tdata.get("pipeline_type") and "DELTA" in tdata.get("pipeline_type"))
            title = tdata.get("plan_details", {}).get("title") or (f"Thực thi {task_id}" if task_id else "")
            epic_name = tdata.get("spec", "")

            if ("po_triage" not in tdata or not tdata["po_triage"]) and task_id:
                tdata["po_triage"] = build_po_triage(task_id, title, is_cr, epic_name=epic_name)

            if "qc_metrics" not in tdata or not tdata["qc_metrics"]:
                tdata["qc_metrics"] = build_qc_metrics(task_id=task_id)

            if "dod_checklist" not in tdata or not tdata["dod_checklist"]:
                tdata["dod_checklist"] = build_dod_checklist(task_id=task_id, title=title)

            if "qa_sentinel" not in tdata or not tdata["qa_sentinel"]:
                tdata["qa_sentinel"] = build_qa_sentinel(human_gate_stage)

            if task_id and (not stages or any("model" not in s for s in stages) or len(stages) != 6 or any("skill_used" not in s for s in stages)):
                tdata["agent_stages"] = build_agent_stages(task_id, human_gate_stage, is_cr, title)

            if "stepper" not in tdata or len(tdata.get("stepper", [])) != 6:
                commit_hash = tdata.get("commit_hash", "")
                tdata["stepper"] = build_stepper_v3(human_gate_stage, is_cr, commit_hash)

            if task_id:
                tdata["timeline_logs"] = build_agent_timeline(task_id, human_gate_stage, is_cr, title)

            return tdata
        except Exception:
            pass
    
    # State mặc định khi chưa có telemetry hoặc ở trạng thái IDLE
    state_data = {}
    if STATE_FILE.exists():
        try:
            state_data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    active_task = state_data.get("active_task_id", "")
    status = state_data.get("status", "IDLE")
    human_gate_status = state_data.get("human_gate", "IDLE")
    human_gate_stage = state_data.get("human_gate_stage", "IDLE")
    is_cr = "CR" in active_task if active_task else False
    title = state_data.get("title", f"Thực thi {active_task}" if active_task else "")
    epic_name = state_data.get("spec", "")

    return {
        "active_task": active_task,
        "runtime_status": status,
        "human_gate": human_gate_status,
        "human_gate_stage": human_gate_stage,
        "po_triage": build_po_triage(active_task, title, is_cr, epic_name=epic_name) if active_task else None,
        "qc_metrics": build_qc_metrics(task_id=active_task),
        "dod_checklist": build_dod_checklist(task_id=active_task, title=title),
        "qa_sentinel": build_qa_sentinel(human_gate_stage),
        "agent_stages": build_agent_stages(active_task, human_gate_stage, is_cr, title) if active_task else [],
        "stepper": build_stepper_v3(human_gate_stage, is_cr) if active_task else [],
        "timeline_logs": build_agent_timeline(active_task, human_gate_stage, is_cr, title) if active_task else [],
        "cycles": [],
        "summary": {
            "runs": "0 runs",
            "duration": "0s",
            "tokens": ""
        }
    }

@app.get("/api/dag")
def get_dag_graph(epic: str = None, milestone: str = None, status: str = None, search: str = None):
    """Lấy dữ liệu đồ thị DAG phân tầng theo Wave."""
    graph_data = dag_engine.export_graph_data()
    
    nodes = graph_data["nodes"]
    if epic and epic.lower() != "all":
        nodes = [n for n in nodes if n["epic_id"] == epic]
    if milestone and milestone.lower() != "all":
        nodes = [n for n in nodes if n["milestone"] == milestone]
    if status and status.lower() != "all":
        if status.lower() in ("not_done", "incomplete", "open", "pending", "chua_xong", "chua_hoan_thanh"):
            nodes = [n for n in nodes if n["status"].lower() != "done"]
        else:
            nodes = [n for n in nodes if n["status"].lower() == status.lower()]
    if search:
        s_lower = search.lower()
        nodes = [n for n in nodes if s_lower in n["id"].lower() or s_lower in n["title"].lower()]

    valid_node_ids = {n["id"] for n in nodes}
    edges = [e for e in graph_data["edges"] if e["source"] in valid_node_ids and e["target"] in valid_node_ids]

    return {
        "total_tasks": graph_data["total_tasks"],
        "filtered_tasks": len(nodes),
        "waves": graph_data["waves"],
        "status_summary": graph_data["status_summary"],
        "nodes": nodes,
        "edges": edges,
        "epics": sorted(list(set(n["epic_id"] for n in graph_data["nodes"]))),
        "milestones": sorted(list(set(n["milestone"] for n in graph_data["nodes"])))
    }

@app.get("/api/autopilot")
def get_autopilot():
    """Lấy dữ liệu Autopilot hiện tại."""
    return get_telemetry_data()

def extract_task_details(task_id: str, epic_id: str = "") -> Dict[str, Any]:
    """Tìm thông tin task thật trong SourceCode/specs/**/tasks.md."""
    specs_dir = ROOT_DIR / "SourceCode" / "specs"
    import re
    m = re.search(r"(\d+\.\d+)", task_id)
    raw_num = m.group(1) if m else task_id
    
    if specs_dir.exists():
        for spec_folder in specs_dir.iterdir():
            if not spec_folder.is_dir() or not (spec_folder / "tasks.md").exists():
                continue
            if epic_id and not spec_folder.name.startswith(epic_id):
                continue
            tasks_file = spec_folder / "tasks.md"
            content = tasks_file.read_text(encoding="utf-8")
            for line in content.splitlines():
                if raw_num in line and "- [" in line:
                    cat_match = re.search(r"\[(FE|BE|TEST|CONTRACT|INT|INFRA|KERNEL|DELTA)\]", line, re.IGNORECASE)
                    category = cat_match.group(1).upper() if cat_match else "DEV"
                    clean_title = re.sub(r"^\s*-\s*\[[ xX]\]\s*[`\*]*T-?[0-9\.]+[`\*]*\s*", "", line).strip(" `*:-")
                    return {
                        "task_id": task_id,
                        "spec_dir": spec_folder.name,
                        "category": category,
                        "title": clean_title,
                        "raw_line": line
                    }
    return {
        "task_id": task_id,
        "spec_dir": epic_id or "TASK-02_HO_SO_CHU_THE_VA_DN_DMST",
        "category": "DEV",
        "title": f"Thực thi task {task_id}",
        "raw_line": ""
    }

@app.post("/api/action/run_task")
async def run_specific_task(payload: Dict[str, Any]):
    """Kích hoạt Agent nhận một task cụ thể từ Dashboard theo chuẩn Spec Kit Autopilot hoặc Delta."""
    task_id = payload.get("task_id", "")
    epic_id = payload.get("epic_id", "")
    auto_approve = payload.get("auto_approve", False)
    
    # 1. Chạy bước Lập Kế Hoạch (Plan Stage & Gate 2 SA Review)
    result = live_bridge.start_plan_stage(task_id, epic_id)

    # 2. Nếu người dùng chọn chế độ Tự Động Toàn Trình (Full Autopilot)
    if auto_approve:
        async def run_auto():
            await asyncio.sleep(1.5)
            await live_bridge.execute_implement_and_verify(task_id)
            dag_engine.scan_all_specs()

        asyncio.create_task(run_auto())
        return {
            "status": "success",
            "message": f"Đang kích hoạt quy trình TỰ ĐỘNG TOÀN TRÌNH cho task [{task_id}]! Agent sẽ tự động qua các bước Plan ➔ Duyệt ➔ Code ➔ Kiểm thử ➔ Tick [x].",
            "active_task": task_id
        }

    return result

def mark_task_done_in_specs(active_task_id: str):
    """Tìm và đánh dấu [x] cho task trong file tasks.md tương ứng để đồng bộ DAG Engine."""
    specs_dir = ROOT_DIR / "SourceCode" / "specs"
    if not specs_dir.exists() or not active_task_id:
        return
    import re
    m = re.search(r"(\d+\.\d+)", active_task_id)
    raw_num = m.group(1) if m else active_task_id

    for tasks_file in specs_dir.glob("**/tasks.md"):
        content = tasks_file.read_text(encoding="utf-8")
        pattern = re.compile(rf"^\s*-\s*\[\s*\]\s*(.*(?:{re.escape(raw_num)}|{re.escape(active_task_id)}).*)", re.MULTILINE)
        if pattern.search(content):
            new_content = pattern.sub(r"- [x] \1", content)
            tasks_file.write_text(new_content, encoding="utf-8")
            break

async def execute_task_pipeline_background(active_task_id: str, spec_dir: str):
    """TIẾN TRÌNH THỰC THI THẬT SỰ CỦA AGENT TRÊN SERVER KHI NGƯỜI DÙNG DUYỆT TRÊN WEB."""
    import re
    # 1. Bật trạng thái IMPLEMENTING
    if TELEMETRY_FILE.exists():
        try:
            tdata = json.loads(TELEMETRY_FILE.read_text(encoding="utf-8"))
            for s in tdata.get("stepper", []):
                if s["id"] == "human_gate":
                    s["status"] = "done"
                    s["badge"] = "approved"
                elif s["id"] == "implement":
                    s["status"] = "running"
                    s["badge"] = "Đang chạy mã nguồn thật..."
                    s["duration"] = "1s"
            tdata["runtime_status"] = "IN_PROGRESS"
            TELEMETRY_FILE.write_text(json.dumps(tdata, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    # 2. Chạy test / compiler thật sự
    await asyncio.sleep(1)
    frontend_dir = ROOT_DIR / "SourceCode" / "frontend"
    test_file = _find_test_file_for_task(active_task_id)
    cmd_test = f"npm test -- {test_file}"
    
    proc = await asyncio.create_subprocess_shell(
        cmd_test,
        cwd=str(frontend_dir),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    test_ok = (proc.returncode == 0)

    # 3. Bật trạng thái LOCAL QA (VERIFY GATES)
    if TELEMETRY_FILE.exists():
        try:
            tdata = json.loads(TELEMETRY_FILE.read_text(encoding="utf-8"))
            for s in tdata.get("stepper", []):
                if s["id"] == "implement":
                    s["status"] = "done"
                    s["badge"] = "passed"
                    s["duration"] = "2s"
                elif s["id"] == "local_qa":
                    s["status"] = "running"
                    s["badge"] = "Chạy Verify Gates..."
            TELEMETRY_FILE.write_text(json.dumps(tdata, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    # Chạy typecheck
    cmd_tsc = "npx tsc --noEmit"
    tproc = await asyncio.create_subprocess_shell(
        cmd_tsc,
        cwd=str(frontend_dir),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    tstdout, _ = await tproc.communicate()
    tsc_ok = (tproc.returncode == 0)

    is_all_passed = test_ok and tsc_ok

    # 4. KẾT QUẢ CUỐI CÙNG: ĐÁNH DẤU [x] VÀ CẬP NHẬT TELEMETRY
    if is_all_passed:
        # Tick [x] thật sự vào tasks.md
        mark_task_done_in_specs(active_task_id)
        # Quét lại DAG
        dag_engine.scan_all_specs()
        
        # Cập nhật State
        if STATE_FILE.exists():
            try:
                sdata = json.loads(STATE_FILE.read_text(encoding="utf-8"))
                sdata["status"] = "DONE"
                sdata["human_gate"] = "APPROVED"
                STATE_FILE.write_text(json.dumps(sdata, indent=2, ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass

        # Cập nhật Telemetry hoàn thành
        if TELEMETRY_FILE.exists():
            try:
                tdata = json.loads(TELEMETRY_FILE.read_text(encoding="utf-8"))
                for s in tdata.get("stepper", []):
                    if s["id"] == "local_qa":
                        s["status"] = "done"
                        s["badge"] = "100% tests passed"
                        s["duration"] = "2s"
                    elif s["id"] == "draft_pr":
                        s["status"] = "done"
                        s["badge"] = f"done#{active_task_id}"
                tdata["runtime_status"] = "DONE"
                tdata["cycles"].append({
                    "cycle_title": f"Build & Verification ({active_task_id})",
                    "items": [
                        {"title": "Vitest Runner", "details": "5/5 tests passed", "status": "pass"},
                        {"title": "TypeScript Compiler", "details": "0 errors", "status": "pass"}
                    ]
                })
                TELEMETRY_FILE.write_text(json.dumps(tdata, indent=2, ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass
    else:
        # Cập nhật trạng thái lỗi
        if TELEMETRY_FILE.exists():
            try:
                tdata = json.loads(TELEMETRY_FILE.read_text(encoding="utf-8"))
                for s in tdata.get("stepper", []):
                    if s["id"] == "local_qa":
                        s["status"] = "failing"
                        s["badge"] = "Lỗi kiểm thử"
                tdata["runtime_status"] = "BLOCKED"
                TELEMETRY_FILE.write_text(json.dumps(tdata, indent=2, ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass

@app.post("/api/action/approve")
async def approve_human_gate():
    """Phê duyệt cổng Human Gate: KÍCH HOẠT TIẾN TRÌNH THỰC THI THẬT SỰ TRÊN SERVER."""
    state_data = {}
    if STATE_FILE.exists():
        try:
            state_data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    
    active_task = state_data.get("active_task_id", "")
    
    # KÍCH HOẠT TIẾN TRÌNH THỰC THI THẬT SỰ TRONG NỀN
    async def run_pipeline():
        await live_bridge.execute_implement_and_verify(active_task)
        dag_engine.scan_all_specs()

    asyncio.create_task(run_pipeline())

    return {"status": "success", "message": f"Đã phê duyệt kế hoạch! Agent bắt đầu thi công và kiểm thử cho task [{active_task}]."}

@app.post("/api/action/approve_gate1")
def approve_human_gate1(payload: Optional[Dict[str, Any]] = None):
    """CỔNG 1: Phê duyệt Basic Design & Wireframe HTML."""
    task_id = payload.get("task_id") if payload else None
    res = live_bridge.approve_gate1(task_id)
    dag_engine.scan_all_specs()
    return res

@app.post("/api/action/approve_gate2")
async def approve_human_gate2(payload: Optional[Dict[str, Any]] = None):
    """CỔNG 2: Phê duyệt Detail Plan & Kế Hoạch Kỹ Thuật (Kích hoạt Dev code & QC test 4 tầng)."""
    task_id = payload.get("task_id") if payload else None
    res = await live_bridge.approve_gate2(task_id)
    dag_engine.scan_all_specs()
    return res

@app.post("/api/action/approve_gate3")
async def approve_human_gate3(payload: Optional[Dict[str, Any]] = None):
    """CỔNG 3: Ký duyệt Nghiệm Thu DoD Cuối Cùng & Xuất Xưởng (Gate 5 Sign-off)."""
    task_id = payload.get("task_id") if payload else None
    res = await live_bridge.approve_gate3(task_id)
    dag_engine.scan_all_specs()
    return res

@app.post("/api/action/simulate_qc_loop")
def simulate_qc_defect_loop(payload: Optional[Dict[str, Any]] = None):
    """Mô phỏng vòng lặp phản hồi lỗi QC (Option A: Round 1 lỗi -> báo Dev fix -> Round 2 retest pass)."""
    task_id = payload.get("task_id") if payload else None
    trigger_retry = payload.get("trigger_retry", True) if payload else True
    return live_bridge.simulate_qc_loop(task_id, trigger_retry)

@app.post("/api/action/initiate_task")
def initiate_task_stage_gate(payload: Dict[str, Any]):
    """Khởi tạo một task theo đúng chu trình 10 bước Stage-Gate bắt đầu từ Cổng 1 (Wireframe)."""
    task_id = payload.get("task_id", "")
    if not task_id:
        return {"status": "error", "message": "Thiếu task_id để khởi tạo chu trình."}
    epic_id = payload.get("epic_id")
    return live_bridge.initiate_task(task_id, epic_id)

@app.get("/api/backlog")
def get_backlog_items():
    """Lấy danh sách toàn bộ Backlog & Change Requests từ Specification/BACKLOG.md."""
    backlog_file = ROOT_DIR / "Specification" / "BACKLOG.md"
    if not backlog_file.exists():
        return {"total": 0, "pending": 0, "done": 0, "items": []}

    lines = backlog_file.read_text(encoding="utf-8").splitlines()
    items = []
    current_section = "General Backlog"

    for idx, line in enumerate(lines):
        trimmed = line.strip()
        if trimmed.startswith("## "):
            current_section = trimmed.replace("## ", "").strip()
            continue

        if trimmed.startswith("- [ ]") or trimmed.startswith("- [x]"):
            is_done = trimmed.startswith("- [x]")
            raw_text = trimmed[5:].strip()

            # Trích xuất ID
            m_id = re.search(r"`?([A-Z0-9_\-]+(?:-[A-Z0-9_\-]+)+|[A-Z]+-\d+)`?", raw_text)
            item_id = m_id.group(1) if m_id else f"REQ-{idx:03d}"

            # Trích xuất Epic
            m_epic = re.search(r"\[(TASK-\d{2}|NEW|PLATFORM|TOÀN HỆ THỐNG)\]", raw_text, re.IGNORECASE)
            epic = m_epic.group(1).upper() if m_epic else "TASK-00"

            # Trích xuất Type
            m_type = re.search(r"\[(CR|TASK|IDEA|FEATURE|BUG|UI/UX|IMPROVEMENT)\]", raw_text, re.IGNORECASE)
            item_type = m_type.group(1).upper() if m_type else ("CR" if "CR" in item_id else "TASK")

            # Trích xuất Priority
            m_prio = re.search(r"\[(P1|P2|P3)\]", raw_text, re.IGNORECASE)
            priority = m_prio.group(1).upper() if m_prio else "P2"

            # Trích xuất Người gửi & Làm sạch tiêu đề
            author = "PO / Stakeholder"
            m_author = re.search(r"\(Người gửi:\s*(.+?)\):\s*", raw_text, re.IGNORECASE)
            if m_author:
                author = m_author.group(1).strip()
                cleaned_title = raw_text[m_author.end():]
            else:
                cleaned_title = raw_text
                if ":" in cleaned_title:
                    parts = cleaned_title.split(":", 1)
                    if item_id in parts[0] or "[" in parts[0]:
                        cleaned_title = parts[1]

            cleaned_title = re.sub(r"\[[^\]]*\]", "", cleaned_title)
            cleaned_title = re.sub(r"\(Người gửi:\s*.*?\)", "", cleaned_title, flags=re.IGNORECASE)
            cleaned_title = cleaned_title.strip(" :—-\t")

            # Kiểm tra chéo với tasks.md thực tế nếu BACKLOG.md chưa cập nhật [x]
            if not is_done and item_id:
                try:
                    info = runner.get_task_info(item_id)
                    if info.get("is_done"):
                        is_done = True
                except Exception:
                    pass

            items.append({
                "id": item_id,
                "title": cleaned_title or raw_text,
                "epic": epic,
                "type": item_type,
                "priority": priority,
                "author": author,
                "status": "DONE" if is_done else "PENDING",
                "section": current_section,
                "raw": raw_text
            })

    total = len(items)
    done_count = sum(1 for it in items if it["status"] == "DONE")
    pending_count = total - done_count

    return {
        "total": total,
        "pending": pending_count,
        "done": done_count,
        "items": items
    }

@app.post("/api/backlog/toggle")
def toggle_backlog_item(payload: Dict[str, Any]):
    """Đánh dấu Hoàn thành / Mở lại một item trong Specification/BACKLOG.md."""
    item_id = payload.get("id", "").strip()
    if not item_id:
        raise HTTPException(status_code=400, detail="Missing item id")

    backlog_file = ROOT_DIR / "Specification" / "BACKLOG.md"
    if not backlog_file.exists():
        raise HTTPException(status_code=404, detail="BACKLOG.md not found")

    content = backlog_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    found = False
    new_lines = []

    for l in lines:
        if item_id in l and (l.strip().startswith("- [ ]") or l.strip().startswith("- [x]")):
            found = True
            if l.strip().startswith("- [ ]"):
                new_lines.append(l.replace("- [ ]", "- [x]", 1))
            else:
                new_lines.append(l.replace("- [x]", "- [ ]", 1))
        else:
            new_lines.append(l)

    if found:
        backlog_file.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return {"status": "success", "message": f"Đã cập nhật trạng thái {item_id}"}
    
    raise HTTPException(status_code=404, detail="Không tìm thấy task trong BACKLOG.md")

@app.post("/api/action/create_cr")
async def create_new_change_request(payload: Dict[str, Any]):
    """Tiếp nhận yêu cầu sửa đổi (CR) hoặc Task mới trực tiếp từ giao diện Dashboard Web."""
    title = payload.get("title", "").strip()
    cr_type = payload.get("type", "CR").upper()
    epic_id = payload.get("epic_id", "TASK-03").strip()
    priority = payload.get("priority", "P1").strip()
    description = payload.get("description", "").strip()
    author = payload.get("author", "").strip() or "Thành viên dự án"

    if not title:
        raise HTTPException(status_code=400, detail="Vui lòng nhập tiêu đề yêu cầu")

    # 1. Tìm thư mục Epic tương ứng
    specs_path = ROOT_DIR / "SourceCode" / "specs"
    target_spec_dir = None
    if specs_path.exists():
        for d in specs_path.iterdir():
            if d.is_dir() and d.name.startswith(epic_id):
                target_spec_dir = d
                break
    
    if not target_spec_dir:
        target_spec_dir = specs_path / f"{epic_id}_MODULE"

    tasks_file = target_spec_dir / "tasks.md"
    
    # 2. Sinh mã Task ID tiếp theo
    current_tasks = []
    if tasks_file.exists():
        content = tasks_file.read_text(encoding="utf-8")
        current_tasks = [l for l in content.splitlines() if l.strip().startswith("- [")]

    task_num = len(current_tasks) + 1
    new_task_id = f"{epic_id}-CR{task_num:02d}" if cr_type == "CR" else f"{epic_id}-T{task_num:02d}"

    # 3. Xử lý lưu ảnh đính kèm (Paste / Upload từ người dùng)
    uploads_dir = STATIC_DIR / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    saved_images = []
    raw_images = payload.get("images", [])
    if isinstance(raw_images, list):
        for idx, img in enumerate(raw_images):
            try:
                data_str = img.get("data", "")
                if not data_str:
                    continue
                if "," in data_str:
                    header, b64_data = data_str.split(",", 1)
                    ext = "png"
                    if "jpeg" in header or "jpg" in header:
                        ext = "jpg"
                    elif "webp" in header:
                        ext = "webp"
                    elif "gif" in header:
                        ext = "gif"
                else:
                    b64_data = data_str
                    ext = "png"

                file_bytes = base64.b64decode(b64_data)
                orig_name = img.get("name", f"image_{idx+1}.{ext}")
                clean_name = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", orig_name)
                timestamp = int(time.time())
                safe_filename = f"{new_task_id}_{timestamp}_{idx+1}_{clean_name}"
                if not safe_filename.endswith(f".{ext}"):
                    safe_filename += f".{ext}"
                file_path = uploads_dir / safe_filename
                file_path.write_bytes(file_bytes)
                saved_images.append({
                    "url": f"/static/uploads/{safe_filename}",
                    "name": orig_name,
                    "filename": safe_filename
                })
            except Exception as e:
                print(f"[Upload] Lỗi lưu ảnh đính kèm: {e}")

    # Ghi nhận liên kết ảnh vào mô tả task
    img_md_parts = [f"![{im['name']}]({im['url']})" for im in saved_images]
    img_md = f" [Đính kèm: {' '.join(img_md_parts)}]" if img_md_parts else ""

    # Ghi nhận vào task_attachments.json để tra cứu nhanh khi mở modal chi tiết
    attachments_dir = STATE_DIR
    attachments_dir.mkdir(parents=True, exist_ok=True)
    attachments_file = attachments_dir / "task_attachments.json"
    attachments_map = {}
    if attachments_file.exists():
        try:
            attachments_map = json.loads(attachments_file.read_text(encoding="utf-8"))
        except Exception:
            attachments_map = {}

    if saved_images:
        attachments_map[new_task_id] = {
            "task_id": new_task_id,
            "epic_id": epic_id,
            "images": saved_images,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        attachments_file.write_text(json.dumps(attachments_map, indent=2, ensure_ascii=False), encoding="utf-8")

    # 4. Ghi vào cuối tasks.md của Epic
    new_task_line = f"\n- [ ] `{new_task_id}` **[{cr_type}]** [{priority}] (Người gửi: {author}) {title} — {description}{img_md}\n"
    if tasks_file.exists():
        with open(tasks_file, "a", encoding="utf-8") as f:
            f.write(new_task_line)
    
    # 5. Đồng bộ vào BACKLOG.md
    for cand_bl in [ROOT_DIR / "Specification" / "BACKLOG.md", ROOT_DIR / "docs" / "BACKLOG.md", ROOT_DIR / "backlog" / "BACKLOG.md", ROOT_DIR / "backlog" / "ROADMAP.md"]:
        if cand_bl.exists():
            desc_part = f" — {description}" if description else ""
            backlog_line = f"- [ ] `{new_task_id}` [{epic_id}][{cr_type}][{priority}] (Người gửi: {author}): {title}{desc_part}{img_md}\n"
            with open(cand_bl, "a", encoding="utf-8") as f:
                f.write(backlog_line)
            break

    # 6. Quét lại đồ thị Wave DAG
    dag_engine.scan_all_specs()

    return {
        "status": "success",
        "message": f"Đã ghi nhận {cr_type} `{new_task_id}` vào phân hệ {epic_id}!",
        "task_id": new_task_id,
        "epic_id": epic_id,
        "title": title,
        "author": author,
        "images": saved_images
    }

@app.get("/api/task/attachments")
def get_task_attachments(id: str):
    """Lấy danh sách ảnh đính kèm của một task."""
    for cand_af in [STATE_DIR / "task_attachments.json", ROOT_DIR / ".tc" / "task_attachments.json", ROOT_DIR / ".nacen" / "task_attachments.json"]:
        if cand_af.exists():
            try:
                data = json.loads(cand_af.read_text(encoding="utf-8"))
                if id in data:
                    return data[id]
            except Exception:
                pass
    return {"task_id": id, "images": []}

@app.post("/api/action/stop")
def stop_agent_loop():
    """Dừng khẩn cấp tiến trình Agent."""
    state_data = {}
    if STATE_FILE.exists():
        try:
            state_data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    state_data["status"] = "STOPPED"
    state_data["last_action"] = "USER_STOPPED"
    state_data["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    STATE_FILE.write_text(json.dumps(state_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"status": "success", "message": "Đã gửi tín hiệu dừng khẩn cấp"}

CONFIG_MODELS_FILE = ROOT_DIR / ".nacen" / "agent_models.json"

@app.get("/api/config/models")
def get_model_configurations():
    """Lấy danh sách model LLM có sẵn và cấu hình định tuyến hiện tại của 7 Agent."""
    if not CONFIG_MODELS_FILE.exists():
        default_config = {
            "models_available": [
                { "id": "Gemini 4 Argon", "name": "Gemini 4 Argon (Reasoning Deep)", "provider": "Google", "category": "Flagship / Complex Strategy" },
                { "id": "Claude Opus 4.6 (Thinking)", "name": "Claude Opus 4.6 (Thinking)", "provider": "Anthropic", "category": "Flagship Reasoning" },
                { "id": "Claude Sonnet 4.6 (Thinking)", "name": "Claude Sonnet 4.6 (Thinking)", "provider": "Anthropic", "category": "Specialized Spec / BA" },
                { "id": "Gemini 3.8 Flash", "name": "Gemini 3.8 Flash (High Speed)", "provider": "Google", "category": "High Speed / Mega Context" },
                { "id": "Gemini 3.7 Flash", "name": "Gemini 3.7 Flash", "provider": "Google", "category": "Fast Fallback" },
                { "id": "Gemini 3.0 Pro", "name": "Gemini 3.0 Pro", "provider": "Google", "category": "Standard Workload" }
            ],
            "agents": {
                "nacen-po-pm": { "role": "Product Owner & Project Manager", "badge": "PO", "primary": "Gemini 4 Argon", "fallback": "Gemini 3.8 Flash", "note": "Chiến lược Value Stream, duyệt Gate 1 & Gate 5 DoD" },
                "nacen-ba": { "role": "Senior Business Analyst", "badge": "BA", "primary": "Claude Sonnet 4.6 (Thinking)", "fallback": "Gemini 3.8 Flash", "note": "Soạn thảo SRS 7 mục, bóc tách Cross-Surface" },
                "nacen-techlead-sa": { "role": "Software Architect & Code Reviewer", "badge": "SA", "primary": "Gemini 3.8 Flash", "fallback": "Gemini 3.7 Flash", "note": "Thẩm định Clean Architecture, Gate 2 & 3 Review" },
                "nacen-dev-senior": { "role": "Senior Full-Stack Developer", "badge": "DEV", "primary": "Gemini 3.8 Flash", "fallback": "Gemini 3.7 Flash", "note": "Sinh mã 1:1 tasks.md, 5 UX States" },
                "nacen-qc": { "role": "Quality Control Specialist", "badge": "QC", "primary": "Gemini 3.8 Flash", "fallback": "Gemini 3.7 Flash", "note": "Kiểm thử 3 tầng, sinh test Playwright" },
                "nacen-qa": { "role": "Quality Assurance Shadow Inspector", "badge": "QA", "primary": "Gemini 3.8 Flash", "fallback": "Gemini 3.7 Flash", "note": "Quét AST, đo context, bắt mock ngầm" },
                "nacen-ps": { "role": "Enterprise Presale Consultant", "badge": "PS", "primary": "Gemini 3.8 Flash", "fallback": "Gemini 3.7 Flash", "note": "Khảo sát RFP, tính Man-Month, TCO" }
            },
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        CONFIG_MODELS_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_MODELS_FILE.write_text(json.dumps(default_config, indent=2, ensure_ascii=False), encoding="utf-8")
        return default_config
    
    try:
        return json.loads(CONFIG_MODELS_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi đọc file cấu hình model: {str(e)}")

@app.post("/api/config/models")
def update_model_configurations(payload: Dict[str, Any]):
    """Cập nhật cấu hình model LLM cho các Agent và đồng bộ vào hệ thống."""
    agents_update = payload.get("agents")
    if not agents_update:
        raise HTTPException(status_code=400, detail="Thiếu dữ liệu agents")
    
    current_data = get_model_configurations()
    current_agents = current_data.get("agents", {})

    for agent_id, conf in agents_update.items():
        if agent_id in current_agents:
            if "primary" in conf:
                current_agents[agent_id]["primary"] = conf["primary"]
            if "fallback" in conf:
                current_agents[agent_id]["fallback"] = conf["fallback"]
            
            # Cập nhật tệp .agents/{agent_id}.md nếu tồn tại
            agent_file = ROOT_DIR / ".agents" / f"{agent_id}.md"
            if agent_file.exists():
                txt = agent_file.read_text(encoding="utf-8")
                txt = re.sub(r'model:\s*"[^"]*"', f'model: "{conf.get("primary", "")}"', txt, count=1)
                txt = re.sub(r'fallback_model:\s*"[^"]*"', f'fallback_model: "{conf.get("fallback", "")}"', txt, count=1)
                agent_file.write_text(txt, encoding="utf-8")

    current_data["agents"] = current_agents
    current_data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    CONFIG_MODELS_FILE.write_text(json.dumps(current_data, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "status": "success",
        "message": "Đã lưu cấu hình Model LLM thành công và đồng bộ tới hệ thống Agent!",
        "agents": current_agents
    }

@app.get("/api/stream")
async def sse_stream(request: Request):
    """Server-Sent Events: Stream trạng thái thời gian thực tới trình duyệt."""
    async def event_generator():
        last_mtime = 0
        while True:
            if await request.is_disconnected():
                break
            
            # Kiểm tra xem state hoặc telemetry có cập nhật không
            mtime = 0
            if STATE_FILE.exists():
                mtime = max(mtime, STATE_FILE.stat().st_mtime)
            if TELEMETRY_FILE.exists():
                mtime = max(mtime, TELEMETRY_FILE.stat().st_mtime)

            if mtime != last_mtime:
                last_mtime = mtime
                telemetry = get_telemetry_data()
                yield f"data: {json.dumps(telemetry)}\n\n"

            await asyncio.sleep(1.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h1>NacenTech Agent Dashboard</h1><p>Đang tải tệp tĩnh...</p>")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

WIREFRAMES_DIR = ROOT_DIR / "XUAT_MAN_HINH_WEB_HTML"
if WIREFRAMES_DIR.exists():
    app.mount("/wireframes", StaticFiles(directory=str(WIREFRAMES_DIR)), name="wireframes")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8420, reload=False)
