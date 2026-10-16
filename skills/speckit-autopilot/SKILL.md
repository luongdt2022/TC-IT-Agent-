---
name: "speckit-autopilot"
description: "Trục cao tốc tự động hóa toàn trình Epic (Specify -> Plan -> Tasks -> Implement -> SA Review Gate 3 -> QC Verify Gate 4 -> QA Shadow Audit -> PO Gate 5 DoD) theo chuẩn Enterprise Multi-Agent Stage-Gate."
metadata:
  author: "TC IT Agent Architecture Team"
  source: "enterprise/speckit-autopilot"
  version: "2.4.0"
---

## User Input

```text
$ARGUMENTS
```

Tham số đầu vào là mã Epic hoặc tên tính năng (Ví dụ: `EPIC-01`, `TASK-01`, hoặc tên phân hệ nghiệp vụ).  
Nếu chưa cung cấp, hãy tra cứu `specs/ROADMAP.md` (hoặc `backlog/ROADMAP.md`) và hỏi người dùng muốn thực thi Epic nào.

---

## Mục Tiêu & Triết Lý Vận Hành (Enterprise Autopilot Philosophy)

Skill **`speckit-autopilot`** giải quyết bài toán: **"Kích hoạt 1 lệnh — Hoàn thành khép kín cả Epic"**.  
Tự động điều phối toàn bộ chu trình phát triển phần mềm doanh nghiệp qua 7 giai đoạn có chốt chặn kiểm soát nghiêm ngặt:

1. **Tự Động Hóa Liền Mạch (Seamless Automation)**: Chuyển giao mượt mà giữa các tác tử (`po-pm`, `ba`, `techlead-sa`, `dev`, `ec`, `qa`).
2. **Kỷ Luật Cách Ly Context (Subagent Context Isolation)**: 
   - Dev, SA Review, và QC Verification bắt buộc chạy trong **Subagent độc lập** với Context mới tinh để tránh suy thoái trí nhớ và context pollution.
   - QC nhận **Zero-Code Context**: Chỉ nhận Spec, Wireframe, và Live URL — tuyệt đối không mớm code của Dev cho QC.
3. **5 Cổng Kiểm Soát Chất Lượng (Strict 5-Stage Gate Governance)**:
   - **Gate 1 (DoR)**: BA soạn thảo SRS 7 mục, làm rõ điểm nghẽn (`ba-clarify`).
   - **Gate 2 (Architecture & Plan)**: SA lập `plan.md`, chốt DTOs/Contract-First, chốt ADR.
   - **Gate 3 (Dev DoD & Adversarial Review)**: SA thẩm định 6 trục kiểm soát, `guard-rails.sh`, độ phủ trường form $\ge 80\%$.
   - **Gate 4 (QC Verification)**: QC kiểm thử Pure Black-Box, Zero-Mock, Deep DB State Verification.
   - **Shadow QA Audit**: QA giám sát vi sai Git, săn mock ngầm, đo Token Context (60% - 80%).
   - **Gate 5 (Release DoD)**: PO nghiệm thu cuối cùng theo Definition of Done (`xong`), xuất xưởng sang `[SHIPPED]`.

---

## Chu Trình Thực Thi 7 Giai Đoạn Chi Tiết

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TC IT AGENT ENTERPRISE AUTOPILOT PIPELINE                       │
└────────────────────────────────────────────────────────────────────────────────────────┘
  [1] speckit-specify   ──> Đọc Basic Design, sinh specs/[epic-id]/spec.md (SRS 7 mục)
           │
           ▼
  [1.1] speckit-clarify ──> 🛑 CHECKPOINT 1: DỪNG LẠI nếu mơ hồ; Tự động đi tiếp nếu rõ ràng
           │
           ▼
  [2] speckit-plan      ──> 🏛️ GATE 2 (SA Review): Thiết kế Clean Architecture, DB schema, RBAC;
           │                ⭐ CONTRACT-FIRST: Chốt DTOs/OpenAPI trước cho cả BE và FE
           │                🛑 CHECKPOINT 2: SA thẩm định & Phê duyệt quyết định kiến trúc lớn (ADR)
           │
           ▼
  [2.1] speckit-uiux    ──> (Nếu Task có UI) Wireframe HTML mapping, chuẩn hóa 5 UX States (<Async>)
           │
           ▼
  [3] speckit-tasks     ──> Phân rã tasks.md: Đủ 5 Entity Lifecycle ([FE-LIST], [DETAIL], [CREATE], [EDIT], [STATUS])
           │
           ▼
  [3.1] speckit-analyze ──> 🏛️ GATE 2 (SA Consistency): Rà soát chéo Coverage Matrix (100% REQ-*, BR-*)
           │
           ▼
  [4] speckit-implement ──> ⚡ SUBAGENT ISOLATION (Dev): Lập trình tuần tự 1:1, Clean Arch, TDD
           │                🛑 CHECKPOINT 3: DỪNG LẠI nếu gặp blocker môi trường/DB/SDK
           │
           ▼
  [4.1] sa-gate3-review ──> 🛑 GATE 3 BẮT BUỘC (SA Adversarial Review Subagent):
           │                - SA chạy pr-review-guard & guard-rails.sh rà soát 6 trục kiểm soát
           │                - Chạy audit_wireframe_fields.py (Controls coverage >= 80%)
           │                - SA phản hồi PO & Dev; Dev fix triệt để mọi lỗi Critical trước khi sang QC
           ▼
  [5] speckit-converge  ──> 🛡️ GATE 4 (QC Subagent Black-box Verification):
           │                - Pure Black-Box: Real Data, Real Login, Zero-Mock (Cấm page.route, cấm mock token)
           │                - Deep DB Assertion: Query CSDL thật xác minh bản ghi INSERT/UPDATE
           ▼
  [5.1] qa-shadow-audit ──> 👻 SHADOW QA AUDIT (Independent Process):
           │                - Đo Token Context (60% - 80%), quét Git diff bắt mock ngầm
           │                - Thẩm định 5 Stage-Gate, xuất bản Release Readiness Scorecard
           ▼
  [5.2] po-signoff-gate5──> 🏆 GATE 5 (PO Acceptance):
                            Nghiệm thu Definition of Done (xong), cập nhật Living Docs & ROADMAP -> [SHIPPED]
```

---

### Giai Đoạn 1: Khởi Tạo Yêu Cầu Từ Basic Design (`speckit-specify`)

1. **Xác định Feature Scope & Nguồn Dữ Liệu**:
   - Đọc tài liệu nguồn tại `docs/01-basic-design/` hoặc biểu mẫu Wireframe HTML mô phỏng.
2. **Khởi tạo Feature Directory**:
   - Tạo thư mục: `specs/[epic-id]/`.
3. **Sinh tài liệu `spec.md` chuẩn hóa**:
   - User Stories theo thứ tự ưu tiên (P1, P2...). Mỗi User Story có Acceptance Scenarios (Given-When-Then).
   - Functional Requirements (`REQ-*`) và Business Rules (`BR-*`).
4. **Cập nhật Roadmap**:
   - Đánh dấu trạng thái Epic trong `specs/ROADMAP.md` sang `🔵 Đang thi công`.

---

### Giai Đoạn 1.1: Làm Rõ Nghiệp Vụ (`speckit-clarify`) — 🛑 CHECKPOINT 1

1. **Rà soát điểm mơ hồ**:
   - Có logic rẽ nhánh mập mờ hoặc thiếu điều kiện bảo mật?
   - Nếu có: **DỪNG LẠI NGAY (STOP)**, đặt tối đa 3 câu hỏi trắc nghiệm A/B/C có phân tích tác động kỹ thuật cho người dùng.
   - Khi có xác nhận: ghi vào `spec.md` và tự động chuyển sang Giai đoạn 2.
   - Nếu đã rõ ràng 100%: Tự động tiếp tục sang Giai đoạn 2.

---

### Giai Đoạn 2: Lập Kế Hoạch Kỹ Thuật (`speckit-plan`) — 🏛️ GATE 2 (SA CHECKPOINT)

1. **Contract-First Design**:
   - Định nghĩa DTOs, API Endpoints, ErrorCodes chuẩn trước khi viết code.
2. **Architecture Plan**:
   - Phân rã tầng Clean Architecture (`Domain`, `Application`, `Infrastructure`, `Presentation`, `WebApp`).
   - Thiết kế CSDL, quan hệ khóa ngoại, Optimistic locking, index.
   - Ghi nhận quyết định kiến trúc lớn thành ADR tại `docs/decisions/`.
3. **🏛️ SA Thẩm định Gate 2**:
   - SA rà soát schema, CQRS, phân quyền và xác nhận đạt chuẩn trước khi sang bước tiếp theo.

---

### Giai Đoạn 2.1: Thiết Kế UI/UX & Wireframe Mapping (`speckit-uiux`)
*(Bỏ qua nếu Epic thuần Backend / Infrastructure)*
1. **Wireframe HTML Mapping**:
   - Đọc trực tiếp các file HTML Wireframe trong `docs/01-basic-design/`.
2. **Chuẩn hóa 5 Trạng Thái UX qua `<Async>`**:
   - `Loading` (Skeleton loader) · `Empty` · `Error` (nút Retry) · `Success` · `Partial` (phân trang).

---

### Giai Đoạn 3 & 3.1: Phân Rã Task & Rà Soát Nhất Quán (`speckit-tasks` & `speckit-analyze`)

1. **Sinh `tasks.md` tuân thủ Kỷ luật 5 Hành vi Entity Lifecycle**:
   - `[FE-LIST]`: Danh sách hiển thị, bộ lọc, phân trang kèm 5 UX states.
   - `[FE-DETAIL]`: Màn hình xem chi tiết bản ghi (Read-only, masking dữ liệu nhạy cảm).
   - `[FE-CREATE]`: Form tạo mới đầy đủ 100% trường dữ liệu theo Wireframe HTML gốc.
   - `[FE-EDIT]`: Form chỉnh sửa bản nháp có kiểm tra quyền Owner và Optimistic Locking.
   - `[FE-STATUS]`: Luồng chuyển đổi trạng thái (Gửi duyệt, Thu hồi, Hủy bỏ).
2. **SA Rà Soát Tính Nhất Quán Chéo (`sa-analyze`)**:
   - 100% User Stories và Business Rules `BR-*` đã có task thực thi tương ứng.
   - Pass Gate 2 mới cho phép chuyển sang Giai đoạn 4.

---

### Giai Đoạn 4: Lập Trình Thực Thi Cô Lập Context (`speckit-implement`) — 🛑 CHECKPOINT 3

> [!CAUTION]
> **KỶ LUẬT CÔ LẬP CONTEXT CỦA DEV (SUBAGENT CONTEXT ISOLATION)**:
> Agent điều phối **BẮT BUỘC DÙNG TOOL `invoke_subagent`** để kích hoạt Agent `dev` với Context riêng độc lập và Model tốc độ cao (`flash`):
> ```json
> invoke_subagent(
>   TypeName: "dev",
>   Role: "Senior Full-Stack Developer",
>   Model: "flash",
>   Prompt: "Thực thi toàn bộ các task trong specs/[epic-id]/tasks.md theo spec.md và plan.md. Đảm bảo form đủ 100% trường theo Wireframe, chạy test trong context của bạn. Khi xong, chỉ gửi báo cáo tóm tắt hoàn thành về cho Orchestrator."
> )
> ```

1. **Thực thi tuần tự nguyên tử 1 task/chu kỳ**:
   - Pre-flight grounding (đọc UI catalog & DB schema).
   - TDD: Viết Unit Test cho `BR-*` trước, viết mã nguồn nghiệp vụ sau.
   - Cập nhật tick `[x]` sau khi kiểm chứng thành công.
2. **Giải phóng Context**:
   - Toàn bộ build logs, test logs nằm trong subagent của Dev; context chính luôn siêu nhẹ.

---

### Giai Đoạn 4.1: Kiểm Toán Đối Kháng SA & Gác Cổng DoD (Gate 3 Bắt Buộc) — 🛑 CHECKPOINT 3.5

> [!CAUTION]
> **KỶ LUẬT CÔ LẬP CONTEXT CỦA SA REVIEW (SUBAGENT ISOLATION FOR SA GATE 3)**:
> Agent điều phối kích hoạt **`techlead-sa`** qua `invoke_subagent`:
> ```json
> invoke_subagent(
>   TypeName: "techlead-sa",
>   Role: "Gate 3 Adversarial Reviewer",
>   Model: "flash",
>   Prompt: "Thực hiện Gate 3 Adversarial Review cho mã nguồn vừa thi công của [epic-id]. Chạy ./scripts/guard-rails.sh và audit_wireframe_fields.py trong context của bạn. Thẩm định 6 trục kiểm soát. Chỉ khi 0 lỗi Critical mới ký duyệt GATE 3 APPROVED."
> )
> ```

1. **SA Kích hoạt Chốt chặn Tĩnh & Review Mã Nguồn**:
   - Chạy `./scripts/guard-rails.sh`: 0 lỗi compilation, 0 TypeScript warning.
   - Chạy `./scripts/audit_wireframe_fields.py`: Tỷ lệ controls trên giao diện $\ge 80\%$.
   - Quét sạch 100% mock routes, mock token, dummy array trong `catch`.
   - Rà soát 6 trục kiểm soát qua `pr-review-guard`.
2. **Dev khắc phục triệt để lỗi CRITICAL**:
   - Chỉ khi SA ký duyệt **"GATE 3 APPROVED"**, task mới được chuyển sang Giai đoạn 5 bàn giao cho QC!

---

### Giai Đoạn 5: Đánh Giá Hội Tụ & Nghiệm Thu QC (`speckit-converge`) — 🛡️ GATE 4

> [!CAUTION]
> **KỶ LUẬT CÔ LẬP SUBAGENT QC (ZERO-CODE CONTEXT ISOLATION)**:
> Agent điều phối kích hoạt Agent `ec` qua `invoke_subagent` với **Zero-Code Payload**:
> ```json
> invoke_subagent(
>   TypeName: "ec",
>   Role: "Independent Black-Box QC",
>   Model: "flash",
>   Prompt: "Kiểm thử Pure Black-box cho [epic-id]. Tài liệu đối soát: docs/01-basic-design/ và specs/[epic-id]/spec.md (chỉ đọc User Stories và BR-*). TUYỆT ĐỐI KHÔNG ĐỌC SOURCE CODE CỦA DEV. Bắt buộc test tài khoản thật, cấm mock token, đối soát CSDL thật."
> )
> ```

1. **Kiểm thử Black-Box Đa Tầng**:
   - Tầng 1: Unit & Invariants Test.
   - Tầng 2: Contract Test (API DTO compatibility).
   - Tầng 3: Database Integration Test (đối soát CSDL thật: dữ liệu được INSERT/UPDATE chính xác, không rỗng ruột).
   - Tầng 4: Playwright E2E Pure Black-Box (tài khoản thật, controls thật, không dùng `page.route()`).
2. **Ký duyệt Gate 4**: Đạt 100% Green $\rightarrow$ QC ký xác nhận Pass Gate 4.

---

### Giai Đoạn 5.1: Kiểm Toán Độc Lập Shadow QA (`qa-shadow-sentinel` & `qa-gate-audit`)

1. **Kích hoạt QA Agent**:
   - Chạy `./scripts/qa-shadow-sentinel.sh`.
   - Đo lường Token Context (cảnh báo vùng vàng 60%, báo động đỏ 80%).
   - Quét vi sai Git diff bắt mock ngầm.
   - Xuất bản Release Readiness Scorecard, cấp thẻ **[GO]** cho PO.

---

### Giai Đoạn 5.2: Nghiệm Thu Cuối Cùng & Xuất Xưởng (Gate 5 Sign-off - PO DoD)

1. **Nghiệm thu DoD qua `xong`**:
   - PO/PM (`po-pm`) đối soát Acceptance Criteria và Definition of Done.
   - Cập nhật Living Docs tại `docs/system/`.
   - Cập nhật Master Roadmap tại `specs/ROADMAP.md` sang trạng thái `✅ [SHIPPED]`.
2. **Báo Cáo Nghiệm Thu Trọn Vẹn**:
   - Xuất báo cáo tổng kết tiến độ hoàn thành cho người dùng.
