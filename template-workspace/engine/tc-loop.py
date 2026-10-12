#!/usr/bin/env python3
"""
TC IT AGENT — AUTONOMOUS LOOP & E2E PIPELINE ENGINE (tc-loop)
Kế thừa tinh hoa từ bmad-loop (bmad-code-org/bmad-loop) & Spec-Kit Enterprise Framework.
Triết lý vận hành cốt lõi:
1. No-LLM-in-the-control-loop: Engine Python/Bash kiểm soát điều phối và trạng thái vòng lặp,
   LLM chỉ đóng vai trò chuyên gia thực thi công việc trong từng lượt gọi.
2. Fresh Context per session: Mỗi task khởi tạo process Agent CLI độc lập, nạp đúng grounding
   của task đó, triệt tiêu ô nhiễm ngữ cảnh (Context Pollution) và chống cạn kiệt token.
3. Deterministic Verify Gate: Chốt chặn kiểm tra toán học tĩnh (guard-rails, linter, tests thật)
   bắt buộc phải 100% Green trước khi nghiệm thu.
4. Atomic tasks.md tick & git commit: Chỉ đánh dấu [x] khi verify pass, commit git ngay cùng lúc
   để bảo đảm ma trận truy vết khép kín 1:1.
5. Blast Radius Guard: Giới hạn số file sửa đổi tối đa trong một task, ngăn chặn sửa lan tràn.
6. Auto-Retry with Failure Context: Tự động gom lỗi biên dịch/test từ lượt trước làm input cho lượt sau.
7. Attention Escalation: Dừng khẩn cấp, ghi sổ ATTENTION.md và bắn notification âm thanh khi lỗi quá số lần cho phép.
8. Native Tmux Multiplexer: Vận hành ngầm (Background daemon), theo dõi trực tiếp qua Attach session.
9. Macro E2E Pipeline: Tự động duyệt backlog ý tưởng từ BACKLOG.md, phân phối PO -> BA -> SA -> Dev -> QC.
"""

import os
import sys
import re
import json
import time
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Python 3.11+ có sẵn tomllib, fallback tomli
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

# ==============================================================================
# XÁC ĐỊNH PROJECT ROOT & ĐƯỜNG DẪN CẤU HÌNH
# ==============================================================================
def find_project_root() -> Path:
    """Tự động tìm thư mục gốc dự án (chứa .git, engine/policy.toml hoặc specs)."""
    current = Path(__file__).resolve().parent
    # Nếu file nằm trong engine/, thư mục cha của engine là project root
    if current.name == "engine":
        return current.parent
    # Quét ngược lên tìm .git hoặc policy.toml
    for p in [current, *current.parents]:
        if (p / ".git").exists() or (p / "engine" / "policy.toml").exists():
            return p
    return Path.cwd()

ROOT_DIR = find_project_root()
CONFIG_PATH = ROOT_DIR / "engine" / "policy.toml"
STATE_DIR = ROOT_DIR / ".tc-loop"
STATE_FILE = STATE_DIR / "state.json"
LOGS_DIR = STATE_DIR / "logs"
ATTENTION_FILE = STATE_DIR / "ATTENTION.md"
DEFAULT_TMUX_SESSION = "tc-loop"
DEFAULT_PIPELINE_SESSION = "tc-pipeline"

# ==============================================================================
# NATIVE TMUX MULTIPLEXER (ZERO EXTERNAL DEPENDENCY)
# ==============================================================================
class NativeTmuxMultiplexer:
    """Điều khiển tmux bằng subprocess POSIX chuẩn, không phụ thuộc thư viện ngoài."""
    def __init__(self):
        self.tmux_bin = shutil.which("tmux")

    def available(self) -> bool:
        return self.tmux_bin is not None

    def has_session(self, session_name: str) -> bool:
        if not self.available():
            return False
        res = subprocess.run(
            ["tmux", "has-session", "-t", session_name],
            capture_output=True,
            text=True
        )
        return res.returncode == 0

    def kill_session(self, session_name: str) -> bool:
        if not self.available():
            return False
        res = subprocess.run(
            ["tmux", "kill-session", "-t", session_name],
            capture_output=True,
            text=True
        )
        return res.returncode == 0

    def new_session(self, session_name: str, cwd: Path, cmd: str) -> bool:
        if not self.available():
            return False
        res = subprocess.run(
            ["tmux", "new-session", "-d", "-s", session_name, "-c", str(cwd), cmd],
            capture_output=True,
            text=True
        )
        return res.returncode == 0

# Tích hợp ưu tiên bmad_loop nếu có cài đặt, fallback sang NativeTmuxMultiplexer
try:
    from bmad_loop.adapters.tmux_backend import TmuxMultiplexer
    MUX = TmuxMultiplexer()
except Exception:
    MUX = NativeTmuxMultiplexer()

# Màu ANSI Terminal
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_GREEN = "\033[32m"
C_RED = "\033[31m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_CYAN = "\033[36m"
C_MAGENTA = "\033[35m"
C_GRAY = "\033[90m"

# ==============================================================================
# QUẢN TRỊ CẤU HÌNH POLICY
# ==============================================================================
def load_policy() -> dict:
    """Đọc cấu hình policy.toml hoặc tạo cấu hình mặc định chuẩn mực."""
    default_policy = {
        "project": {
            "name": "TC IT Enterprise Project"
        },
        "loop": {
            "project_root": ".",
            "task_specs_dir": "specs",
            "backlog_file": "backlog/BACKLOG.md",
            "basic_design_dir": "docs/01-basic-design",
            "max_attempts_per_task": 3,
            "session_timeout_seconds": 600,
            "blast_radius_max_files": 8,
            "auto_commit": True,
            "auto_advance": True,
        },
        "agents": {
            "cli": "auto",
            "dev_model": "sonnet",
            "review_model": "opus",
        },
        "verify": {
            "commands": [
                "bash scripts/guard-rails.sh"
            ]
        },
        "scm": {
            "isolation": "branch",
            "base_branch": "main",
            "branch_prefix": "loop/",
            "commit_prefix": "feat"
        },
        "escalation": {
            "notify_mac_desktop": True,
            "attention_file": ".tc-loop/ATTENTION.md"
        }
    }
    if CONFIG_PATH.exists() and tomllib:
        try:
            with open(CONFIG_PATH, "rb") as f:
                loaded = tomllib.load(f)
                for k, v in loaded.items():
                    if k in default_policy and isinstance(v, dict):
                        default_policy[k].update(v)
                    else:
                        default_policy[k] = v
        except Exception as e:
            print(f"{C_YELLOW}[!] Không đọc được policy.toml ({e}), dùng cấu hình mặc định.{C_RESET}")
    return default_policy

def ensure_state_dir():
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def notify_desktop(title: str, message: str):
    """Gửi notification âm thanh trên macOS."""
    try:
        cmd = f'display notification "{message}" with title "{title}" sound name "Glass"'
        subprocess.run(["osascript", "-e", cmd], capture_output=True, timeout=5)
    except Exception:
        pass

# ==============================================================================
# BÓC TÁCH TASKS & BACKLOG (REGEX DETERMINISTIC)
# ==============================================================================
class TaskItem:
    def __init__(self, raw_line: str, task_id: str, is_done: bool, tag: str, description: str, line_num: int):
        self.raw_line = raw_line
        self.task_id = task_id
        self.is_done = is_done
        self.tag = tag or ""
        self.description = description.strip()
        self.line_num = line_num

    def __repr__(self):
        status = "[x]" if self.is_done else "[ ]"
        return f"{status} {self.task_id} {self.tag} {self.description}"

def parse_tasks_md(tasks_file: Path) -> list[TaskItem]:
    """Đọc và bóc tách các task trong tasks.md (hỗ trợ cả bold, code ticks, tag)."""
    if not tasks_file.exists():
        return []
    tasks = []
    task_regex = re.compile(r"^-\s*\[([ xX])\]\s+[`*]*([A-Za-z0-9_.-]+)[`*]*\s*(?:\[([^\]]+)\])?\s*(.*)$")
    with open(tasks_file, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            match = task_regex.match(line.strip())
            if match:
                is_done = match.group(1).lower() == "x"
                task_id = match.group(2)
                tag = match.group(3) or ""
                desc = match.group(4)
                tasks.append(TaskItem(line, task_id, is_done, tag, desc, idx))
    return tasks

def update_task_in_file(tasks_file: Path, task_id: str, commit_hash: str = "") -> bool:
    """Đánh dấu [x] vào file tasks.md một cách nguyên tử."""
    if not tasks_file.exists():
        return False
    with open(tasks_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    task_regex = re.compile(rf"^-\s*\[ \]\s+[`*]*({re.escape(task_id)})[`*]*\b")
    updated = False
    new_lines = []
    for line in lines:
        if task_regex.search(line.strip()):
            suffix = f" [commit: {commit_hash[:7]}]" if commit_hash else ""
            new_line = re.sub(r"^-\s*\[ \]", "- [x]", line)
            if commit_hash and "[commit:" not in new_line:
                new_line = new_line.rstrip() + suffix + "\n"
            new_lines.append(new_line)
            updated = True
        else:
            new_lines.append(line)

    if updated:
        with open(tasks_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    return updated

class BacklogItem:
    def __init__(self, raw_line: str, item_id: str, is_done: bool, tag: str, title: str, line_num: int):
        self.raw_line = raw_line
        self.item_id = item_id
        self.is_done = is_done
        self.tag = tag or ""
        self.title = title.strip()
        self.line_num = line_num

    def __repr__(self):
        status = "[x]" if self.is_done else "[ ]"
        return f"{status} {self.item_id} {self.tag} {self.title}"

def resolve_backlog_file(policy: dict) -> Path:
    """Tự động tìm kiếm file backlog theo cấu hình và fallback."""
    cfg_backlog = policy.get("loop", {}).get("backlog_file", "backlog/BACKLOG.md")
    candidates = [
        ROOT_DIR / cfg_backlog,
        ROOT_DIR / "backlog" / "BACKLOG.md",
        ROOT_DIR / "BACKLOG.md",
        ROOT_DIR / "Specification" / "BACKLOG.md",
        ROOT_DIR / "backlog" / "ROADMAP.md",
        ROOT_DIR / "specs" / "ROADMAP.md"
    ]
    for c in candidates:
        if c.exists():
            return c
    # Fallback mặc định
    return ROOT_DIR / "backlog" / "BACKLOG.md"

def parse_backlog_md(backlog_file: Path) -> list[BacklogItem]:
    """Đọc và bóc tách các ý tưởng/CR trong BACKLOG.md."""
    if not backlog_file.exists():
        return []
    items = []
    item_regex = re.compile(r"^-\s*\[([ xX])\]\s+[`*]*([A-Za-z0-9_.-]+)[`*]*\s*(?:\[([^\]]+)\])?\s*:?\s*(.*)$")
    with open(backlog_file, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            match = item_regex.match(line.strip())
            if match:
                is_done = match.group(1).lower() == "x"
                item_id = match.group(2)
                tag = match.group(3) or ""
                title = match.group(4)
                items.append(BacklogItem(line, item_id, is_done, tag, title, idx))
    return items

def update_backlog_in_file(backlog_file: Path, item_id: str) -> bool:
    """Đánh dấu [x] vào file BACKLOG.md một cách nguyên tử."""
    if not backlog_file.exists():
        return False
    with open(backlog_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    item_regex = re.compile(rf"^-\s*\[ \]\s+[`*]*({re.escape(item_id)})[`*]*\b")
    updated = False
    new_lines = []
    for line in lines:
        if item_regex.search(line.strip()):
            new_line = re.sub(r"^-\s*\[ \]", "- [x]", line)
            new_lines.append(new_line)
            updated = True
        else:
            new_lines.append(line)
    if updated:
        with open(backlog_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
    return updated

def append_backlog_item(title: str, tag: str = "", backlog_file: Path = None, policy: dict = None) -> str:
    """Thêm một ý tưởng mới vào cuối BACKLOG.md."""
    if backlog_file is None:
        backlog_file = resolve_backlog_file(policy or load_policy())
    backlog_file.parent.mkdir(parents=True, exist_ok=True)
    items = parse_backlog_md(backlog_file)
    next_num = len(items) + 1
    item_id = f"IDEA-{next_num:02d}"
    tag_str = f"[{tag}] " if tag else ""
    new_line = f"- [ ] {item_id} {tag_str}: {title.strip()}\n"
    with open(backlog_file, "a", encoding="utf-8") as f:
        f.write(new_line)
    return item_id

def run_command(cmd: str, cwd: Path = ROOT_DIR, timeout: int = 300) -> tuple[int, str, str]:
    """Chạy command shell xác thực, trả về (code, stdout, stderr)."""
    p = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout
    )
    return p.returncode, p.stdout, p.stderr

# ==============================================================================
# ĐIỀU PHỐI VÒNG LẶP CHO 1 EPIC (MICRO LOOP ENGINE)
# ==============================================================================
class LoopEngine:
    def __init__(self, spec_dir_name: str, policy: dict):
        self.spec_dir_name = spec_dir_name
        self.policy = policy
        ensure_state_dir()

        # Xác định thư mục specs
        task_specs_dir = self.policy["loop"].get("task_specs_dir", "specs")
        specs_base = ROOT_DIR / task_specs_dir
        if not specs_base.exists() and (ROOT_DIR / "SourceCode" / "specs").exists():
            specs_base = ROOT_DIR / "SourceCode" / "specs"

        self.spec_dir = specs_base / self.spec_dir_name
        self.tasks_file = self.spec_dir / "tasks.md"
        self.plan_file = self.spec_dir / "plan.md"
        self.spec_file = self.spec_dir / "spec.md"

    def get_state(self) -> dict:
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "spec": self.spec_dir_name,
            "active_task_id": None,
            "status": "IDLE",
            "attempts": 0,
            "last_error": None,
            "updated_at": datetime.now().isoformat()
        }

    def save_state(self, state: dict):
        state["updated_at"] = datetime.now().isoformat()
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def verify_gates(self) -> tuple[bool, str]:
        """Thực thi các lệnh verify toán học tĩnh cấu hình trong policy.toml."""
        commands = self.policy.get("verify", {}).get("commands", [])
        for cmd in commands:
            code, stdout, stderr = run_command(cmd, cwd=ROOT_DIR)
            if code != 0:
                output = (stdout + "\n" + stderr).strip()
                return False, f"Command thất bại: {cmd}\nOutput:\n{output}"
        return True, "All Verify Gates Passed 100% Green."

    def check_blast_radius(self) -> tuple[bool, list[str]]:
        """Kiểm tra số file bị thay đổi (Blast Radius)."""
        max_files = self.policy["loop"].get("blast_radius_max_files", 8)
        code, stdout, _ = run_command("git status --porcelain", cwd=ROOT_DIR)
        if code != 0:
            return True, []
        changed = [line.strip().split()[-1] for line in stdout.splitlines() if line.strip()]
        # Lọc bỏ các file log hoặc state
        changed = [f for f in changed if not f.startswith(".tc-loop") and not f.startswith(".nacen-loop")]
        if len(changed) > max_files:
            return False, changed
        return True, changed

    def log_attention(self, task_id: str, reason: str, details: str):
        """Ghi nhận vào ATTENTION.md khi task bị tắc nghẽn."""
        msg = f"""
## [ATTENTION] Task {task_id} bị kẹt - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Epic**: {self.spec_dir_name}
- **Lý do**: {reason}
- **Chi tiết**:
```
{details}
```
---
"""
        with open(ATTENTION_FILE, "a", encoding="utf-8") as f:
            f.write(msg)
        if self.policy["escalation"].get("notify_mac_desktop", True):
            notify_desktop(f"TC-Loop: {task_id} FAILED", f"{reason}. Đã dừng để người can thiệp.")

    def resolve_agent_cli(self) -> tuple[str, str | None]:
        """Tự động phát hiện CLI agent có sẵn (claude, agy, cursor...)."""
        cfg_cli = self.policy.get("agents", {}).get("cli", "auto").lower()

        # 1. claude
        if cfg_cli in ["claude", "auto"]:
            claude_path = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
            if os.path.exists(str(claude_path)) and os.access(str(claude_path), os.X_OK):
                return "claude", str(claude_path)

        # 2. agy (Google Antigravity)
        if cfg_cli in ["agy", "auto"]:
            agy_path = shutil.which("agy")
            if agy_path:
                return "agy", agy_path

        # 3. Fallback
        if shutil.which("claude"):
            return "claude", shutil.which("claude")
        if shutil.which("agy"):
            return "agy", shutil.which("agy")

        return "none", None

    def build_task_prompt(self, task: TaskItem, previous_error: str = "") -> str:
        """Sinh prompt có cấu trúc chặt chẽ nạp kỹ năng dev-code theo Hiến pháp."""
        project_name = self.policy.get("project", {}).get("name", "TC IT Enterprise Project")
        error_context = ""
        if previous_error:
            error_context = f"""
[LƯU Ý LỖI TỪ LẦN THỬ TRƯỚC - BẮT BUỘC KHẮC PHỤC TRIỆT ĐỂ]
Hệ thống kiểm thử báo lỗi sau:
{previous_error[:2500]}
Hãy đọc kỹ thông báo lỗi trên để sửa đúng căn nguyên, không lặp lại lỗi cũ.
"""
        prompt = f"""Bạn là Senior Full-Stack Developer trong dự án {project_name}.
Nhiệm vụ: Thực thi triệt để và trọn vẹn task kỹ thuật sau:
- Epic: {self.spec_dir_name}
- Task ID: {task.task_id} {task.tag}
- Mô tả: {task.description}

TÀI LIỆU THAM CHIẾU BẮT BUỘC (GROUNDING):
- Đặc tả yêu cầu: {self.spec_file.relative_to(ROOT_DIR) if self.spec_file.exists() else 'spec.md'}
- Bản kế hoạch kiến trúc: {self.plan_file.relative_to(ROOT_DIR) if self.plan_file.exists() else 'plan.md'}
- Danh mục công việc: {self.tasks_file.relative_to(ROOT_DIR) if self.tasks_file.exists() else 'tasks.md'}
- Hiến pháp dự án: AGENTS.md & constitution.md (Clean Architecture, Zero-Mock, 5 UX states, Scoped RBAC)

{error_context}
QUY CHUẨN KỸ THUẬT BẮT BUỘC:
1. Đọc kỹ spec.md và plan.md trước khi viết mã để đảm bảo đúng schema CSDL/API và logic nghiệp vụ.
2. Viết mã nguồn thực tế, chất lượng cao, tuyệt đối không tạo mock ngầm trên frontend (Zero-Mock discipline).
3. Giữ bán kính thay đổi file tối thiểu (Blast Radius <= {self.policy['loop'].get('blast_radius_max_files', 8)} files).
4. Đảm bảo toàn bộ mã nguồn biên dịch thành công 0 cảnh báo/lỗi và vượt qua các bài kiểm thử liên quan.
5. Khi hoàn thành, tóm tắt ngắn gọn các file đã tạo/sửa.
"""
        return prompt

    def invoke_agent(self, task: TaskItem, attempt_num: int, previous_error: str = "", custom_prompt: str = "") -> tuple[bool, str]:
        """Triệu hồi Agent CLI để lập trình task với Fresh Context độc lập."""
        cli_type, binary_path = self.resolve_agent_cli()
        if not binary_path:
            return False, f"Không tìm thấy Agent CLI khả dụng ({cli_type}) trên PATH."

        prompt = custom_prompt if custom_prompt else self.build_task_prompt(task, previous_error)
        timeout = self.policy.get("loop", {}).get("session_timeout_seconds", 600)
        dev_model = self.policy.get("agents", {}).get("dev_model", "sonnet")

        agent_log_file = LOGS_DIR / f"{task.task_id}_attempt_{attempt_num}_agent.log"

        if cli_type == "claude":
            cmd = [
                binary_path,
                "-p", prompt,
                "--permission-mode", "bypassPermissions",
            ]
            if dev_model:
                cmd.extend(["--model", dev_model])
        elif cli_type == "agy":
            cmd = [
                binary_path,
                "-p", prompt,
                "--dangerously-skip-permissions"
            ]
        else:
            return False, f"Chưa hỗ trợ CLI type: {cli_type}"

        try:
            p = subprocess.run(
                cmd,
                cwd=ROOT_DIR,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            output = p.stdout or p.stderr or ""
            with open(agent_log_file, "w", encoding="utf-8") as f:
                f.write(f"=== STDOUT ===\n{p.stdout}\n=== STDERR ===\n{p.stderr}\n")

            if p.returncode != 0:
                if "OAuth access token has expired" in output or "Failed to authenticate" in output:
                    return False, "AUTH_EXPIRED: Token Claude Code đã hết hạn (chạy 'claude login' để đăng nhập lại)"
                return False, output[:300]

            return True, output
        except subprocess.TimeoutExpired:
            return False, f"Agent CLI timeout sau {timeout} giây."
        except Exception as e:
            return False, f"Lỗi khởi chạy Agent CLI: {str(e)}"

    def run_loop(self, max_tasks: int = 999, dry_run: bool = False):
        """Vòng lặp tự trị cốt lõi: Pick -> Invoke Agent -> Verify Gates -> Commit -> Tick."""
        state = self.get_state()
        state["spec"] = self.spec_dir_name
        tasks = parse_tasks_md(self.tasks_file)
        if not tasks:
            print(f"{C_RED}[X] Không tìm thấy task nào trong {self.tasks_file}{C_RESET}")
            return

        cli_type, cli_path = self.resolve_agent_cli()
        project_name = self.policy.get("project", {}).get("name", "TC IT Enterprise Project")
        print(f"\n{C_CYAN}{C_BOLD}=== KHỞI ĐỘNG TC IT AGENT AUTONOMOUS LOOP ==={C_RESET}")
        print(f"• Dự án        : {C_YELLOW}{project_name}{C_RESET}")
        print(f"• Epic         : {C_YELLOW}{self.spec_dir_name}{C_RESET}")
        print(f"• Agent Runner : {C_GREEN}{cli_type} ({cli_path or 'Chưa cấu hình'}){C_RESET}")
        print(f"• Tổng số task : {len(tasks)} | Chưa xong: {len([t for t in tasks if not t.is_done])}")
        print(f"• Verify checks: {len(self.policy['verify']['commands'])} chốt chặn\n")

        executed_count = 0
        for task in tasks:
            if task.is_done:
                continue
            if executed_count >= max_tasks:
                print(f"{C_YELLOW}[!] Đã đạt giới hạn {max_tasks} task của phiên này. Tạm dừng.{C_RESET}")
                break

            state["active_task_id"] = task.task_id
            state["status"] = "IN_PROGRESS"
            state["attempts"] = 0
            self.save_state(state)

            print(f"\n{C_BLUE}{C_BOLD}▶ Đang xử lý task: {task.task_id} {task.tag} {task.description}{C_RESET}")

            if dry_run:
                print(f"{C_GRAY}  [DRY-RUN] Giả lập thực thi task {task.task_id} (không sửa file)...{C_RESET}")
                executed_count += 1
                continue

            max_attempts = self.policy["loop"].get("max_attempts_per_task", 3)
            task_success = False
            previous_error = ""

            while state["attempts"] < max_attempts:
                state["attempts"] += 1
                self.save_state(state)
                attempt_num = state["attempts"]
                print(f"  ┌─ Attempt {attempt_num}/{max_attempts}...")

                # 1. Gọi Agent CLI thực thi
                if cli_path:
                    print(f"  ├─ {C_CYAN}🤖 Đang gọi Agent CLI ({cli_type}) thực thi task...{C_RESET}")
                    agent_ok, agent_log = self.invoke_agent(task, attempt_num, previous_error)
                    if not agent_ok:
                        print(f"  ├─ {C_YELLOW}⚠ Agent phản hồi cảnh báo ({agent_log.strip()}){C_RESET}")
                        if "AUTH_EXPIRED" in agent_log:
                            print(f"  ├─ {C_CYAN}ℹ Tự động chuyển sang đối soát mã nguồn thực tế qua Verify Gates...{C_RESET}")
                    else:
                        print(f"  ├─ {C_GREEN}✓ Agent đã hoàn tất lượt sinh mã{C_RESET}")
                else:
                    print(f"  ├─ {C_YELLOW}⚠ Không có Agent CLI, chuyển thẳng sang Verify Gates...{C_RESET}")

                # 2. Chạy Verify Gates kiểm tra
                print(f"  ├─ {C_CYAN}🔍 Chạy Verify Gates kiểm thử mã nguồn...{C_RESET}")
                passed, msg = self.verify_gates()
                if passed:
                    # Kiểm tra Blast Radius
                    ok_radius, changed = self.check_blast_radius()
                    if not ok_radius:
                        print(f"  ├─ {C_RED}[X] Vi phạm Blast Radius: Thay đổi {len(changed)} files (tối đa {self.policy['loop']['blast_radius_max_files']}){C_RESET}")
                        self.log_attention(task.task_id, "Vi phạm Blast Radius", f"Files: {changed}")
                        break

                    # Tick [x] vào tasks.md
                    update_task_in_file(self.tasks_file, task.task_id)

                    # Tạo Git commit nguyên tử
                    commit_hash = ""
                    if self.policy["scm"].get("auto_commit", True):
                        commit_msg = f"feat({self.spec_dir_name}): [{task.task_id}] {task.description}"
                        run_command(f'git add -A && git commit -m "{commit_msg}" --allow-empty', cwd=ROOT_DIR)
                        _, hash_out, _ = run_command("git rev-parse --short HEAD", cwd=ROOT_DIR)
                        commit_hash = hash_out.strip()
                        print(f"  ├─ {C_GREEN}✓ Git Commit: {commit_hash} - {commit_msg}{C_RESET}")

                    print(f"  └─ {C_GREEN}✓ HOÀN TẤT TASK {task.task_id} -> Đã tick [x]{C_RESET}")
                    task_success = True
                    executed_count += 1
                    break
                else:
                    print(f"  ├─ {C_YELLOW}⚠ Gate kiểm thử chưa đạt:{C_RESET}\n     {msg[:200]}...")
                    previous_error = msg
                    err_log = LOGS_DIR / f"{task.task_id}_attempt_{attempt_num}_verify.log"
                    with open(err_log, "w", encoding="utf-8") as f:
                        f.write(msg)
                    time.sleep(2)

            if not task_success:
                print(f"\n{C_RED}[!] Task {task.task_id} thất bại sau {max_attempts} lần thử. Dừng khẩn cấp để người can thiệp.{C_RESET}")
                state["status"] = "BLOCKED"
                self.save_state(state)
                self.log_attention(task.task_id, f"Thất bại sau {max_attempts} attempts", "Vui lòng kiểm tra log tại .tc-loop/logs/")
                break

        if state.get("status") != "BLOCKED":
            state["status"] = "IDLE"
            state["active_task_id"] = None
            self.save_state(state)

        print(f"\n{C_GREEN}{C_BOLD}=== PHIÊN CHẠY KẾT THÚC. ĐÃ HOÀN TẤT {executed_count} TASK ==={C_RESET}\n")

    def print_dashboard(self):
        """Hiển thị bảng điều khiển TUI Terminal trực quan."""
        tasks = parse_tasks_md(self.tasks_file)
        state = self.get_state()
        done_count = sum(1 for t in tasks if t.is_done)
        total_count = len(tasks)
        pct = (done_count / total_count * 100) if total_count > 0 else 0

        project_name = self.policy.get("project", {}).get("name", "TC IT Enterprise Project")
        print(f"\n{C_CYAN}{C_BOLD}╔══════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_CYAN}{C_BOLD}║                 TC IT AGENT AUTONOMOUS LOOP DASHBOARD                            ║{C_RESET}")
        print(f"{C_CYAN}{C_BOLD}╚══════════════════════════════════════════════════════════════════════════════════╝{C_RESET}")
        print(f"  • Dự án       : {C_YELLOW}{project_name}{C_RESET}")
        print(f"  • Epic Mục Tiêu: {C_YELLOW}{self.spec_dir_name}{C_RESET}")
        print(f"  • Trạng Thái   : {C_GREEN if state.get('status') == 'IDLE' else C_YELLOW}{state.get('status')}{C_RESET}")
        print(f"  • Task Hiện Tại: {C_CYAN}{state.get('active_task_id') or 'Không'}{C_RESET}")
        print(f"  • Tiến Độ Tổng : [{C_GREEN}{'='*int(pct//5)}{C_GRAY}{'-'*(20 - int(pct//5))}{C_RESET}] {C_BOLD}{done_count}/{total_count} tasks ({pct:.1f}%){C_RESET}\n")

        print(f"{C_BOLD}{'STT':<4} {'TASK ID':<12} {'LOẠI':<8} {'MÔ TẢ CÔNG VIỆC':<45} {'TRẠNG THÁI':<10}{C_RESET}")
        print(f"{C_GRAY}{'-'*85}{C_RESET}")
        for idx, t in enumerate(tasks, start=1):
            status = f"{C_GREEN}✓ DONE{C_RESET}" if t.is_done else f"{C_GRAY}○ PENDING{C_RESET}"
            desc = t.description[:42] + "..." if len(t.description) > 42 else t.description
            print(f"{idx:<4} {t.task_id:<12} {t.tag:<8} {desc:<45} {status}")
        print(f"{C_GRAY}{'-'*85}{C_RESET}\n")

# ==============================================================================
# TÌM KIẾM VÀ ĐIỀU PHỐI EPIC
# ==============================================================================
def resolve_spec_name(query: str = "", policy: dict = None) -> str:
    """Tìm thư mục Epic trong thư mục specs dựa trên từ khóa hoặc số thứ tự."""
    if policy is None:
        policy = load_policy()
    task_specs_dir = policy["loop"].get("task_specs_dir", "specs")
    specs_base = ROOT_DIR / task_specs_dir
    if not specs_base.exists() and (ROOT_DIR / "SourceCode" / "specs").exists():
        specs_base = ROOT_DIR / "SourceCode" / "specs"

    if not specs_base.exists():
        return ""

    epics = [d.name for d in specs_base.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if not query:
        return find_default_spec(policy)

    q = query.strip()
    # 1. Tìm khớp chính xác
    if q in epics:
        return q

    # 2. Tìm theo số: "01", "1", "07"...
    if q.isdigit():
        num_str = f"{int(q):02d}"
        for ep in epics:
            if f"TASK-{num_str}" in ep or f"EPIC-{num_str}" in ep or ep.startswith(f"{num_str}_") or ep.startswith(num_str):
                return ep

    # 3. Tìm không phân biệt hoa thường
    for ep in epics:
        if q.lower() in ep.lower():
            return ep

    return query

def resolve_epic_from_text(text: str, policy: dict = None) -> str:
    """Tự động phân tích chuỗi mô tả để tìm mã Epic phù hợp."""
    m = re.search(r"\b(TASK|EPIC)-?(\d{1,2})\b", text, re.IGNORECASE)
    if m:
        num = int(m.group(2))
        return resolve_spec_name(f"{num:02d}", policy)
    m2 = re.search(r"\b(\d{1,2})\b", text)
    if m2:
        return resolve_spec_name(m2.group(1), policy)
    return ""

def find_default_spec(policy: dict = None) -> str:
    """Tìm Epic mặc định chưa hoàn thành hoặc gần nhất."""
    if policy is None:
        policy = load_policy()
    task_specs_dir = policy["loop"].get("task_specs_dir", "specs")
    specs_base = ROOT_DIR / task_specs_dir
    if not specs_base.exists() and (ROOT_DIR / "SourceCode" / "specs").exists():
        specs_base = ROOT_DIR / "SourceCode" / "specs"

    if not specs_base.exists():
        return ""

    epics = sorted([d.name for d in specs_base.iterdir() if d.is_dir() and not d.name.startswith(".")])
    # Ưu tiên Epic có task chưa xong
    for ep in epics:
        tasks_file = specs_base / ep / "tasks.md"
        if tasks_file.exists():
            tasks = parse_tasks_md(tasks_file)
            if any(not t.is_done for t in tasks):
                return ep
    return epics[0] if epics else ""

# ==============================================================================
# MACRO PIPELINE ENGINE (PO -> BA -> SA -> DEV -> QC E2E)
# ==============================================================================
class PipelineEngine:
    def __init__(self, policy: dict):
        self.policy = policy
        self.backlog_file = resolve_backlog_file(policy)

    def print_backlog(self):
        items = parse_backlog_md(self.backlog_file)
        done_count = sum(1 for i in items if i.is_done)
        total_count = len(items)
        pct = (done_count / total_count * 100) if total_count > 0 else 0

        project_name = self.policy.get("project", {}).get("name", "TC IT Enterprise Project")
        print(f"\n{C_CYAN}{C_BOLD}╔══════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_CYAN}{C_BOLD}║                 TC IT AGENT E2E AUTONOMOUS PIPELINE DASHBOARD                    ║{C_RESET}")
        print(f"{C_CYAN}{C_BOLD}╚══════════════════════════════════════════════════════════════════════════════════╝{C_RESET}")
        print(f"  • Dự án         : {C_YELLOW}{project_name}{C_RESET}")
        print(f"  • Nguồn Backlog : {C_YELLOW}{self.backlog_file.relative_to(ROOT_DIR) if self.backlog_file.is_relative_to(ROOT_DIR) else self.backlog_file}{C_RESET}")
        print(f"  • Tiến Độ Tổng  : [{C_GREEN}{'='*int(pct//5)}{C_GRAY}{'-'*(20 - int(pct//5))}{C_RESET}] {C_BOLD}{done_count}/{total_count} items ({pct:.1f}%){C_RESET}\n")

        print(f"{C_BOLD}{'STT':<4} {'ID':<10} {'LOẠI':<12} {'MÔ TẢ YÊU CẦU / Ý TƯỞNG':<45} {'TRẠNG THÁI':<10}{C_RESET}")
        print(f"{C_GRAY}{'-'*85}{C_RESET}")
        for idx, it in enumerate(items, start=1):
            status = f"{C_GREEN}✓ DONE{C_RESET}" if it.is_done else f"{C_GRAY}○ PENDING{C_RESET}"
            title = it.title[:42] + "..." if len(it.title) > 42 else it.title
            print(f"{idx:<4} {it.item_id:<10} {it.tag:<12} {title:<45} {status}")
        print(f"{C_GRAY}{'-'*85}{C_RESET}\n")

    def run_pipeline(self, dry_run: bool = False):
        """Vòng lặp Macro E2E: Duyệt từng ý tưởng/CR trong BACKLOG.md -> PO -> BA -> SA -> Dev -> QC."""
        items = parse_backlog_md(self.backlog_file)
        pending = [i for i in items if not i.is_done]
        if not pending:
            print(f"\n{C_GREEN}✓ Không có ý tưởng hoặc CR nào đang chờ trong {self.backlog_file.name}!{C_RESET}\n")
            return

        print(f"\n{C_CYAN}{C_BOLD}╔══════════════════════════════════════════════════════════════════════════════════╗{C_RESET}")
        print(f"{C_CYAN}{C_BOLD}║          KHỞI ĐỘNG VÒNG LẶP TOÀN TRÌNH E2E PIPELINE (PO -> BA -> DEV -> QC)     ║{C_RESET}")
        print(f"{C_CYAN}{C_BOLD}╚══════════════════════════════════════════════════════════════════════════════════╝{C_RESET}")
        print(f"• Số lượng yêu cầu cần xử lý: {C_YELLOW}{len(pending)}{C_RESET}\n")

        task_specs_dir = self.policy["loop"].get("task_specs_dir", "specs")
        specs_base = ROOT_DIR / task_specs_dir
        if not specs_base.exists() and (ROOT_DIR / "SourceCode" / "specs").exists():
            specs_base = ROOT_DIR / "SourceCode" / "specs"

        basic_design_dir = self.policy["loop"].get("basic_design_dir", "docs/01-basic-design")
        bd_base = ROOT_DIR / basic_design_dir

        for idx, item in enumerate(pending, start=1):
            print(f"\n{C_MAGENTA}{C_BOLD}======================================================================{C_RESET}")
            print(f"{C_MAGENTA}{C_BOLD}▶ [YÊU CẦU {idx}/{len(pending)}] {item.item_id}: {item.title}{C_RESET}")
            print(f"{C_MAGENTA}{C_BOLD}======================================================================{C_RESET}")

            # 1. PO Triage & Routing
            target_epic = resolve_epic_from_text(f"{item.tag} {item.title}", self.policy)
            print(f"  • {C_CYAN}[PO po-pm]{C_RESET} Phân tích đề bài -> Ánh xạ Epic: {C_YELLOW}{target_epic or 'TÍNH NĂNG MỚI'}{C_RESET}")

            if not target_epic:
                # Nếu chưa có Epic, tạo mã mới từ ID
                target_epic = f"EPIC-{item.item_id}"
                print(f"  • {C_CYAN}Khởi tạo Epic mới: {target_epic}{C_RESET}")

            bd_path = bd_base / target_epic / "README.md"
            tasks_path = specs_base / target_epic / "tasks.md"

            # 2. Xử lý Phân nhánh Mới vs Change Request
            if not bd_path.exists() and not tasks_path.exists():
                print(f"  • {C_YELLOW}[NHÁNH A - TÍNH NĂNG MỚI]{C_RESET} Khởi tạo Basic Design & Spec Kit...")
                if not dry_run:
                    engine_micro = LoopEngine(target_epic, self.policy)
                    cli_type, binary_path = engine_micro.resolve_agent_cli()
                    if binary_path:
                        prompt_ba = f"""Bạn là BA Agent (Senior Business Analyst).
Đề bài từ PO: {item.title} (Mã Epic: {target_epic}).
Nhiệm vụ:
1. Xây dựng tài liệu Thiết Kế Cơ Sở (Basic Design) tại {basic_design_dir}/{target_epic}/README.md theo kỹ năng ba-design (C4 Context, Domain Model, Story Mapping).
2. Soạn thảo SRS 7 mục tại {task_specs_dir}/{target_epic}/spec.md (REQ-, BR-, DB-, Scoped RBAC).
3. Lập kế hoạch kiến trúc tại {task_specs_dir}/{target_epic}/plan.md (sa-plan).
4. Phân rã danh sách công việc kiểm chứng tại {task_specs_dir}/{target_epic}/tasks.md (dev-tasks).
"""
                        engine_micro.invoke_agent(TaskItem("", f"BA-{item.item_id}", False, "[BA]", item.title, 0), 1, "", custom_prompt=prompt_ba)
            else:
                print(f"  • {C_GREEN}[NHÁNH B - CHANGE REQUEST]{C_RESET} Cập nhật phi phá hủy qua Delta...")
                existing_tasks = parse_tasks_md(tasks_path)
                has_pending = any(not t.is_done for t in existing_tasks)
                if not has_pending:
                    if not dry_run:
                        engine_micro = LoopEngine(target_epic, self.policy)
                        cli_type, binary_path = engine_micro.resolve_agent_cli()
                        if binary_path:
                            prompt_delta = f"""Bạn là Software Architect (TechLead/SA Agent).
Change Request: {item.title} cho Epic {target_epic}.
Nhiệm vụ:
1. Quét ma trận truy vết khép kín (traceability-auditor).
2. Thực hiện quy trình speckit-delta / wf-delta cho {task_specs_dir}/{target_epic}/:
   - Ghi Delta section vào spec.md.
   - Cập nhật plan.md với phương án non-destructive migration.
   - Bổ sung các tasks Delta [BE]/[FE]/[Test] mới vào cuối file tasks.md (bảo toàn các task cũ).
"""
                            engine_micro.invoke_agent(TaskItem("", f"DELTA-{item.item_id}", False, "[DELTA]", item.title, 0), 1, "", custom_prompt=prompt_delta)

            # 3. Kích hoạt Micro Loop cho Epic
            print(f"\n  • {C_CYAN}[THỰC THI TỰ TRỊ]{C_RESET} Kích hoạt Micro Loop cho {target_epic}...")
            engine_micro = LoopEngine(target_epic, self.policy)
            engine_micro.run_loop(dry_run=dry_run)

            # 4. Nghiệm thu Gate 5 DoD
            tasks_after = parse_tasks_md(tasks_path)
            if tasks_after and all(t.is_done for t in tasks_after):
                print(f"\n  • {C_GREEN}✓ [PO SIGN-OFF]{C_RESET} 100% Tasks của {target_epic} đã hoàn tất. Đóng item {item.item_id}!")
                update_backlog_in_file(self.backlog_file, item.item_id)
                notify_desktop("TC-Pipeline", f"Hoàn tất toàn trình: {item.item_id}")
            else:
                print(f"\n  • {C_YELLOW}⚠ Item {item.item_id} còn task chưa xong hoặc cần người can thiệp.{C_RESET}")

        print(f"\n{C_GREEN}{C_BOLD}=== PHIÊN CHẠY TOÀN TRÌNH E2E PIPELINE KẾT THÚC ==={C_RESET}\n")

# ==============================================================================
# QUẢN TRỊ TMUX BACKGROUND RUNNER
# ==============================================================================
def launch_tmux_bg(spec_name: str, max_tasks: int, dry_run: bool = False) -> bool:
    """Khởi chạy vòng lặp ngầm trong tmux session."""
    if not MUX or not MUX.available():
        print(f"{C_RED}[X] Tmux không khả dụng trên hệ thống. Chạy trực tiếp foreground.{C_RESET}")
        return False

    session_name = DEFAULT_TMUX_SESSION
    if MUX.has_session(session_name):
        print(f"{C_YELLOW}[!] Session tmux '{session_name}' đã tồn tại. Đang dừng session cũ...{C_RESET}")
        MUX.kill_session(session_name)
        time.sleep(1)

    script_path = ROOT_DIR / "engine" / "tc-loop.py"
    dry_flag = " --dry-run" if dry_run else ""
    cmd = f"python3 '{script_path}' run --spec '{spec_name}' --max-tasks {max_tasks}{dry_flag}"

    MUX.new_session(session_name, ROOT_DIR, cmd)
    print(f"\n{C_GREEN}{C_BOLD}✓ ĐÃ KHỞI CHẠY VÒNG LẶP ÂM THẦM TRONG TMUX SESSION: {session_name}{C_RESET}")
    print(f"• Epic đang chạy : {C_YELLOW}{spec_name}{C_RESET}")
    print(f"• Để theo dõi    : {C_CYAN}./loop view{C_RESET} hoặc {C_CYAN}python3 engine/tc-loop.py attach{C_RESET}")
    print(f"• Hoặc xem TUI   : {C_CYAN}./loop dash{C_RESET}")
    print(f"• Để dừng session: {C_RED}./loop stop{C_RESET}\n")
    return True

def launch_tmux_pipeline(dry_run: bool = False) -> bool:
    """Khởi chạy toàn trình E2E Pipeline trong tmux session riêng."""
    if not MUX or not MUX.available():
        print(f"{C_RED}[X] Tmux không khả dụng trên hệ thống. Chạy trực tiếp foreground.{C_RESET}")
        return False

    session_name = DEFAULT_PIPELINE_SESSION
    if MUX.has_session(session_name):
        print(f"{C_YELLOW}[!] Session tmux '{session_name}' đã tồn tại. Đang dừng session cũ...{C_RESET}")
        MUX.kill_session(session_name)
        time.sleep(1)

    script_path = ROOT_DIR / "engine" / "tc-loop.py"
    dry_flag = " --dry-run" if dry_run else ""
    cmd = f"python3 '{script_path}' pipeline{dry_flag}"

    MUX.new_session(session_name, ROOT_DIR, cmd)
    print(f"\n{C_GREEN}{C_BOLD}✓ ĐÃ KHỞI CHẠY TOÀN TRÌNH E2E PIPELINE TRONG TMUX SESSION: {session_name}{C_RESET}")
    print(f"• Để theo dõi    : {C_CYAN}./loop view{C_RESET} hoặc {C_CYAN}python3 engine/tc-loop.py attach --pipeline{C_RESET}")
    print(f"• Hoặc xem TUI   : {C_CYAN}./loop backlog{C_RESET}")
    print(f"• Để dừng session: {C_RED}./loop stop{C_RESET}\n")
    return True

def attach_tmux(is_pipeline: bool = False):
    """Kết nối vào session tmux đang chạy ngầm để xem trực tiếp."""
    session_name = DEFAULT_PIPELINE_SESSION if is_pipeline else DEFAULT_TMUX_SESSION
    if not MUX or not MUX.has_session(session_name):
        other_session = DEFAULT_TMUX_SESSION if is_pipeline else DEFAULT_PIPELINE_SESSION
        if MUX and MUX.has_session(other_session):
            session_name = other_session
        else:
            print(f"{C_YELLOW}[!] Không tìm thấy session tmux nào đang hoạt động.{C_RESET}")
            return
    print(f"{C_CYAN}Đang kết nối vào tmux session '{session_name}'... (Nhấn Ctrl+B rồi bấm D để thoát ra ngoài){C_RESET}")
    time.sleep(1)
    os.system(f"tmux attach-session -t {session_name}")

def stop_tmux(is_pipeline: bool = False):
    """Dừng an toàn các session tmux của vòng lặp."""
    session_name = DEFAULT_PIPELINE_SESSION if is_pipeline else DEFAULT_TMUX_SESSION
    stopped = False
    if MUX and MUX.has_session(session_name):
        MUX.kill_session(session_name)
        print(f"{C_GREEN}✓ Đã dừng session tmux '{session_name}'.{C_RESET}")
        stopped = True
    if not is_pipeline and MUX and MUX.has_session(DEFAULT_PIPELINE_SESSION):
        MUX.kill_session(DEFAULT_PIPELINE_SESSION)
        print(f"{C_GREEN}✓ Đã dừng session tmux '{DEFAULT_PIPELINE_SESSION}'.{C_RESET}")
        stopped = True
    if not stopped:
        print(f"{C_YELLOW}Không có session tmux nào đang hoạt động.{C_RESET}")

# ==============================================================================
# HÀM MAIN VÀ CLI ROUTER
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="TC IT Agent Autonomous Loop Engine (Inspired by bmad-loop)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Lệnh điều khiển")

    # Command: dashboard
    dash_p = subparsers.add_parser("dashboard", help="Xem bảng điều khiển tiến độ Epic")
    dash_p.add_argument("--spec", help="Tên hoặc mã số Epic (VD: 01, TASK-01...)")

    # Command: run
    run_p = subparsers.add_parser("run", help="Chạy vòng lặp tự trị cho 1 Epic")
    run_p.add_argument("--spec", help="Tên hoặc mã số Epic (VD: 01, TASK-01...)")
    run_p.add_argument("--max-tasks", type=int, default=999, help="Số task tối đa cần chạy")
    run_p.add_argument("--dry-run", action="store_true", help="Chạy thử không sinh mã và commit")
    run_p.add_argument("--bg", action="store_true", help="Chạy ngầm trong tmux session")

    # Command: pipeline
    pipe_p = subparsers.add_parser("pipeline", help="Chạy toàn trình E2E Pipeline từ Backlog")
    pipe_p.add_argument("--dry-run", action="store_true", help="Chạy thử không sinh mã")
    pipe_p.add_argument("--bg", action="store_true", help="Chạy ngầm trong tmux session")

    # Command: backlog
    subparsers.add_parser("backlog", help="Xem bảng tiến độ Backlog ý tưởng/CR")

    # Command: add
    add_p = subparsers.add_parser("add", help="Thêm một ý tưởng/CR mới vào Backlog")
    add_p.add_argument("idea", help="Nội dung ý tưởng hoặc yêu cầu mới")
    add_p.add_argument("--tag", default="CR", help="Nhãn phân loại (CR, FEATURE, BUG)")

    # Command: verify
    subparsers.add_parser("verify", help="Chạy kiểm tra các chốt chặn Verify Gates")

    # Command: attach
    att_p = subparsers.add_parser("attach", help="Kết nối xem trực tiếp Agent làm việc qua tmux")
    att_p.add_argument("--pipeline", action="store_true", help="Kết nối session pipeline")

    # Command: stop
    stop_p = subparsers.add_parser("stop", help="Dừng session tmux đang chạy ngầm")
    stop_p.add_argument("--pipeline", action="store_true", help="Dừng session pipeline")

    args = parser.parse_args()
    policy = load_policy()

    if not args.command:
        # Mặc định mở dashboard
        spec_name = resolve_spec_name("", policy)
        if spec_name:
            LoopEngine(spec_name, policy).print_dashboard()
        else:
            parser.print_help()
        return

    if args.command == "dashboard":
        spec_name = resolve_spec_name(args.spec or "", policy)
        if not spec_name:
            print(f"{C_RED}[X] Không tìm thấy Epic nào. Hãy tạo specs/[epic-id] trước.{C_RESET}")
            sys.exit(1)
        LoopEngine(spec_name, policy).print_dashboard()

    elif args.command == "run":
        spec_name = resolve_spec_name(args.spec or "", policy)
        if not spec_name:
            print(f"{C_RED}[X] Không tìm thấy Epic nào để chạy.{C_RESET}")
            sys.exit(1)

        if args.bg:
            launch_tmux_bg(spec_name, args.max_tasks, args.dry_run)
        else:
            LoopEngine(spec_name, policy).run_loop(args.max_tasks, args.dry_run)

    elif args.command == "pipeline":
        if args.bg:
            launch_tmux_pipeline(args.dry_run)
        else:
            PipelineEngine(policy).run_pipeline(args.dry_run)

    elif args.command == "backlog":
        PipelineEngine(policy).print_backlog()

    elif args.command == "add":
        item_id = append_backlog_item(args.idea, args.tag, policy=policy)
        print(f"\n{C_GREEN}✓ Đã ghi nhận thành công {item_id}: {args.idea}{C_RESET}\n")

    elif args.command == "verify":
        spec_name = resolve_spec_name("", policy)
        engine = LoopEngine(spec_name, policy) if spec_name else LoopEngine("DEFAULT", policy)
        print(f"\n{C_CYAN}🔍 Đang kiểm tra toàn bộ Verify Gates...{C_RESET}")
        passed, msg = engine.verify_gates()
        if passed:
            print(f"{C_GREEN}{C_BOLD}✓ 100% VERIFY GATES GREEN! Hệ thống đạt chuẩn xuất xưởng.{C_RESET}\n")
        else:
            print(f"{C_RED}{C_BOLD}[X] VERIFY GATES FAILED!{C_RESET}\n{msg}\n")
            sys.exit(1)

    elif args.command == "attach":
        attach_tmux(args.pipeline)

    elif args.command == "stop":
        stop_tmux(args.pipeline)

if __name__ == "__main__":
    main()
