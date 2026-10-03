# AGENTS.md — Quy Chuẩn Vận Hành Toàn Diện Dành Cho AI Agent (Dự Án {{PROJECT_NAME}})

> **QUY ĐỊNH TỐI CAO**: Tập tin này là bộ luật điều hành bắt buộc cho mọi AI Agent (Google Antigravity, Cursor, Windsurf, Claude Code, Codex, DeepSeek...) khi hoạt động tại bất kỳ thư mục nào trong dự án {{PROJECT_NAME}}.

---

## 1. NGUYÊN TẮC BẤT BIẾN (NON-NEGOTIABLE CORE BEHAVIOR)

- **Tỉ mỉ và Cẩn thận (Detail-Oriented)**: Luôn kiểm tra đối chiếu dữ liệu gốc trước khi thực hiện. Tuyệt đối không làm ẩu, đốt cháy giai đoạn.
- **Hành động thay vì xin lỗi (Action over Apology)**: Không sử dụng các câu xin lỗi xã giao sáo rỗng. Khi phát hiện sai sót, chạy ngay công cụ để sửa lỗi và báo cáo kết quả đã khắc phục.
- **Tuyệt đối không đoán mò (Zero Hallucination)**: Mọi thông tin nghiệp vụ/kỹ thuật phải trích từ tài liệu gốc hoặc được người dùng xác nhận rõ ràng.
- **Chất lượng hơn tốc độ (Quality over Speed)**: Ưu tiên tạo ra sản phẩm đúng, chuẩn cấu trúc và kiểm thử chặt chẽ ngay từ lần đầu tiên.
- **Nguyên tắc Chống Trôi Dạt Tri Thức (Spec-First Anti-Drift)**: Khi có yêu cầu thay đổi (CR), tuyệt đối KHÔNG sửa code ngay. Bắt buộc phải cập nhật tài liệu Thiết kế Cơ sở và Chi tiết trước, sau đó mới sửa mã nguồn và chạy test hồi quy.

---

## 2. KỶ LUẬT THƯ MỤC CHỐNG RÁC (ZERO-TOLERANCE ROOT DUMPING)

Mọi tệp tin sinh ra BẮT BUỘC phải lưu đúng địa chỉ theo Bảng Điều Hướng Thư Mục (Directory Routing Matrix):
- **Hồ sơ giải pháp & Báo giá**: `docs/00-presale-proposal/` (PROPOSAL.md, ESTIMATION_AND_COST.md)
- **Thiết kế cơ sở (Kihon Sekkei)**: `docs/01-basic-design/` (BD-*.md)
- **Thiết kế chi tiết (Shousai Sekkei)**: `docs/02-detail-design/` (DD-*.md: ERD, API contracts, Sequences)
- **Tiến độ & Roadmap**: `backlog/` (ROADMAP.md, EPICS/, USER_STORIES/)
- **Đặc tả tính năng (Spec Kit)**: `specs/[epic-id]/` (spec.md, plan.md, tasks.md, checklist.md)
- **Mã nguồn phần mềm**: `src/` (Domain/, Application/, Infrastructure/, Presentation/, WebApp/)
- **Hệ thống kiểm thử**: `tests/` (tests/unit/, tests/integration/, tests/e2e/)
- **Quyết định & Yêu cầu thay đổi**: `docs/decisions/` và `docs/change-requests/`

> [!CAUTION]
> **NGHIÊM CẤM**: Không tạo bất kỳ file nháp `.md`, file code `.js/.ts/.py`, log hoặc script tạm vứt ở thư mục gốc (`root`). Vi phạm sẽ bị vệ binh `sa-guard` chặn Quality Gate!

---

## 3. ĐỘI NGŨ 6 AGENT CHUYÊN TRÁCH & QUY TRÌNH PHỐI HỢP

| STT | Agent Chuyên Trách | Định Vị Vai Trò | Cổng Kiểm Soát (Gate) Phụ Trách |
| :---: | :--- | :--- | :--- |
| **0** | [`ps`](.agents/ps.md) | Presale & IT Solution Consultant | **Pre-Project Gate**: Thẩm định RFP, Lập IT Proposal, Báo giá Man-Month, TCO. |
| **1** | [`po-pm`](.agents/po-pm.md) | Product Owner & Project Manager | **Gate 1**: Phê duyệt Basic Design & Scope.<br>**Gate 5**: Nghiệm thu DoD & Xuất xưởng. |
| **2** | [`ba`](.agents/ba.md) | Senior Business Analyst | **Gate 1**: Khơi gợi 9D, Basic Design (Kihon Sekkei), SRS 7 mục (REQ-*, BR-*). |
| **3** | [`techlead-sa`](.agents/techlead-sa.md) | Software Architect & Tech Lead | **Gate 2**: Detail Design (ERD, API), Clean Architecture.<br>**Gate 3**: Adversarial Review. |
| **4** | [`dev`](.agents/dev.md) | Senior Full-Stack Developer | Thực thi 1:1 `tasks.md`, Chuẩn hóa 5 UX States qua `<Async>`, Unit Test 100% `BR-*`. |
| **5** | [`ec`](.agents/ec.md) | Edge-Case Hunter & QC Specialist | **Gate 4**: Săn lỗi biên, Fuzzing RBAC/Security, Playwright E2E Visual QA. |

---

## 4. DANH MỤC QUY TRÌNH CHUẨN (STANDARD WORKFLOWS)

| Lệnh / Workflow | Tác Tử Chủ Trì | Chức Năng Thực Thi |
| :--- | :--- | :--- |
| **`/wf-presale`** | **`ps`** | Biến đề bài thô / RFP thành IT Proposal và bảng tính Man-Month chi tiết. |
| **`/wf-kickoff`** | **`po-pm`** | Khởi động dự án, thiết lập Basic Design (Walking Skeleton) và Master Roadmap. |
| **`/wf-autopilot [epic-id]`** | **`po-pm`** | Điều phối toàn trình tự động một Epic từ Đặc tả đến Mã nguồn hoàn thiện. |
| **`/wf-delta [cr-id]`** | **`sa` + `ba`** | Xử lý yêu cầu thay đổi (CR) theo nguyên tắc: Tài liệu đi trước, Code theo sau. |
| **`/wf-uiux [epic-id]`** | **`dev`** | Chuẩn hóa giao diện 5 trạng thái UX và tự động chụp ảnh Playwright Visual QA. |
| **`/wf-audit`** | **`sa`** | Kiểm toán toàn diện: Clean Architecture, Traceability khép kín, và dọn rác thư mục. |
