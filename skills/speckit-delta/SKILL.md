---
name: "speckit-delta"
description: "Quy trình điều phối cập nhật & nâng cấp (Delta / Change Request) cho một Epic trong hệ sinh thái TC IT Agent: từ Cross-Surface Impact Analysis, bổ sung spec non-destructive, phân rã task mới [BE]/[FE], kiểm thử hồi quy, Subagent Isolation đến nghiệm thu hội tụ."
metadata:
  author: "TC IT Agent Architecture Team"
  source: "enterprise/speckit-delta"
  version: "2.4.0"
---

## User Input

```text
$ARGUMENTS
```

Tham số đầu vào bao gồm:
1. **Epic cần cập nhật**: Mã Epic chuẩn (ví dụ: `EPIC-01`, `TASK-01`).
2. **Nội dung thay đổi / Yêu cầu mới**: Mô tả yêu cầu sửa đổi, tài liệu bổ sung từ PO, hoặc yêu cầu kỹ thuật phát sinh (Change Request).

Nếu người dùng chưa cung cấp đủ thông tin, hãy hỏi người dùng:
1. Cần cập nhật Delta cho Epic nào trong Roadmap?
2. Chi tiết yêu cầu thay đổi nghiệp vụ hoặc kỹ thuật cần bổ sung là gì?

---

## Triết Lý Vận Hành Của Spec Kit Delta (Core Principles)

Khác với việc xây dựng một Epic mới từ con số 0, việc **sửa đổi/bổ sung một Epic đang thi công hoặc đã hoàn thiện** đòi hỏi sự chặt chẽ tối đa để không làm gãy hệ thống đang chạy:

1. **Bất Biến Lịch Sử & Non-destructive Migration**:
   - **Tuyệt đối KHÔNG** sửa đè hoặc xóa các file migration cũ đã áp dụng vào CSDL.
   - Luôn tạo file migration mới với tên mô tả rõ ràng.
2. **Tương Thích Ngược Tuyệt Đối (Backward Compatibility)**:
   - Các cột mới bổ sung vào bảng đã có dữ liệu bắt buộc phải là `Nullable` hoặc có giá trị mặc định (`DEFAULT`).
   - Tuyệt đối không xóa cột hoặc đổi kiểu dữ liệu gây mất dữ liệu nếu không có kế hoạch chuyển đổi tường minh.
3. **Bảo Toàn Danh Sách Việc Cũ (Append-only Tasks)**:
   - Giữ nguyên vẹn toàn bộ các task cũ đã đánh dấu `[x]` hoặc `[ ]`.
   - Phân rã phần việc mới thành một Giai đoạn bổ sung ở cuối file `tasks.md` (ví dụ: `## Giai đoạn N: Delta v2 — [Tên Nội Dung]`).
4. **Không Gây Hồi Quy (Zero Regression)**:
   - 100% test suites cũ của Backend và Frontend phải tiếp tục pass.
   - Bổ sung test suites mới kiểm chứng chuyên biệt cho các trường/tính năng vừa nâng cấp.
5. **Hội Tụ Đa Bề Mặt (Cross-Surface Convergence)**:
   - Một thay đổi nghiệp vụ không được coi là hoàn tất chỉ vì một kênh đã sửa. Trước khi code và trước khi converge, phải đối chiếu đủ: Basic Design/wireframe, Detail Spec, API/DTO, domain validation, DB/migration, Web, App (nếu có), public/owner/admin và test.
6. **Kỷ Luật Cô Lập Context (Subagent Isolation)**:
   - Dev, SA Review và QC Verification Delta thực thi trong Subagent độc lập để chống tràn ngữ cảnh và bảo vệ chất lượng.

---

## Quy Trình Nâng Cấp Delta 5 Giai Đoạn Chi Tiết

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TC IT AGENT SPECKIT DELTA PIPELINE                              │
└────────────────────────────────────────────────────────────────────────────────────────┘
  [1] Impact Analysis ──> Đánh giá bề mặt tác động & Viết Spec Delta vào spec.md
           │
           ▼
  [1.1] Clarify Check ──> 🛑 CHECKPOINT 1: DỪNG LẠI HỎI nếu mâu thuẫn/thiếu dữ kiện
           │               (Nếu yêu cầu rõ ràng -> Tự động đi tiếp)
           ▼
  [2] Plan Delta      ──> 🏛️ GATE 2 (SA Review): Cập nhật plan.md & schema CSDL
           │               🛑 CHECKPOINT 2: SA thẩm định Non-destructive Migration & DTOs
           ▼
  [2.1] speckit-uiux  ──> (Nếu Delta có đổi UI) Wireframe HTML mapping, 5 trạng thái UX
           │
           ▼
  [3] Tasks Delta     ──> Append Phase mới vào cuối tasks.md (Gắn tag [BE], [FE], [INT])
           │
           ▼
  [3.1] speckit-analyze──> 🏛️ GATE 2 (SA Consistency): Rà soát chéo Coverage Matrix Delta 100%
           │
           ▼
  [4] Implement Delta ──> ⚡ SUBAGENT ISOLATION (Dev): Viết migration/code mới, test delta
           │                🛑 CHECKPOINT 3: DỪNG LẠI HỎI nếu gặp lỗi môi trường/DB lock
           ▼
  [4.1] sa-gate3-delta ──> 🛑 GATE 3 BẮT BUỘC (SA Adversarial Review Subagent):
           │                - SA chạy pr-review-guard & guard-rails.sh rà soát 6 trục kiểm soát
           │                - Chạy audit_wireframe_fields.py kiểm tra độ phủ trường biểu mẫu
           │                - Dev fix triệt để mọi lỗi Critical trước khi sang QC
           ▼
  [5] Converge Delta  ──> 🛡️ GATE 4 (QC Subagent Black-box Verification):
           │                - Pure Black-Box, Zero-Mock (Cấm page.route, cấm mock token)
           │                - Deep DB State Verification (đối soát trực tiếp CSDL thật)
           ▼
  [5.1] qa-shadow-audit ──> 👻 SHADOW QA AUDIT (Independent Process):
           │                - Quét Git diff bắt mock ngầm, đo Token Context (60% - 80%)
           ▼
  [5.2] po-signoff-delta──> 🏆 GATE 5 (PO DoD Sign-off):
                            Kiểm thử hồi quy 100%, cập nhật ROADMAP & Living Docs docs/system/
```

---

### Giai Đoạn 1: Đánh Giá Tác Động & Viết Spec Delta (`spec.md`)

1. **Bước 1.0 (BẮT BUỘC): Quét Mã Nguồn Toàn Cục (Grep-First Surface Discovery)**:
   - Trước khi viết bất kỳ chữ nào vào `spec.md`, BA/SA **bắt buộc phải chạy lệnh Grep toàn diện** trên toàn bộ codebase (`src/` hoặc `frontend/`, `backend/`) để tìm tất cả các vị trí tiêu thụ từ khóa/mã liên quan.
   - Tránh tuyệt đối cái bẫy "Mù cục bộ" (chỉ nhìn file spec của 1 Task mà bỏ sót Trang chủ, Login, Dashboard, Navigation...).
2. **Xác định Task mục tiêu & Lập Bảng Ma Trận Bề Mặt**:
   - Định vị thư mục Task tương ứng trong `specs/`.
   - Lập **Cross-Surface Impact Matrix** gồm 4 cột: Bề mặt/Màn hình | File Path | Hiện trạng | Thay đổi cần làm.
3. **🛑 CHECKPOINT 1.1: CỔNG DUYỆT PHẠM VI ẢNH HƯỞNG (USER SCOPE GATE)**:
   - Xuất trình Bảng Ma trận Bề mặt Ảnh hưởng cho User/PO và đặt câu hỏi xác nhận phạm vi trước khi phân rã kỹ thuật.
4. **Cập nhật `spec.md` (Append-only)**:
   - Giữ nguyên toàn bộ nội dung của các User Stories cũ.
   - Bổ sung mục mới vào cuối file: `## Phần Bổ Sung Delta [Phiên Bản / Ngày Tháng]`.
   - Bổ sung các `REQ-DELTA-###` và `BR-DELTA-###` tương ứng.

---

### Giai Đoạn 2: Lập Kế Hoạch Kỹ Thuật Delta (`plan.md`) — 🏛️ GATE 2

1. **Thiết Kế Phi Phá Hủy (Non-destructive Plan)**:
   - Bổ sung schema CSDL mới: Đảm bảo các cột mới là Nullable hoặc có Default value.
   - Bổ sung API endpoints hoặc DTOs mới (mở rộng backwards-compatible).
2. **🏛️ SA Thẩm Định Gate 2 Delta**:
   - SA rà soát migration, index, CQRS và xác nhận đạt chuẩn trước khi phân rã task.

---

### Giai Đoạn 3 & 3.1: Phân Rã Tasks Delta & Rà Soát Nhất Quán

1. **Thêm Phase Mới Vào Cuối `tasks.md` (Append-only)**:
   ```markdown
   ## Giai Đoạn N: Delta v2 — [Tên Nội Dung Bổ Sung]
   - [ ] `TASK-D1` [DB]: Tạo Migration schema phi phá hủy cho các trường mới.
   - [ ] `TASK-D2` [BE]: Cập nhật Domain Entity và Command/Query Handler.
   - [ ] `TASK-D3` [TEST]: Viết Unit Test cho các quy tắc `BR-DELTA-*`.
   - [ ] `TASK-D4` [FE-CREATE]: Bổ sung 100% các trường mới vào Form tạo/sửa (Controls coverage >= 80%).
   - [ ] `TASK-D5` [TEST]: Viết E2E Black-box test kiểm chứng toàn trình và đối soát CSDL thật.
   ```
2. **SA Rà Soát Tính Nhất Quán (`sa-analyze`)**:
   - Đảm bảo 100% bề mặt trong Cross-Surface Impact Matrix đã có task thực thi.

---

### Giai Đoạn 4: Lập Trình Thực Thi Delta Cô Lập Context (`Implement Delta`) — 🛑 CHECKPOINT 3

> [!CAUTION]
> **KỶ LUẬT CÔ LẬP CONTEXT CỦA DEV DELTA**:
> Agent điều phối **BẮT BUỘC DÙNG TOOL `invoke_subagent`** để kích hoạt Agent `dev` với Context riêng độc lập:
> ```json
> invoke_subagent(
>   TypeName: "dev",
>   Role: "Senior Full-Stack Developer",
>   Model: "flash",
>   Prompt: "Thực thi các task Delta mới trong specs/[epic-id]/tasks.md theo spec.md Delta và plan.md Delta. Đảm bảo form đủ 100% trường theo Wireframe, chạy migration non-destructive. Tự chạy build và regression test trong context của bạn. Khi xong, chỉ gửi báo cáo tóm tắt hoàn thành về cho Orchestrator."
> )
> ```

1. **Thực thi trong đúng module/layer tương ứng**:
   - Tạo migration phi phá hủy, cập nhật entity, use case.
   - Bổ sung input fields trên UI, bọc `<Async>`.
2. **Kỷ luật Zero-Mock**:
   - Cấm mảng tĩnh cố định thay cho API; cấm fallback fake data trong khối `catch`.
3. **Kiểm tra hồi quy liên tục (Regression Test)**:
   - 100% test cũ và mới đều pass. Build sạch 0 lỗi.

---

### Giai Đoạn 4.1: Kiểm Toán Đối Kháng SA Cho Delta (Gate 3 Delta Bắt Buộc) — 🛑 CHECKPOINT 3.5

> [!CAUTION]
> **KỶ LUẬT CÔ LẬP CONTEXT CỦA SA GATE 3 DELTA**:
> Agent điều phối kích hoạt **`techlead-sa`** qua `invoke_subagent`:
> ```json
> invoke_subagent(
>   TypeName: "techlead-sa",
>   Role: "Gate 3 Adversarial Reviewer",
>   Model: "flash",
>   Prompt: "Thực hiện Gate 3 Adversarial Review cho Delta vừa thi công của [epic-id]. Chạy ./scripts/guard-rails.sh và audit_wireframe_fields.py trong context của bạn. Thẩm định 6 trục kiểm soát. Chỉ khi 0 lỗi Critical mới ký duyệt GATE 3 DELTA APPROVED."
> )
> ```

1. **SA Kích hoạt Chốt chặn Tĩnh & Review Delta**:
   - Chạy `./scripts/guard-rails.sh` kiểm tra biên dịch, ranh giới kiến trúc, quét sạch mock routes/tokens.
   - Chạy `./scripts/audit_wireframe_fields.py`: Tỷ lệ controls trên giao diện $\ge 80\%$.
   - Kích hoạt `/pr-review-guard` rà soát theo 6 trục kiểm soát.
2. **Dev fix triệt để mọi lỗi CRITICAL**:
   - Chỉ khi SA ký duyệt **"GATE 3 DELTA APPROVED"**, mới chính thức chuyển sang Giai đoạn 5 bàn giao cho QC!

---

### Giai Đoạn 5: Đánh Giá Hội Tụ & Nghiệm Thu QC/PO (`Converge Delta`) — 🛡️ GATE 4 & GATE 5

> [!CAUTION]
> **KỶ LUẬT CÔ LẬP SUBAGENT QC (ZERO-CODE CONTEXT ISOLATION)**:
> Agent điều phối kích hoạt Agent `ec` qua `invoke_subagent` với **Zero-Code Payload**:
> ```json
> invoke_subagent(
>   TypeName: "ec",
>   Role: "Independent Black-Box QC",
>   Model: "flash",
>   Prompt: "Kiểm thử Pure Black-box cho Delta của [epic-id]. Bắt buộc test tài khoản thật, cấm mock token, đối soát CSDL thật."
> )
> ```

1. **Kiểm thử Black-Box Đa Tầng**:
   - Tầng 1: Unit & Invariants Test.
   - Tầng 2: Contract Test (API DTO compatibility).
   - Tầng 3: Database Integration Test (đối soát CSDL thật: bản ghi được INSERT/UPDATE chính xác).
   - Tầng 4: Playwright E2E Pure Black-Box (tài khoản thật, controls thật, không dùng `page.route()`).
2. **Kiểm toán độc lập Shadow QA**:
   - QA Agent chạy `./scripts/qa-shadow-sentinel.sh`, quét vi sai Git diff bắt mock ngầm, kiểm tra token context.
3. **Nghiệm thu Cuối cùng (Gate 5 Sign-off - PO DoD)**:
   - PO/PM (`po-pm`) đối soát tiêu chuẩn hoàn thành Definition of Done (`xong`).
   - Cập nhật Living Docs tại `docs/system/`.
   - Đổi trạng thái Epic trong Roadmap sang `✅ Hoàn thành (Delta vX)`.
