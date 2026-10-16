#!/usr/bin/env python3
"""
ENTERPRISE AGENT — FACT-FORCING GATEKEEPER (fact-forcing-guard)
Cơ chế ép khai báo sự thật (Fact-Forcing) lấy cảm hứng từ GateGuard của ECC:
- Phạm vi áp dụng: TIER-1 CRITICAL FILES (Domain Entities, Database Migrations, RBAC, Specification).
- Nguyên lý: Ép Agent phải chứng minh ngữ cảnh (Ai đang gọi? Có phá vỡ CSDL/API không? Rollback thế nào?)
  TRƯỚC KHI được phép ghi đè các tệp sống còn của hệ thống.

Cách dùng:
  fact-forcing-guard.py --audit                 # Quét staged/modified files trong git
  fact-forcing-guard.py --check-file <path>     # Kiểm tra trước khi sửa một tệp
  fact-forcing-guard.py --submit-facts <json>   # Nộp fact-sheet hợp lệ để cấp quyền
"""

import sys
import os
import subprocess
import json
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
FACTS_DIR = os.path.join(PROJECT_ROOT, ".facts")

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
BOLD = "\033[1m"
NC = "\033[0m"

# Danh mục phân vùng Nhạy cảm cao Tier-1 (Domain Entities, Migrations, RBAC, Master Specs)
TIER_1_PATTERNS = [
    "/domain/",
    "/Domain/",
    "/migrations/",
    "/Migrations/",
    "/identity/",
    "/Identity/",
    "/rbac/",
    "/RBAC/",
    "/auth/",
    "/Auth/",
    "specs/spec.md",
    "Specification/",
    "docs/spec/",
]

def is_tier_1_file(filepath: str) -> bool:
    """Kiểm tra xem một file có thuộc Tier-1 Critical hay không."""
    normalized = filepath.replace("\\", "/")
    for pattern in TIER_1_PATTERNS:
        if pattern in normalized:
            return True
    return False

def get_modified_files() -> list[str]:
    """Lấy danh sách các file đang bị thay đổi trong git (staged + working tree)."""
    files = []
    # Quét root và các thư mục submodule nếu có
    candidate_repos = [PROJECT_ROOT]
    for sub in ("SourceCode", "backend", "frontend", "Specification", "src"):
        p = os.path.join(PROJECT_ROOT, sub)
        if os.path.exists(os.path.join(p, ".git")):
            candidate_repos.append(p)
            
    for r in candidate_repos:
        if os.path.exists(os.path.join(r, ".git")):
            try:
                out = subprocess.check_output(
                    ["git", "-C", r, "status", "--porcelain"],
                    stderr=subprocess.DEVNULL,
                    text=True
                )
                for line in out.splitlines():
                    if len(line) > 3:
                        path = line[3:].strip()
                        full_path = os.path.join(r, path)
                        rel_path = os.path.relpath(full_path, PROJECT_ROOT)
                        files.append(rel_path)
            except Exception:
                pass
    return list(set(files))

def verify_facts_for_file(filepath: str) -> tuple[bool, str]:
    """Kiểm tra xem tệp Tier-1 đã có bản khai Fact-Sheet hợp lệ chưa."""
    os.makedirs(FACTS_DIR, exist_ok=True)
    basename = os.path.basename(filepath)
    fact_file = os.path.join(FACTS_DIR, f"{basename}.facts.json")
    
    if not os.path.exists(fact_file):
        return False, (
            f"Thiếu Fact-Sheet cho tệp Tier-1 '{filepath}'.\n"
            f"Vui lòng nộp fact-sheet tại .facts/{basename}.facts.json với các trường bắt buộc:\n"
            f"  - importers: Danh sách module/hàm đang gọi\n"
            f"  - schema_impact: Ảnh hưởng schema CSDL / API contract\n"
            f"  - rollback_plan: Kế hoạch rollback nếu phát sinh lỗi"
        )
        
    try:
        with open(fact_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        required_fields = ["importers", "schema_impact", "rollback_plan"]
        for rf in required_fields:
            if rf not in data or not data[rf]:
                return False, f"Fact-Sheet {fact_file} thiếu trường bắt buộc: '{rf}'"
                
        return True, "Fact-Sheet hợp lệ và đầy đủ bằng chứng."
    except Exception as e:
        return False, f"Lỗi đọc Fact-Sheet: {str(e)}"

def cmd_audit():
    """Kiểm toán toàn bộ thay đổi đối với các tệp Tier-1."""
    modified = get_modified_files()
    tier_1_modified = [f for f in modified if is_tier_1_file(f)]
    
    if not tier_1_modified:
        print(f"{GREEN}✓ Không có tệp Tier-1 Critical nào bị sửa đổi.{NC}")
        sys.exit(0)
        
    print(f"\n{YELLOW}[FACT-FORCING GATEKEEPER] Phát hiện {len(tier_1_modified)} tệp Tier-1 bị can thiệp:{NC}")
    violations = []
    
    for f in tier_1_modified:
        valid, msg = verify_facts_for_file(f)
        if not valid:
            print(f"  {RED}✗ [CHƯA KHAI BÁO SỰ THẬT]{NC} {f}")
            violations.append((f, msg))
        else:
            print(f"  {GREEN}✓ [ĐÃ XÁC THỰC BẰNG CHỨNG]{NC} {f}")
            
    if violations:
        print(f"\n{RED}{BOLD}[LỖI KỶ LUẬT] Chặn đứng thao tác! Có tệp Tier-1 bị sửa ẩu khi chưa nộp Fact-Sheet:{NC}")
        for f, msg in violations:
            print(f"{RED}--- File: {f} ---{NC}\n{msg}\n")
        print(f"{YELLOW}Quy tắc ECC: Agent bắt buộc phải điều tra trước khi can thiệp vào tầng Domain/DB!{NC}\n")
        sys.exit(2)
    else:
        print(f"\n{GREEN}{BOLD}✓ Tất cả tệp Tier-1 đều có đầy đủ Fact-Sheet xác thực! Cho phép tiếp tục.{NC}\n")
        sys.exit(0)

def cmd_check_file(target_file: str):
    """Kiểm tra trước khi sửa một tệp cụ thể."""
    rel = os.path.relpath(target_file, PROJECT_ROOT)
    if not is_tier_1_file(rel):
        print(f"{GREEN}File '{rel}' thuộc vùng thông thường (Tier-2/3), không kích hoạt Fact-Forcing.{NC}")
        sys.exit(0)
        
    print(f"{YELLOW}[CẢNH BÁO TIER-1] Tệp '{rel}' thuộc phân vùng Lõi Sống Còn!{NC}")
    valid, msg = verify_facts_for_file(rel)
    if not valid:
        print(f"{RED}{BOLD}CHẶN QUYỀN SỬA ĐỔI:{NC}\n{msg}")
        sys.exit(2)
    else:
        print(f"{GREEN}Fact-Sheet đã được phê duyệt. Quyền sửa đổi được mở.{NC}")
        sys.exit(0)

def cmd_submit_facts(target_file: str, json_str: str):
    """Nộp Fact-Sheet cho một tệp Tier-1."""
    os.makedirs(FACTS_DIR, exist_ok=True)
    basename = os.path.basename(target_file)
    fact_file = os.path.join(FACTS_DIR, f"{basename}.facts.json")
    
    try:
        data = json.loads(json_str)
        data["submitted_at"] = datetime.now().isoformat()
        data["target_file"] = target_file
        with open(fact_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"{GREEN}✓ Đã nộp Fact-Sheet thành công cho '{basename}':{NC} {fact_file}")
    except Exception as e:
        print(f"{RED}Lỗi lưu Fact-Sheet: {str(e)}{NC}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(f"""
{BLUE}{BOLD}ENTERPRISE FACT-FORCING GATEKEEPER (ECC GateGuard Principle){NC}

Cách dùng:
  fact-forcing-guard.py --audit
  fact-forcing-guard.py --check-file <đường_dẫn_file>
  fact-forcing-guard.py --submit-facts <tên_file> '<chuỗi_json>'
""")
        sys.exit(0)
        
    arg = sys.argv[1]
    if arg == "--audit":
        cmd_audit()
    elif arg == "--check-file" and len(sys.argv) >= 3:
        cmd_check_file(sys.argv[2])
    elif arg == "--submit-facts" and len(sys.argv) >= 4:
        cmd_submit_facts(sys.argv[2], sys.argv[3])
    else:
        print(f"{RED}Lệnh hoặc tham số không đúng: {sys.argv}{NC}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
