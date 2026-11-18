#!/usr/bin/env python3
"""
TC IT AGENT ORCHESTRATOR - DASHBOARD API SERVER (v4.0)
======================================================
- Đọc đường dẫn động qua config_loader (engine/policy.toml).
- Bảo mật Admin Token + chế độ TC_PUBLIC_PORTAL=1 cho Cloudflare Tunnel.
- Tuân thủ Spec Management Constitution: create_cr sinh Delta Ledger PROPOSED.
"""

import os
import sys
import re
import json
import time
import socket
import base64
import secrets
import asyncio
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Request, Depends, Header
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

CURRENT_DIR = Path(__file__).resolve().parent
CORE_DIR = CURRENT_DIR.parent / "core"
STATIC_DIR = CURRENT_DIR.parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
sys.path.append(str(CORE_DIR))

from config_loader import resolve_project_paths
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
)

PATHS = resolve_project_paths()
ROOT_DIR: Path = PATHS["root_dir"]
SPECS_DIR: Path = PATHS["specs_dir"]
BACKLOG_FILE: Path = PATHS["backlog_file"]
WIREFRAMES_DIR: Path = PATHS["wireframes_dir"]
STATE_DIR: Path = PATHS["state_dir"]
STATE_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = STATE_DIR / "state.json"
TELEMETRY_FILE = STATE_DIR / "telemetry.json"
ADMIN_TOKEN_FILE = STATE_DIR / "admin.token"
ATTACHMENTS_FILE = STATE_DIR / "task_attachments.json"
CONFIG_MODELS_FILE = STATE_DIR / "agent_models.json"

PUBLIC_PORTAL_MODE = os.environ.get("TC_PUBLIC_PORTAL", "0") == "1"

if ADMIN_TOKEN_FILE.exists():
    ADMIN_TOKEN = ADMIN_TOKEN_FILE.read_text(encoding="utf-8").strip()
else:
    ADMIN_TOKEN = secrets.token_urlsafe(24)
    ADMIN_TOKEN_FILE.write_text(ADMIN_TOKEN, encoding="utf-8")

MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5MB
MAX_UPLOAD_COUNT = 5

app = FastAPI(title="TC IT Agent Orchestrator Dashboard", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8420", "http://localhost:8420"] if not PUBLIC_PORTAL_MODE else [],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

dag_engine = DAGEngine()
live_bridge = LiveExecutionBridge()


def require_admin(request: Request, x_tc_admin_token: Optional[str] = Header(default=None)):
    """Chặn tuyệt đối hành vi thực thi/cấu hình từ Public Portal hoặc khi thiếu Admin Token."""
    if PUBLIC_PORTAL_MODE:
        raise HTTPException(status_code=403, detail="Public Portal chỉ cho phép xem tiến độ và gửi CR mới.")
    client_host = request.client.host if request.client else ""
    if x_tc_admin_token == ADMIN_TOKEN:
        return True
    if client_host in ("127.0.0.1", "::1", "localhost") and not request.headers.get("cf-connecting-ip"):
        return True
    raise HTTPException(status_code=403, detail="Thiếu hoặc sai X-TC-Admin-Token.")


def _validate_image_bytes(data: bytes) -> Optional[str]:
    if len(data) > MAX_UPLOAD_BYTES:
        return None
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return "gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "webp"
    return None


def get_telemetry_data() -> Dict[str, Any]:
    tdata: Dict[str, Any] = {}
    if TELEMETRY_FILE.exists():
        try:
            tdata = json.loads(TELEMETRY_FILE.read_text(encoding="utf-8"))
        except Exception:
            tdata = {}

    state_data: Dict[str, Any] = {}
    if STATE_FILE.exists():
        try:
            state_data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass

    task_id = state_data.get("active_task_id") or tdata.get("active_task", "")
    runtime_status = state_data.get("status") or tdata.get("runtime_status", "IDLE")
    human_gate = state_data.get("human_gate") or tdata.get("human_gate", "IDLE")

    if task_id:
        try:
            task_info = live_bridge.get_task_info(task_id)
            if task_info.get("is_done") and runtime_status != "DONE":
                runtime_status = "DONE"
                human_gate = "IDLE"
                state_data["status"] = "DONE"
                state_data["human_gate"] = "IDLE"
                state_data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
                STATE_FILE.write_text(json.dumps(state_data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    human_gate_stage = "DONE" if runtime_status == "DONE" else (
        state_data.get("human_gate_stage") or tdata.get("human_gate_stage") or (
            "GATE_2_WAITING" if human_gate == "WAITING" else "IDLE"
        )
    )
    is_cr = "CR" in task_id or (state_data.get("pipeline") and "DELTA" in str(state_data.get("pipeline")))
    title = state_data.get("title") or tdata.get("plan_details", {}).get("title") or (f"Thực thi {task_id}" if task_id else "Chờ kích hoạt task mới")
    epic_name = state_data.get("spec") or tdata.get("spec", "")

    tdata["active_task"] = task_id
    tdata["runtime_status"] = runtime_status
    tdata["human_gate"] = human_gate
    tdata["human_gate_stage"] = human_gate_stage
    tdata["spec"] = epic_name
    tdata["project_name"] = PATHS["project_name"]
    tdata["public_portal_mode"] = PUBLIC_PORTAL_MODE

    if task_id:
        tdata["po_triage"] = build_po_triage(task_id, title, is_cr, epic_name=epic_name)
        if "qc_metrics" not in tdata:
            tdata["qc_metrics"] = build_qc_metrics(task_id=task_id)
        tdata["dod_checklist"] = build_dod_checklist(task_id=task_id, title=title, qc_summary=tdata["qc_metrics"].get("summary"))
        tdata["qa_sentinel"] = build_qa_sentinel(human_gate_stage)
        tdata["agent_stages"] = build_agent_stages(task_id, human_gate_stage, is_cr, title)
        commit_hash = tdata.get("commit_hash", "")
        tdata["stepper"] = build_stepper_v3(human_gate_stage, is_cr, commit_hash)
        tdata["timeline_logs"] = build_agent_timeline(task_id, human_gate_stage, is_cr, title)

    return tdata


@app.get("/api/meta")
def get_project_meta():
    return {
        "project_name": PATHS["project_name"],
        "public_portal_mode": PUBLIC_PORTAL_MODE,
        "specs_dir": str(SPECS_DIR.relative_to(ROOT_DIR)) if SPECS_DIR.is_relative_to(ROOT_DIR) else str(SPECS_DIR),
    }


@app.get("/api/dag")
def get_dag_graph(epic: str = None, milestone: str = None, status: str = None, search: str = None):
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
    return get_telemetry_data()


@app.post("/api/action/run_task", dependencies=[Depends(require_admin)])
async def run_specific_task(payload: Dict[str, Any]):
    task_id = payload.get("task_id", "")
    epic_id = payload.get("epic_id", "")
    auto_approve = payload.get("auto_approve", False)
    result = live_bridge.start_plan_stage(task_id, epic_id)

    if auto_approve:
        async def run_auto():
            await asyncio.sleep(1.0)
            await live_bridge.execute_implement_and_verify(task_id)
            dag_engine.scan_all_specs()
        asyncio.create_task(run_auto())
        return {
            "status": "success",
            "message": f"Đang kích hoạt quy trình TỰ ĐỘNG cho task [{task_id}].",
            "active_task": task_id
        }
    return result


@app.post("/api/action/approve", dependencies=[Depends(require_admin)])
async def approve_human_gate():
    state_data = {}
    if STATE_FILE.exists():
        try:
            state_data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    active_task = state_data.get("active_task_id", "")

    async def run_pipeline():
        await live_bridge.execute_implement_and_verify(active_task)
        dag_engine.scan_all_specs()
    asyncio.create_task(run_pipeline())
    return {"status": "success", "message": f"Đã phê duyệt kế hoạch cho task [{active_task}]."}


@app.post("/api/action/approve_gate1", dependencies=[Depends(require_admin)])
def approve_human_gate1(payload: Optional[Dict[str, Any]] = None):
    res = live_bridge.approve_gate1(payload.get("task_id") if payload else None)
    dag_engine.scan_all_specs()
    return res


@app.post("/api/action/approve_gate2", dependencies=[Depends(require_admin)])
async def approve_human_gate2(payload: Optional[Dict[str, Any]] = None):
    res = await live_bridge.approve_gate2(payload.get("task_id") if payload else None)
    dag_engine.scan_all_specs()
    return res


@app.post("/api/action/approve_gate3", dependencies=[Depends(require_admin)])
async def approve_human_gate3(payload: Optional[Dict[str, Any]] = None):
    res = await live_bridge.approve_gate3(payload.get("task_id") if payload else None)
    dag_engine.scan_all_specs()
    return res


@app.post("/api/action/simulate_qc_loop", dependencies=[Depends(require_admin)])
def simulate_qc_defect_loop(payload: Optional[Dict[str, Any]] = None):
    return live_bridge.simulate_qc_loop()


@app.post("/api/action/initiate_task", dependencies=[Depends(require_admin)])
def initiate_task_stage_gate(payload: Dict[str, Any]):
    task_id = payload.get("task_id", "")
    if not task_id:
        return {"status": "error", "message": "Thiếu task_id để khởi tạo chu trình."}
    return live_bridge.initiate_task(task_id, payload.get("epic_id"))


@app.get("/api/backlog")
def get_backlog_items():
    if not BACKLOG_FILE.exists():
        return {"total": 0, "pending": 0, "done": 0, "items": []}

    raw_content = BACKLOG_FILE.read_text(encoding="utf-8")
    clean_content = re.sub(r"<!--.*?-->", "", raw_content, flags=re.DOTALL)
    items = []
    current_section = "General Backlog"

    for idx, line in enumerate(clean_content.splitlines()):
        trimmed = line.strip()
        if trimmed.startswith("## "):
            current_section = trimmed.replace("## ", "").strip()
            continue

        if trimmed.startswith("- [ ]") or trimmed.startswith("- [x]") or trimmed.startswith("- [X]"):
            is_done = trimmed.lower().startswith("- [x]")
            raw_text = trimmed[5:].strip()

            m_id = re.search(r"`?([A-Z0-9_\-]+(?:-[A-Z0-9_\-]+)+|[A-Z]+-\d+)`?", raw_text)
            item_id = m_id.group(1) if m_id else f"REQ-{idx:03d}"
            m_epic = re.search(r"\[((?:EPIC|TASK)-\d{2,3}|NEW|PLATFORM)\]", raw_text, re.IGNORECASE)
            epic = m_epic.group(1).upper() if m_epic else "GENERAL"
            m_type = re.search(r"\[(CR|TASK|IDEA|FEATURE|BUG|UI/UX|IMPROVEMENT)\]", raw_text, re.IGNORECASE)
            item_type = m_type.group(1).upper() if m_type else ("CR" if "CR" in item_id else "TASK")
            m_prio = re.search(r"\[(P1|P2|P3)\]", raw_text, re.IGNORECASE)
            priority = m_prio.group(1).upper() if m_prio else "P2"

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

            if not is_done and item_id:
                try:
                    if live_bridge.get_task_info(item_id).get("is_done"):
                        is_done = True
                except Exception:
                    pass

            items.append({
                "id": item_id, "title": cleaned_title or raw_text, "epic": epic,
                "type": item_type, "priority": priority, "author": author,
                "status": "DONE" if is_done else "PENDING",
                "section": current_section, "raw": raw_text
            })

    total = len(items)
    done_count = sum(1 for it in items if it["status"] == "DONE")
    return {"total": total, "pending": total - done_count, "done": done_count, "items": items}


@app.post("/api/backlog/toggle", dependencies=[Depends(require_admin)])
def toggle_backlog_item(payload: Dict[str, Any]):
    item_id = payload.get("id", "").strip()
    if not item_id:
        raise HTTPException(status_code=400, detail="Missing item id")
    if not BACKLOG_FILE.exists():
        raise HTTPException(status_code=404, detail="BACKLOG.md not found")

    lines = BACKLOG_FILE.read_text(encoding="utf-8").splitlines()
    found = False
    new_lines = []
    for l in lines:
        if item_id in l and (l.strip().startswith("- [ ]") or l.strip().lower().startswith("- [x]")):
            found = True
            new_lines.append(l.replace("- [ ]", "- [x]", 1) if l.strip().startswith("- [ ]") else re.sub(r"- \[[xX]\]", "- [ ]", l, count=1))
        else:
            new_lines.append(l)

    if found:
        BACKLOG_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return {"status": "success", "message": f"Đã cập nhật trạng thái {item_id}"}
    raise HTTPException(status_code=404, detail="Không tìm thấy task trong BACKLOG.md")


@app.post("/api/action/create_cr")
async def create_new_change_request(payload: Dict[str, Any]):
    """Tiếp nhận CR/Task mới, tạo Delta Ledger PROPOSED theo Hiến pháp và ghi vào BACKLOG.md."""
    title = payload.get("title", "").strip()
    cr_type = payload.get("type", "CR").upper()
    epic_id = re.sub(r"[^A-Za-z0-9_-]", "", payload.get("epic_id", "EPIC-01").strip()) or "EPIC-01"
    priority = payload.get("priority", "P1").strip()
    description = payload.get("description", "").strip()
    author = payload.get("author", "").strip() or "Stakeholder"

    if not title:
        raise HTTPException(status_code=400, detail="Vui lòng nhập tiêu đề yêu cầu")

    target_spec_dir = None
    if SPECS_DIR.exists():
        for d in SPECS_DIR.iterdir():
            if d.is_dir() and d.name.startswith(epic_id):
                target_spec_dir = d
                break
    if not target_spec_dir:
        target_spec_dir = SPECS_DIR / epic_id

    deltas_dir = target_spec_dir / "deltas"
    deltas_dir.mkdir(parents=True, exist_ok=True)

    existing_deltas = list(deltas_dir.glob("CR-*.md"))
    seq = len(existing_deltas) + 1
    new_task_id = f"{epic_id}-CR{seq:02d}" if cr_type == "CR" else f"{epic_id}-T{seq:02d}"

    # Lưu ảnh đính kèm có kiểm tra kích thước & magic bytes
    uploads_dir = STATIC_DIR / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    saved_images = []
    raw_images = payload.get("images", [])
    if isinstance(raw_images, list):
        for idx, img in enumerate(raw_images[:MAX_UPLOAD_COUNT]):
            try:
                data_str = img.get("data", "")
                if not data_str:
                    continue
                b64_data = data_str.split(",", 1)[1] if "," in data_str else data_str
                file_bytes = base64.b64decode(b64_data)
                ext = _validate_image_bytes(file_bytes)
                if not ext:
                    continue
                safe_filename = f"{new_task_id}_{int(time.time())}_{idx+1}.{ext}"
                (uploads_dir / safe_filename).write_bytes(file_bytes)
                saved_images.append({"url": f"/static/uploads/{safe_filename}", "name": safe_filename, "filename": safe_filename})
            except Exception:
                pass

    img_links = " ".join(f"![{im['name']}]({im['url']})" for im in saved_images)
    img_md = f" [Đính kèm: {img_links}]" if saved_images else ""

    if saved_images:
        attachments_map = {}
        if ATTACHMENTS_FILE.exists():
            try:
                attachments_map = json.loads(ATTACHMENTS_FILE.read_text(encoding="utf-8"))
            except Exception:
                attachments_map = {}
        attachments_map[new_task_id] = {
            "task_id": new_task_id, "epic_id": epic_id,
            "images": saved_images, "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        ATTACHMENTS_FILE.write_text(json.dumps(attachments_map, indent=2, ensure_ascii=False), encoding="utf-8")

    # Sinh Delta Ledger file trạng thái PROPOSED theo SPEC_MANAGEMENT_CONSTITUTION.md
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", title.lower()).strip("_")[:40] or "change_request"
    delta_file = deltas_dir / f"CR-{seq:03d}_{slug}.md"
    delta_file.write_text(f"""# CHANGE REQUEST: {new_task_id} — {title}

- **Trạng thái**: PROPOSED
- **Epic**: {epic_id}
- **Mức độ ưu tiên**: {priority}
- **Tác giả đề xuất**: {author}
- **Ngày tạo**: {time.strftime('%Y-%m-%d')}

## 1. BỐI CẢNH & MÔ TẢ
{description or title}
{img_md}
""", encoding="utf-8")

    # Ghi nhận vào BACKLOG.md
    BACKLOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    desc_part = f" — {description}" if description else ""
    backlog_line = f"- [ ] `{new_task_id}` [{epic_id}][{cr_type}][{priority}] (Người gửi: {author}): {title}{desc_part}{img_md}\n"
    with open(BACKLOG_FILE, "a", encoding="utf-8") as f:
        f.write(backlog_line)

    dag_engine.scan_all_specs()
    return {
        "status": "success",
        "message": f"Đã ghi nhận {cr_type} `{new_task_id}` (Delta PROPOSED tại {delta_file.name})!",
        "task_id": new_task_id, "epic_id": epic_id,
        "title": title, "author": author, "images": saved_images
    }


@app.get("/api/task/attachments")
def get_task_attachments(id: str):
    if ATTACHMENTS_FILE.exists():
        try:
            data = json.loads(ATTACHMENTS_FILE.read_text(encoding="utf-8"))
            if id in data:
                return data[id]
        except Exception:
            pass
    return {"task_id": id, "images": []}


@app.post("/api/action/stop", dependencies=[Depends(require_admin)])
def stop_agent_loop():
    state_data = {}
    if STATE_FILE.exists():
        try:
            state_data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    state_data["status"] = "STOPPED"
    state_data["last_action"] = "USER_STOPPED"
    state_data["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    STATE_FILE.write_text(json.dumps(state_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"status": "success", "message": "Đã gửi tín hiệu dừng khẩn cấp"}


@app.get("/api/config/models")
def get_model_configurations():
    if not CONFIG_MODELS_FILE.exists():
        default_config = {
            "models_available": [
                {"id": "inherit", "name": "Inherit (Theo Model IDE hiện tại)", "provider": "Antigravity", "category": "Recommended"},
                {"id": "pro", "name": "Pro Tier (Complex Reasoning)", "provider": "Antigravity", "category": "Deep Reasoning"},
                {"id": "flash", "name": "Flash Tier (High Speed)", "provider": "Antigravity", "category": "Fast Execution"},
                {"id": "flash_lite", "name": "Flash Lite (Lightweight)", "provider": "Antigravity", "category": "Economy"},
            ],
            "agents": {
                "po-pm": {"role": "Product Owner & Project Manager", "badge": "PO", "primary": "inherit", "fallback": "flash", "note": "Value Stream, duyệt Gate 1 & Gate 5 DoD"},
                "ba": {"role": "Senior Business Analyst", "badge": "BA", "primary": "inherit", "fallback": "flash", "note": "SRS 7 mục, Cross-Surface & Wireframe"},
                "sa": {"role": "Software Architect & TechLead", "badge": "SA", "primary": "inherit", "fallback": "flash", "note": "Clean Architecture, Gate 2 & Gate 3 Review"},
                "dev": {"role": "Senior Full-Stack Developer", "badge": "DEV", "primary": "inherit", "fallback": "flash", "note": "Code 1:1 tasks.md, 5 UX States, TDD"},
                "qc": {"role": "Pure Black-Box QC Specialist", "badge": "QC", "primary": "inherit", "fallback": "flash", "note": "Kiểm thử 4 tầng, Playwright & Deep DB Assert"},
                "qa": {"role": "Shadow SQA Inspector", "badge": "QA", "primary": "inherit", "fallback": "flash", "note": "Kiểm toán độc lập Gate 1-5, Context Telemetry"},
                "ps": {"role": "Enterprise Presale Consultant", "badge": "PS", "primary": "inherit", "fallback": "flash", "note": "RFP, WBS Man-Month, TCO"},
            },
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        CONFIG_MODELS_FILE.write_text(json.dumps(default_config, indent=2, ensure_ascii=False), encoding="utf-8")
        return default_config
    return json.loads(CONFIG_MODELS_FILE.read_text(encoding="utf-8"))


@app.post("/api/config/models", dependencies=[Depends(require_admin)])
def update_model_configurations(payload: Dict[str, Any]):
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
            agent_file = ROOT_DIR / ".agents" / "agents" / f"{agent_id}.md"
            if agent_file.exists() and conf.get("primary"):
                txt = agent_file.read_text(encoding="utf-8")
                txt = re.sub(r'model:\s*"[^"]*"', f'model: "{conf["primary"]}"', txt, count=1)
                agent_file.write_text(txt, encoding="utf-8")

    current_data["agents"] = current_agents
    current_data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    CONFIG_MODELS_FILE.write_text(json.dumps(current_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"status": "success", "message": "Đã lưu cấu hình Model LLM thành công!", "agents": current_agents}


@app.get("/api/stream")
async def sse_stream(request: Request):
    async def event_generator():
        last_mtime = 0.0
        heartbeat_counter = 0
        while True:
            if await request.is_disconnected():
                break
            mtime = 0.0
            for fp in (STATE_FILE, TELEMETRY_FILE, BACKLOG_FILE):
                if fp.exists():
                    mtime = max(mtime, fp.stat().st_mtime)
            if SPECS_DIR.exists():
                for tpath in SPECS_DIR.glob("**/tasks.md"):
                    mtime = max(mtime, tpath.stat().st_mtime)

            if mtime != last_mtime:
                last_mtime = mtime
                yield f"data: {json.dumps(get_telemetry_data(), ensure_ascii=False)}\n\n"

            heartbeat_counter += 1
            if heartbeat_counter >= 10:
                heartbeat_counter = 0
                yield ": ping\n\n"
            await asyncio.sleep(1.5)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache, no-transform", "Connection": "keep-alive", "X-Accel-Buffering": "no"}
    )


@app.get("/")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return HTMLResponse("<h1>TC IT Agent Dashboard</h1><p>index.html not found.</p>")


app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
if WIREFRAMES_DIR.exists():
    app.mount("/wireframes", StaticFiles(directory=str(WIREFRAMES_DIR)), name="wireframes")


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def find_available_port(start_port: int = 8420, max_attempts: int = 20) -> int:
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    return start_port


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TC IT Agent Dashboard Server")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    args, _ = parser.parse_known_args()

    env_port = os.environ.get("PORT") or os.environ.get("DASHBOARD_PORT")
    selected_port = args.port or (int(env_port) if env_port else None)
    if not selected_port:
        selected_port = find_available_port(8420)
    elif is_port_in_use(selected_port):
        selected_port = find_available_port(selected_port + 1)

    print(f"🚀 [TC IT Agent Dashboard] http://{args.host}:{selected_port} (Public Portal: {PUBLIC_PORTAL_MODE})")
    uvicorn.run(app, host=args.host, port=selected_port, reload=False)
