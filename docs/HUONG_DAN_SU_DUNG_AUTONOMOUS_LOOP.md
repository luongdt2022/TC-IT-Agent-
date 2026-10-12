# Hướng Dẫn Vận Hành Vòng Lặp Tự Trị Đa Tác Tử (TC IT Autonomous Loop & E2E Pipeline)

> **Bộ Khung**: TC IT Agent Framework Enterprise v2.3  
> **Cảm hứng & Phương pháp luận**: `bmad-loop` (bmad-code-org) kết hợp GitHub Spec Kit Framework.

---

## 1. Triết Lý Vận Hành Cốt Lõi (Core Principles)

Vòng lặp tự trị trong TC IT Agent được xây dựng dựa trên 6 nguyên lý sắt đá:

1. **No-LLM-in-the-control-loop (Thuật toán kiểm soát xác định)**:
   - LLM **không bao giờ** được trao quyền tự quyết định trạng thái vòng lặp, tự đánh giá "đã xong hay chưa", hoặc tự ý chuyển task.
   - Toàn bộ việc đọc task, chuyển trạng thái, gọi lệnh kiểm thử, kiểm tra blast radius, tạo git commit và ghi log do **Engine Python/Bash (`engine/tc-loop.py`)** kiểm soát 100% một cách xác định (deterministic).
2. **Fresh Context per session (Triệt tiêu ô nhiễm ngữ cảnh)**:
   - Thay vì chạy một phiên chat dài vô tận khiến LLM bị đầy token, quên ngữ cảnh (context drift) hoặc sinh ảo giác; mỗi task kỹ thuật được khởi tạo trong một **process CLI độc lập** (`agy` hoặc `claude`).
   - Mỗi phiên chỉ nạp đúng 3 tệp neo grounding: `spec.md`, `plan.md`, `tasks.md` và mã lỗi từ attempt trước (nếu có).
3. **Deterministic Verify Gate (Chốt chặn toán học tĩnh bắt buộc)**:
   - Sau khi Agent báo hoàn thành mã nguồn, Engine lập tức kích hoạt bộ Verify Gates thật (TypeCheck, Compiler, Linter, Unit/Integration tests, Guard-rails).
   - Chỉ khi kiểm thử đạt **100% Green (exit code 0)**, task mới được công nhận.
4. **Atomic tasks.md tick & Git Commit (Truy vết khép kín 1:1)**:
   - Đánh dấu `[x]` vào `tasks.md` và lệnh `git commit` được thực hiện đồng thời trong cùng một lượt. Mã hash commit được gắn trực tiếp vào task để đối soát.
5. **Blast Radius Guard (Kiểm soát bán kính ảnh hưởng)**:
   - Giới hạn số lượng file được phép sửa đổi trong 1 task (mặc định $\le$ 8 files). Ngăn chặn hành vi Agent "tiện tay sửa lan" làm hỏng các module không liên quan.
6. **Auto-Retry with Failure Context & Attention Escalation**:
   - Nếu Verify Gate báo lỗi biên dịch hoặc test trượt, Engine tự động trích xuất `stdout/stderr` làm input ngữ cảnh cho attempt kế tiếp.
   - Nếu vượt quá số lần thử tối đa (`max_attempts_per_task = 3`), hệ thống tự dừng an toàn, ghi nhận vào `.tc-loop/ATTENTION.md` và phát thông báo âm thanh trên desktop macOS.

---

## 2. Bảng Điều Khiển Nhanh 1 Chạm (`./loop`)

Tại thư mục gốc của dự án, chỉ cần gõ duy nhất:

```bash
./loop
```

Màn hình điều khiển Terminal TUI trực quan xuất hiện:

```text
╔══════════════════════════════════════════════════════════════════════╗
║              TC IT AGENT AI LOOP — BẢNG ĐIỀU KHIỂN NHANH             ║
╚══════════════════════════════════════════════════════════════════════╝
  • Epic Đang Chọn: TASK-01

  ─── VÒNG LẶP TOÀN TRÌNH E2E (PO -> BA -> SA -> DEV -> QC) ──────────────
  [7] Khởi động Toàn trình E2E Pipeline (Tự động chạy hết Backlog)
  [8] Xem Bảng Điều Khiển Backlog Ý Tưởng (BACKLOG.md)
  [9] Thêm ý tưởng / CR mới vào Backlog

  ─── THỰC THI CHO 1 EPIC ĐANG CHỌN ─────────────────────────────────────
  [1] Xem tiến độ công việc (Dashboard trực quan)
  [2] Bật AI chạy ngầm âm thầm (Run in Background qua tmux)
  [3] Xem trực tiếp AI đang làm gì (Attach Live Screen)
  [4] Dừng AI chạy ngầm (Stop Background Process)
  [5] Kiểm tra chất lượng code & test (Verify Gates 100% Green)
  [6] Đổi Epic mục tiêu (VD: gõ 01, 02...)
  [0] Thoát
```

### Các phím bấm chức năng:
- **`[1]`**: Xem Dashboard tiến độ chi tiết của Epic mục tiêu: tỷ lệ %, danh sách task `[BE]`/`[FE]`/`[Test]`, trạng thái `DONE` hay `PENDING`.
- **`[2]`**: Khởi động Agent chạy ngầm trong tmux session `tc-loop`. Terminal hiện tại được giải phóng ngay lập tức, bạn có thể tiếp tục làm việc khác hoặc tắt máy terminal.
- **`[3]`**: Nhảy trực tiếp vào màn hình tmux để xem Agent đang đọc file, viết mã, chạy test theo thời gian thực. *(Nhấn `Ctrl + B` rồi bấm `D` để thoát ra mà không làm tắt Agent)*.
- **`[4]`**: Dừng an toàn session ngầm bất cứ lúc nào.
- **`[5]`**: Chạy thử bộ Verify Gates để đối soát chất lượng trước khi bàn giao.
- **`[6]`**: Đổi Epic đang thực thi (chỉ cần gõ số: `01`, `02`, hoặc mã `TASK-01`).
- **`[7]`**: **Toàn trình E2E Pipeline**: Tự động duyệt qua toàn bộ các ý tưởng/CR trong `BACKLOG.md`, tự động phân phối qua các Agent PO $\rightarrow$ BA $\rightarrow$ SA $\rightarrow$ Dev $\rightarrow$ QC và chạy khép kín đến khi hoàn tất 100%.
- **`[8]`**: Xem danh sách các đề bài/CR đang có trong `BACKLOG.md`.
- **`[9]`**: Thêm đề bài hoặc Change Request mới vào Backlog ngay từ terminal.

---

## 3. Danh Mục Lệnh Tắt Dòng Lệnh (CLI Shortcuts)

Ngoài menu bấm phím, bạn có thể gọi trực tiếp từ terminal hoặc CI/CD pipeline:

| Lệnh Dòng Lệnh | Mục Đích Thực Thi |
| :--- | :--- |
| **`./loop dash`** | Mở ngay Dashboard tiến độ của Epic hiện tại. |
| **`./loop 02`** | Mở Dashboard của Epic số 02 (VD: `TASK-02`). |
| **`./loop run`** | Khởi chạy Micro Loop chạy ngầm qua tmux cho Epic hiện tại. |
| **`./loop view`** / **`./loop attach`** | Kết nối trực tiếp vào màn hình ngầm để theo dõi Agent. |
| **`./loop stop`** | Dừng an toàn toàn bộ các session tmux đang chạy. |
| **`./loop check`** / **`./loop verify`**| Chạy kiểm tra các chốt chặn Verify Gates. |
| **`./loop pipeline`** / **`./loop auto`**| Khởi chạy E2E Pipeline chạy ngầm xử lý toàn bộ Backlog. |
| **`./loop backlog`** | Hiển thị bảng tiến độ Backlog ý tưởng. |
| **`./loop add "Tích hợp SSO Zalo"`** | Thêm ý tưởng/CR mới vào cuối `BACKLOG.md`. |

---

## 4. Tùy Biến Cấu Hình Dự Án (`engine/policy.toml`)

Mọi hành vi của Engine được điều khiển qua tập tin `engine/policy.toml`. Bạn có thể tùy biến linh hoạt theo từng dự án:

```toml
[project]
name = "My Enterprise Project"

[loop]
project_root = "."
task_specs_dir = "specs"                  # Hoặc "SourceCode/specs"
backlog_file = "backlog/BACKLOG.md"       # File chứa ý tưởng/CR
max_attempts_per_task = 3                 # Tối đa 3 lần thử lại
session_timeout_seconds = 600             # 10 phút / task
blast_radius_max_files = 8                # Tối đa 8 files sửa đổi / task
auto_commit = true                        # Tự động commit git
auto_advance = true                       # Tự động chuyển task kế tiếp

[agents]
cli = "auto"                              # "auto", "agy" (Google Antigravity), hoặc "claude"
dev_model = "sonnet"                      # Model ưu tiên cho dev
review_model = "opus"                     # Model cho review

[verify]
# Danh sách các lệnh kiểm thử toán học tĩnh:
commands = [
    "bash scripts/guard-rails.sh",
    # Bổ sung theo stack của bạn:
    # "dotnet test tests/unit --no-build",
    # "pnpm test --run",
    # "pytest tests/unit",
]

[scm]
isolation = "branch"
base_branch = "main"
commit_prefix = "feat"

[escalation]
notify_mac_desktop = true
attention_file = ".tc-loop/ATTENTION.md"
```

---

## 5. Cấu Trúc Thư Mục Dữ Liệu Runtime (`.tc-loop/`)

Khi vận hành, Engine tự động quản lý trạng thái tại thư mục ẩn `.tc-loop/` (đã được cấu hình tự động trong `.gitignore`):

```text
.tc-loop/
├── state.json                 # Lưu Epic đang chọn, active_task_id, số lần attempts
├── ATTENTION.md               # Sổ ghi nhận các task bị tắc nghẽn cần người can thiệp
└── logs/                      # Toàn bộ stdout/stderr của Agent CLI và Verify log
    ├── TASK-01_attempt_1_agent.log
    ├── TASK-01_attempt_1_verify.log
    └── ...
```

---

## 6. Khả Năng Độc Lập & Tương Thích

- **Zero-Dependency Native Tmux Backend**: Engine tích hợp sẵn trình điều khiển `NativeTmuxMultiplexer` tương tác trực tiếp với POSIX tmux bằng `subprocess`. Không bắt buộc cài đặt package ngoài.
- Nếu môi trường có cài đặt gói `bmad-loop`, Engine sẽ tự động nhận diện và sử dụng adapter tối ưu tương ứng.
- Tương thích 100% với các nền tảng: macOS, Linux, WSL2.
