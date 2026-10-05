# QUY TRÌNH TOÀN TRÌNH TỰ ĐỘNG: wf-autopilot (TỪ ĐẶC TẢ ĐẾN MÃ NGUỒN HOÀN THIỆN)

> **Mã Quy Trình**: `wf-autopilot`  
> **Tác Tử Điều Phối**: **PO/PM Agent (`po-pm` / `tc-po`)** — Product Owner & Project Manager  
> **Các Tác Tử Phối Hợp**: **BA (`ba` / `tc-ba`)**, **TL/SA (`techlead-sa` / `tc-sa`)**, **Dev (`dev` / `tc-dev`)**, **EC (`ec` / `tc-ec`)**  
> **Cổng Kết Thúc**: Quality Gate 5 Final Acceptance & Shipped Release

---

## 1. MỤC TIÊU CỐT LÕI
Phát triển khép kín tự động toàn diện một Epic/Tính năng qua 7 chặng Stage-Gate nghiêm ngặt, tích hợp **Bộ chốt chặn chống ảo giác & Bảo vệ kiến trúc (Anti-Hallucination & Architecture Guardrails)**:
- Đặc tả nghiệp vụ chuẩn xác 7 mục (REQ-, BR-), làm rõ điểm nghẽn với `ba-clarify` (Cấm đoán mò).
- Thiết kế kiến trúc kỹ thuật chi tiết (C4, DB-, API-), lập kế hoạch với `sa-plan`.
- Phân rã công việc tuần tự có kiểm chứng `[x]` với `dev-tasks`.
- Lập trình thực thi chuẩn Clean Architecture, Pre-flight Grounding bắt buộc, thực thi nguyên tử 1 task/chu kỳ (Context < 15,000 tokens).
- Chốt chặn TypeCheck & Compiler toán học tĩnh (`./scripts/guard-rails.sh`).
- Kiểm thử 3 tầng khép kín với kỷ luật **Test Immobility** (Dev cấm sửa assertion của test để đối phó).
- Nghiệm thu Definition of Done (DoD), cập nhật Living Docs và Roadmap với kỹ năng `xong` (Gate 5).

---

## 2. BẢNG ĐIỀU HƯỚNG TỆP TIN ĐẦU RA (ENFORCED DIRECTORY CONTRACT)
Tất cả các tài liệu và mã nguồn BẮT BUỘC lưu tại:
- `specs/[epic-id]/spec.md` (Đặc tả SRS 7 mục)
- `specs/[epic-id]/plan.md` (Kế hoạch kỹ thuật & File Manifest)
- `specs/[epic-id]/tasks.md` (Checklist công việc thực thi [x])
- `src/` (hoặc `apps/`, `services/`: Mã nguồn phân tầng chuẩn)
- `tests/` (hoặc `__tests__/`: Kiểm thử Unit, Integration, E2E)
- `docs/system/<vùng>.md` (Living Docs phản ánh hiện trạng hệ thống)
- `docs/decisions/` (Architecture Decision Records - ADR)
- `docs/decisions/GATE4_VERIFICATION.md` (Biên bản kiểm định Gate 4)
- `docs/decisions/GATE5_ACCEPTANCE.md` (Biên bản nghiệm thu Gate 5)

---

## 3. CÁC CHẶNG THỰC THI TUẦN TỰ (7-STAGE CHOREOGRAPHY)

```mermaid
sequenceDiagram
    autonumber
    actor User as Con người (User)
    participant PO as PO/PM Agent (Nhạc trưởng)
    participant BA as BA Agent
    participant SA as TL/SA Agent
    participant Dev as Dev Agent
    participant EC as EC Agent

    User->>PO: "Kích hoạt wf-autopilot cho [epic-id]"
    activate PO
    
    Note over PO,BA: CHẶNG 1: ĐẶC TẢ NGHIỆP VỤ & LÀM RÕ (SPECIFY & CLARIFY)
    PO->>BA: Yêu cầu đặc tả Epic
    activate BA
    BA->>BA: Thực thi [ba-srs] (Soạn thảo SRS 7 mục)
    BA->>BA: Thực thi [ba-clarify] (Phát hiện & làm rõ các vùng mơ hồ - CẤM ĐOÁN MÒ)
    BA-->>PO: Sinh specs/[epic-id]/spec.md (Chuẩn xác 100%)
    deactivate BA

    Note over PO,SA: CHẶNG 2: THIẾT KẾ KỸ THUẬT (PLAN)
    PO->>SA: Chuyển spec.md, yêu cầu lập Plan kỹ thuật
    activate SA
    SA->>SA: Thực thi [sa-plan] & [sa-design]
    SA-->>PO: Sinh specs/[epic-id]/plan.md (Kèm File Manifest)
    deactivate SA

    Note over PO,Dev: CHẶNG 3: PHÂN RÃ CÔNG VIỆC (TASKS)
    PO->>Dev: Yêu cầu phân rã tasks
    activate Dev
    Dev->>Dev: Thực thi [dev-tasks]
    Dev-->>PO: Sinh specs/[epic-id]/tasks.md (Tuần tự hóa phụ thuộc)
    deactivate Dev

    Note over PO,SA: CHẶNG 4: THẨM ĐỊNH TÍNH NHẤT QUÁN GATE 2 (ANALYZE)
    PO->>SA: Thẩm định tính nhất quán chéo (spec vs plan vs tasks)
    activate SA
    SA->>SA: Thực thi [sa-analyze] (Chặn đứng mâu thuẫn kế hoạch)
    SA-->>PO: Xác nhận PASS Gate 2 (Đồng nhất 100%, không xung đột)
    deactivate SA

    Note over PO,Dev: CHẶNG 5: LẬP TRÌNH THỰC THI CHỐNG ẢO GIÁC (IMPLEMENT & CONVERGE)
    PO->>Dev: Lệnh thực thi code
    activate Dev
    Dev->>Dev: Pre-flight Grounding (Đọc UI Catalog & Data Schema)
    Dev->>Dev: Thực thi nguyên tử 1 task/chu kỳ (Context < 15,000 tokens)
    Dev->>Dev: Chạy chốt chặn tĩnh (./scripts/guard-rails.sh)
    Dev->>Dev: Thực thi [dev-code], [dev-uiux] & [dev-unit] (Tuân thủ Test Immobility)
    Dev->>Dev: Thực thi [dev-converge] (Đối soát quét sạch việc chưa làm)
    Dev-->>PO: Hoàn thành mã nguồn và tests (Hội tụ 100%)
    deactivate Dev

    Note over PO,SA: CHẶNG 5.1: CODE REVIEW GATE 3
    PO->>SA: Yêu cầu rà soát đối kháng mã nguồn
    activate SA
    SA->>SA: Chạy ./scripts/guard-rails.sh & [sa-review] & [sa-guard]
    SA-->>PO: Ký duyệt Gate 3 PASS
    deactivate SA

    Note over PO,EC: CHẶNG 6: KIỂM THỬ ĐỐI KHÁNG ĐA TẦNG (GATE 4)
    PO->>EC: Yêu cầu kiểm thử độc lập
    activate EC
    EC->>EC: Thực thi [ec-hunt] (Săn lỗi biên & ngoại lệ)
    EC->>EC: Thực thi [ec-fuzz] (Fuzzing bảo mật & phân quyền)
    EC->>EC: Thực thi [ec-e2e] (Sinh test Playwright / E2E Visual QA)
    EC->>EC: Thực thi [ec-test] (Chạy toàn bộ test suite 3 tầng)
    EC-->>PO: Xuất docs/decisions/GATE4_VERIFICATION.md [PASS]
    deactivate EC

    Note over PO,User: CHẶNG 7: NGHIỆM THU XUẤT XƯỞNG (GATE 5)
    PO->>PO: Thực thi [xong] (Kiểm tra DoD, cập nhật Living Docs, chuyển Shipped)
    PO->>PO: Xuất docs/decisions/GATE5_ACCEPTANCE.md
    PO->>PO: Cập nhật ROADMAP.md sang [SHIPPED]
    PO-->>User: "Đã hoàn thành xuất sắc Epic [epic-id]!"
    deactivate PO
```
