#!/usr/bin/env python3
"""
TC IT AGENT — SPECIFICATION INTEGRITY LINTER & PARITY AUDITOR
=============================================================================
Công cụ kiểm toán tính toàn vẹn và đối soát đồng bộ đa tầng cho Spec Kit:
1. Đối soát số lượng Task giữa tasks.md và ROADMAP.md (Zero Task Count Drift)
2. Kiểm tra tính liên tục, không lùi giai đoạn, không trùng lặp số Phase trong tasks.md
3. Bắt lỗi trùng lặp tiêu đề Delta / Versioning trong spec.md & plan.md
4. Bắt lỗi lệch pha trạng thái Header (Metadata Status: In Planning vs 100% Done)
5. Hỗ trợ linh hoạt cấu trúc specs/ hoặc SourceCode/specs/ cho mọi dự án
=============================================================================
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

# ANSI colors
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
BOLD = "\033[1m"
RESET = "\033[0m"

def get_project_root():
    current = Path(__file__).resolve().parent
    for p in [current, *current.parents]:
        if (p / ".git").exists() or (p / "specs").exists() or (p / "SourceCode" / "specs").exists() or (p / "AGENTS.md").exists():
            return p
    return current.parent

def find_specs_dir(root: Path):
    candidates = [
        root / "specs",
        root / "SourceCode" / "specs",
        root / "backlog" / "specs"
    ]
    for c in candidates:
        if c.exists() and c.is_dir():
            return c
    return root / "specs"

def find_roadmap_file(root: Path, specs_dir: Path):
    candidates = [
        specs_dir / "ROADMAP.md",
        root / "specs" / "ROADMAP.md",
        root / "backlog" / "ROADMAP.md",
        root / "ROADMAP.md"
    ]
    for c in candidates:
        if c.exists() and c.is_file():
            return c
    return specs_dir / "ROADMAP.md"

def parse_roadmap(roadmap_path: Path):
    """
    Trích xuất danh sách module, tiến độ và số task được ghi nhận trong ROADMAP.md
    """
    if not roadmap_path.exists():
        return {}
    
    content = roadmap_path.read_text(encoding="utf-8")
    roadmap_modules = {}
    
    # Tìm bảng Master Registry (Bảng 1)
    # Hỗ trợ cả TASK-XX, EPIC-XX hoặc mã tương đương
    table_pattern = re.compile(r"\|\s*\*\*`?((?:TASK|EPIC)-\d{2,3})`?\*\*\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|([^|]*)\|([^|]*)\|([^|]*)\|")
    
    for line in content.splitlines():
        match = table_pattern.search(line)
        if match:
            epic_id = match.group(1)
            status_text = match.group(2).strip()
            progress_text = match.group(3).strip()
            notes_text = match.group(4).strip()
            
            # Trích xuất số tasks từ progress hoặc notes
            task_match = re.search(r"\((\d+)/(\d+)\s*(?:Tasks|tasks)?\)", progress_text + " " + notes_text)
            recorded_done = int(task_match.group(1)) if task_match else None
            recorded_total = int(task_match.group(2)) if task_match else None
            
            roadmap_modules[epic_id] = {
                "status": status_text,
                "progress": progress_text,
                "recorded_done": recorded_done,
                "recorded_total": recorded_total,
                "raw_line": line
            }
            
    return roadmap_modules

def audit_module(task_dir: Path, roadmap_data: dict):
    """
    Kiểm toán chi tiết 1 thư mục TASK-XX hoặc EPIC-XX
    """
    epic_id_match = re.search(r"(?:TASK|EPIC)-\d{2,3}", task_dir.name)
    epic_id = epic_id_match.group(0) if epic_id_match else task_dir.name
    
    results = {
        "epic_id": epic_id,
        "dir_name": task_dir.name,
        "errors": [],
        "warnings": [],
        "info": {},
        "stats": {}
    }
    
    spec_file = task_dir / "spec.md"
    plan_file = task_dir / "plan.md"
    tasks_file = task_dir / "tasks.md"
    
    # 1. Kiểm tra sự tồn tại của bộ 3 tài liệu bắt buộc
    if not spec_file.exists():
        results["errors"].append(f"Thiếu file bắt buộc: spec.md")
    if not plan_file.exists():
        results["errors"].append(f"Thiếu file bắt buộc: plan.md")
    if not tasks_file.exists():
        results["errors"].append(f"Thiếu file bắt buộc: tasks.md")
        return results

    # 2. Phân tích tasks.md (chỉ đếm top-level tasks bắt đầu bằng '- [ ]' hoặc '- [x]')
    tasks_content = tasks_file.read_text(encoding="utf-8")
    task_lines = [l for l in tasks_content.splitlines() if re.match(r"^-\s*\[([ xX])\]", l)]
    
    done_count = sum(1 for l in task_lines if re.match(r"^-\s*\[[xX]\]", l))
    pending_count = sum(1 for l in task_lines if re.match(r"^-\s*\[ \]", l))
    total_tasks = len(task_lines)
    
    results["stats"]["tasks_total"] = total_tasks
    results["stats"]["tasks_done"] = done_count
    results["stats"]["tasks_pending"] = pending_count
    
    # Kiểm tra thứ tự Phase/Giai đoạn trong tasks.md
    phase_pattern = re.compile(r"^##\s*(?:Giai đoạn|Phase)\s*(\d+)[:\s—\-]+(.*)$", re.IGNORECASE)
    phases_found = []
    for idx, line in enumerate(tasks_content.splitlines(), start=1):
        m = phase_pattern.match(line)
        if m:
            p_num = int(m.group(1))
            p_title = m.group(2).strip()
            phases_found.append((p_num, p_title, idx))
            
    # Phát hiện thụt lùi số Phase hoặc trùng lặp số Phase
    seen_phases = {}
    last_phase_num = 0
    for p_num, p_title, line_no in phases_found:
        if p_num in seen_phases:
            prev_line_no = seen_phases[p_num]
            results["errors"].append(
                f"[tasks.md:L{line_no}] Trùng lặp Phase {p_num} ('{p_title}'). "
                f"Phase {p_num} đã xuất hiện tại dòng L{prev_line_no}!"
            )
        elif p_num < last_phase_num:
            results["errors"].append(
                f"[tasks.md:L{line_no}] Thứ tự Phase bị thụt lùi: Phase {p_num} đứng sau Phase {last_phase_num}!"
            )
        seen_phases[p_num] = line_no
        last_phase_num = max(last_phase_num, p_num)

    # 3. Phân tích spec.md
    if spec_file.exists():
        spec_content = spec_file.read_text(encoding="utf-8")
        
        # Kiểm tra Header Status
        status_match = re.search(r"\*\*Status\*\*:\s*([^\n\r]+)", spec_content)
        spec_status = status_match.group(1).strip() if status_match else "UNKNOWN"
        results["info"]["spec_status"] = spec_status
        
        # Nếu tasks đã 100% xong mà Status vẫn In Planning hoặc Draft
        if total_tasks > 0 and done_count == total_tasks:
            if "planning" in spec_status.lower() or "draft" in spec_status.lower():
                results["warnings"].append(
                    f"[spec.md] Header Status chưa cập nhật: 100% tasks đã xong nhưng Status vẫn là '{spec_status}'."
                )
                
        # Kiểm tra trùng lặp tiêu đề Delta trong spec.md
        spec_deltas = []
        delta_pattern = re.compile(r"^##\s*(Delta\s*[vV]?\d+|Kế Hoạch Triển Khai Delta\s*[vV]?\d+)(.*)$", re.IGNORECASE)
        for idx, line in enumerate(spec_content.splitlines(), start=1):
            dm = delta_pattern.match(line)
            if dm:
                v_name = dm.group(1).strip().upper()
                v_norm = re.sub(r"^(?:KẾ HOẠCH TRIỂN KHAI\s*)?DELTA\s*V?", "DELTA-V", v_name)
                spec_deltas.append((v_norm, line, idx))
                
        seen_deltas = {}
        for v_norm, raw_line, line_no in spec_deltas:
            if v_norm in seen_deltas:
                prev_line_no = seen_deltas[v_norm]
                results["errors"].append(
                    f"[spec.md:L{line_no}] Trùng lặp phiên bản Delta: '{v_norm}' đã xuất hiện tại L{prev_line_no}."
                )
            seen_deltas[v_norm] = line_no

    # 4. Phân tích plan.md
    if plan_file.exists():
        plan_content = plan_file.read_text(encoding="utf-8")
        
        # Kiểm tra Header Status
        p_status_match = re.search(r"\*\*Status\*\*:\s*([^\n\r]+)", plan_content)
        plan_status = p_status_match.group(1).strip() if p_status_match else "UNKNOWN"
        results["info"]["plan_status"] = plan_status
        
        if total_tasks > 0 and done_count == total_tasks:
            if "planning" in plan_status.lower() or "draft" in plan_status.lower():
                results["warnings"].append(
                    f"[plan.md] Header Status chưa cập nhật: 100% tasks đã xong nhưng Status vẫn là '{plan_status}'."
                )
                
        # Kiểm tra trùng lặp tiêu đề Delta trong plan.md
        plan_deltas = []
        p_delta_pattern = re.compile(r"^##\s*(?:Plan\s*)?(Delta\s*[vV]?\d+|Kế Hoạch Triển Khai Delta\s*[vV]?\d+)(.*)$", re.IGNORECASE)
        for idx, line in enumerate(plan_content.splitlines(), start=1):
            pm = p_delta_pattern.match(line)
            if pm:
                v_name = pm.group(1).strip().upper()
                v_norm = re.sub(r"^(?:KẾ HOẠCH TRIỂN KHAI\s*)?DELTA\s*V?", "DELTA-V", v_name)
                plan_deltas.append((v_norm, line, idx))
                
        seen_p_deltas = {}
        for v_norm, raw_line, line_no in plan_deltas:
            if v_norm in seen_p_deltas:
                prev_line_no = seen_p_deltas[v_norm]
                results["errors"].append(
                    f"[plan.md:L{line_no}] Trùng lặp phiên bản Delta: '{v_norm}' đã xuất hiện tại L{prev_line_no}."
                )
            seen_p_deltas[v_norm] = line_no

    # 5. Đối soát với ROADMAP.md
    if epic_id in roadmap_data:
        rm_info = roadmap_data[epic_id]
        results["info"]["roadmap_status"] = rm_info["status"]
        results["info"]["roadmap_total"] = rm_info["recorded_total"]
        results["info"]["roadmap_done"] = rm_info["recorded_done"]
        
        if rm_info["recorded_total"] is not None:
            if rm_info["recorded_total"] != total_tasks:
                results["errors"].append(
                    f"[LỆCH PHA ROADMAP] tasks.md có {total_tasks} tasks ({done_count} xong) "
                    f"nhưng ROADMAP.md chỉ ghi nhận {rm_info['recorded_total']} tasks ({rm_info['recorded_done']} xong). "
                    f"Lệch {abs(total_tasks - rm_info['recorded_total'])} tasks!"
                )
    else:
        results["warnings"].append(f"Epic {epic_id} chưa được đăng ký trong Master Registry của ROADMAP.md!")

    return results

def main():
    parser = argparse.ArgumentParser(description="TC IT Agent — Spec Integrity Linter")
    parser.add_argument("--dir", help="Đường dẫn thư mục dự án cần kiểm toán", default=None)
    args, _ = parser.parse_known_args()

    root = Path(args.dir).resolve() if args.dir else get_project_root()
    specs_dir = find_specs_dir(root)
    roadmap_path = find_roadmap_file(root, specs_dir)
    
    if not specs_dir.exists():
        print(f"{YELLOW}Không tìm thấy thư mục specs: {specs_dir} (bỏ qua linter){RESET}")
        sys.exit(0)
        
    roadmap_data = parse_roadmap(roadmap_path)
    
    # Tìm tất cả thư mục TASK-* hoặc EPIC-* hoặc có spec.md
    task_dirs = sorted([
        d for d in specs_dir.iterdir() 
        if d.is_dir() and (d.name.startswith("TASK-") or d.name.startswith("EPIC-") or (d / "spec.md").exists())
    ])
    
    if not task_dirs:
        print(f"{BLUE}Chưa có module nào trong {specs_dir}.{RESET}")
        sys.exit(0)
        
    total_errors = 0
    total_warnings = 0
    
    print(f"\n{BLUE}{BOLD}=============================================================================={RESET}")
    print(f"{BLUE}{BOLD}   TC IT AGENT — SPECIFICATION INTEGRITY & PARITY LINTER (AUTOMATED AUDITOR)   {RESET}")
    print(f"{BLUE}{BOLD}=============================================================================={RESET}\n")
    
    print(f"Quét thư mục: {specs_dir}")
    print(f"Tổng số modules phát hiện: {len(task_dirs)}\n")
    
    for task_dir in task_dirs:
        res = audit_module(task_dir, roadmap_data)
        
        err_len = len(res["errors"])
        warn_len = len(res["warnings"])
        total_errors += err_len
        total_warnings += warn_len
        
        status_color = GREEN if err_len == 0 else RED
        status_text = f"{GREEN}✓ PASS{RESET}" if err_len == 0 else f"{RED}✗ FAIL ({err_len} lỗi){RESET}"
        if warn_len > 0:
            status_text += f" {YELLOW}({warn_len} cảnh báo){RESET}"
            
        t_total = res["stats"].get("tasks_total", 0)
        t_done = res["stats"].get("tasks_done", 0)
        
        print(f"[{res['epic_id']}] {task_dir.name} ({t_done}/{t_total} tasks) -> {status_text}")
        
        for err in res["errors"]:
            print(f"   {RED}• LỖI: {err}{RESET}")
        for warn in res["warnings"]:
            print(f"   {YELLOW}• CẢNH BÁO: {warn}{RESET}")
            
    print(f"\n{BLUE}{BOLD}=============================================================================={RESET}")
    print(f"TỔNG KẾT KIỂM TOÁN SPEC:")
    print(f"- Tổng số lỗi nghiêm trọng (FAIL): {total_errors}")
    print(f"- Tổng số cảnh báo (WARNING):       {total_warnings}")
    
    if total_errors > 0:
        print(f"{RED}{BOLD}KẾT QUẢ: KHÔNG ĐẠT (SPEC LINTER FAILED). Cần chuẩn hóa dứt điểm các lỗi trên!{RESET}\n")
        sys.exit(1)
    else:
        print(f"{GREEN}{BOLD}KẾT QUẢ: 100% ĐẠT CHUẨN TOÀN VẸN VÀ ĐỒNG BỘ.{RESET}\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
