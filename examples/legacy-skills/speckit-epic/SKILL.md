---
name: "speckit-epic"
description: "Khởi tạo một Epic mới, đăng ký vào Master Roadmap (specs/ROADMAP.md) và thiết lập thư mục specs/<epic-id> với đầy đủ bộ 3 tài liệu chuẩn (spec.md, plan.md, tasks.md) cho ManageAgent."
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "custom/speckit-epic"
---

## User Input

```text
$ARGUMENTS
```

Tham số đầu vào là Mã Epic và Tên phân hệ nghiệp vụ (Ví dụ: `E2: RAG Engine & Qdrant Semantic Search`, `E3: Agent Management & Chat SSE`, `E4: Embed Widget`).

---

## Quy Trình Thực Hiện

1. **Xác định thông tin Epic**:
   - Phân tích mã Epic, tên phân hệ, phạm vi chức năng từ tham số đầu vào và `docs/reference/PRD.md`.
   - Xác định số thứ tự thư mục tiếp theo trong `specs/` (ví dụ: `specs/009-rag-engine`).

2. **Khởi tạo thư mục và tài liệu mẫu**:
   - Tạo thư mục `specs/<mã-thứ-tự>-<tên-nghiệp-vụ>`.
   - Sinh `spec.md` từ mẫu `.specify/templates/spec-template.md`.
   - Sinh `plan.md` từ mẫu `.specify/templates/plan-template.md`.
   - Sinh `tasks.md` từ mẫu `.specify/templates/tasks-template.md`.
   - Cập nhật `.specify/feature.json` trỏ tới thư mục vừa tạo.

3. **Đăng ký vào Master Roadmap (`specs/ROADMAP.md`)**:
   - Thêm một hàng mới vào **Mục 1: Bảng Điều Phối Toàn Bộ Epics** với trạng thái ban đầu `⚪ Dự Kiến` hoặc `🔵 Đang thi công`.
   - Thêm một dòng ghi nhận vào **Mục 3: Lịch Sử Thay Đổi & Phát Sinh Epics** mô tả lý do tạo Epic.

4. **Báo cáo kết quả**:
   - Thông báo cho người dùng đường dẫn thư mục `specs/<epic-id>/`.
   - Gợi ý lệnh tiếp theo: `/speckit-autopilot` để thực thi tự động hoặc `/speckit-specify` để hoàn thiện đặc tả.
