#!/usr/bin/env python3
"""
ENTERPRISE AGENT — ZERO-BYPASS GIT HOOK SENTINEL (block-no-verify)
Chốt chặn cứng ngăn chặn AI Agent tự ý bypass pre-commit / commit-msg / pre-push hooks:
- Phát hiện: --no-verify, -n (cho commit), -c core.hooksPath=...
- Chặn đứng mọi hành vi luồn lách để qua mặt linter, compiler hoặc test.
- Ghi vết vi phạm kỷ luật vào logs/guard-violations.log.

Mã trả về (Exit Codes):
  0: Lệnh hợp lệ (không chứa cờ bypass)
  2: PHÁT HIỆN VI PHẠM (Chặn đứng thực thi)
"""

import sys
import os
import re
import shlex
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "guard-violations.log")

RED = "\033[0;31m"
BOLD = "\033[1m"
YELLOW = "\033[1;33m"
NC = "\033[0m"

# Các cờ vi phạm bị cấm tuyệt đối
FORBIDDEN_FLAGS = {
    "--no-verify",
}

# Các pattern regex kiểm tra git config override nguy hiểm
FORBIDDEN_CONFIG_PATTERNS = [
    re.compile(r"core\.hookspath\s*=\s*(/dev/null|[\"']{2}|NUL|\$null)", re.IGNORECASE),
    re.compile(r"core\.hookspath\s*=\s*['\"]?(/tmp|temp)[\"']?", re.IGNORECASE),
]

def log_violation(trigger_type: str, raw_command: str, reason: str):
    """Ghi lại lịch sử vi phạm kỷ luật của Agent."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"[{timestamp}] [VIOLATION] [TYPE: {trigger_type}]\n"
        f"  Command : {raw_command.strip()}\n"
        f"  Reason  : {reason}\n"
        f"  Action  : BLOCKED (Exit code 2)\n"
        f"{'-'*70}\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def inspect_tokens(tokens: list) -> tuple[bool, str]:
    """Phân tích danh sách tokens của câu lệnh git."""
    if not tokens:
        return False, ""

    is_git = False
    git_subcmd = None
    
    # Tìm lệnh git và sub-command
    for i, tok in enumerate(tokens):
        base_tok = os.path.basename(tok).lower()
        if base_tok in ("git", "git.exe"):
            is_git = True
            # Tìm subcommand tiếp theo (commit, push, merge...)
            for next_tok in tokens[i+1:]:
                if not next_tok.startswith("-"):
                    git_subcmd = next_tok.lower()
                    break
            break

    # Kiểm tra config override: -c core.hooksPath=...
    for i, tok in enumerate(tokens):
        if tok == "-c" and i + 1 < len(tokens):
            target_cfg = tokens[i+1]
            for pat in FORBIDDEN_CONFIG_PATTERNS:
                if pat.search(target_cfg):
                    return True, f"Phát hiện cấu hình vô hiệu hóa Git Hooks: -c {target_cfg}"
        elif tok.startswith("-c") and "=" in tok:
            for pat in FORBIDDEN_CONFIG_PATTERNS:
                if pat.search(tok):
                    return True, f"Phát hiện cấu hình vô hiệu hóa Git Hooks: {tok}"

    # Kiểm tra các cờ bypass trực tiếp
    for i, tok in enumerate(tokens):
        # 1. Cờ --no-verify
        if tok in FORBIDDEN_FLAGS:
            return True, f"Phát hiện cờ bỏ qua kiểm tra chất lượng: {tok}"

        # 2. Cờ ngắn -n cho 'git commit'
        if is_git and git_subcmd == "commit":
            if tok == "-n":
                return True, "Phát hiện cờ ngắn '-n' (--no-verify) trong lệnh git commit"
            # Trường hợp gộp cờ: e.g. -anm "msg" hoặc -nm
            if tok.startswith("-") and not tok.startswith("--") and "n" in tok:
                return True, f"Phát hiện cờ 'n' (--no-verify) nằm trong cụm cờ: {tok}"

    return False, ""

def scan_command_string(cmd_str: str) -> tuple[bool, str]:
    """Phân tích chuỗi câu lệnh shell đầy đủ."""
    try:
        tokens = shlex.split(cmd_str)
    except Exception:
        tokens = cmd_str.split()
    return inspect_tokens(tokens)

def main():
    # Chế độ 1: Quét chuỗi lệnh truyền qua --cmd
    if len(sys.argv) >= 3 and sys.argv[1] == "--cmd":
        cmd_str = " ".join(sys.argv[2:])
        is_violation, reason = scan_command_string(cmd_str)
        if is_violation:
            print(f"\n{RED}{BOLD}[ENTERPRISE SECURITY GUARD] LỆNH BỊ CHẶN ĐỨNG!{NC}", file=sys.stderr)
            print(f"{RED}Lý do: {reason}{NC}", file=sys.stderr)
            print(f"{YELLOW}Kỷ luật Enterprise: Tuyệt đối CẤM sử dụng --no-verify hoặc bypass hooks.{NC}", file=sys.stderr)
            print(f"{YELLOW}Mã nguồn bắt buộc phải vượt qua 100% TypeCheck, Compiler và Quality Gates.{NC}\n", file=sys.stderr)
            log_violation("COMMAND_SCAN", cmd_str, reason)
            sys.exit(2)
        sys.exit(0)

    # Chế độ 2: Làm Wrapper trung gian cho lệnh git
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        is_violation, reason = inspect_tokens(args)
        if is_violation:
            cmd_repr = "git " + " ".join(args)
            print(f"\n{RED}{BOLD}[ENTERPRISE SECURITY GUARD] LỆNH GIT BỊ CHẶN ĐỨNG!{NC}", file=sys.stderr)
            print(f"{RED}Lý do: {reason}{NC}", file=sys.stderr)
            print(f"{YELLOW}Kỷ luật Enterprise: CẤM vượt rào bằng --no-verify hoặc bypass hook.{NC}", file=sys.stderr)
            log_violation("GIT_WRAPPER", cmd_repr, reason)
            sys.exit(2)
        
        # Nếu sạch, chạy git thật
        import subprocess
        real_git = "/usr/bin/git"
        if not os.path.exists(real_git):
            import shutil
            real_git = shutil.which("git") or "git"
        
        sys.exit(subprocess.call([real_git] + args))

    print("Usage: block-no-verify.py --cmd '<command>' OR block-no-verify.py <git args...>")
    sys.exit(0)

if __name__ == "__main__":
    main()
