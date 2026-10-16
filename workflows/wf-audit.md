# QUY TRÌNH KIỂM TOÁN TOÀN DIỆN: wf-audit (KIỂM TOÁN HỘI TỤ, TRUY VẾT, ZERO-MOCK & SHADOW QA)

> **Mã Quy Trình**: `wf-audit`  
> **Tác Tử Chủ Trì**: **QA Lead (`qa`)** & **TL/SA Agent (`techlead-sa`)**  
> **Tác Tử Phối Hợp**: **BA Agent (`ba`)**, **EC/QC Agent (`ec`)**, **Dev Agent (`dev`)**, **PO/PM (`po-pm`)**  
> **Cổng Kết Thúc**: Pre-Release Audit Sign-off (Quality Gate 5 Go/No-Go)

---

## 1. MỤC TIÊU CỐT LÕI
Chạy định kỳ cuối mỗi Sprint hoặc trước các đợt phát hành lớn (Release):
1. **Kiểm toán Ranh giới Kiến trúc**: Quét toàn bộ mã nguồn để đảm bảo không có rò rỉ CSDL, vi phạm phân tầng Clean Architecture (`sa-guard`, `clean-arch-guard`).
2. **Kiểm toán Chốt chặn Tĩnh & Compiler**: Chạy `./scripts/guard-rails.sh` đảm bảo 0 lỗi biên dịch, 0 lỗi Schema validation.
3. **Kiểm toán Độ phủ Trường Biểu mẫu**: Chạy `./scripts/audit_wireframe_fields.py` đảm bảo tỷ lệ interactive controls so với Wireframe HTML gốc $\ge 80\%$.
4. **Kiểm toán Truy vết Khép kín**: Quét ma trận `REQ-` ↔ `BR-` ↔ `DB-` ↔ `API-` ↔ `Test` (`traceability-auditor`, `ba-trace`).
5. **Kiểm toán Triệt tiêu Mock Ngầm & Đối soát CSDL thật**: Quét sạch dữ liệu giả (`fakeItem`, dummy array trong `catch`), kiểm tra bài test QC query CSDL thật.
6. **Kiểm toán Trí nhớ & An toàn Context**: Đo Token Context (ngưỡng 60% - 80%) và kẹp chốt chặn chống code chay qua `./scripts/qa-shadow-sentinel.sh`.
7. **Kiểm toán Mức độ Hội tụ Mã Nguồn**: Đảm bảo toàn bộ task trong `specs/` đã được chuyển sang `[x]` và khớp với code chạy thực tế.

---

## 2. BẢNG ĐIỀU HƯỚNG TỆP TIN ĐẦU RA (ENFORCED DIRECTORY CONTRACT)
- Báo cáo kiểm toán tổng thể BẮT BUỘC lưu tại:
  `docs/decisions/AUDIT_REPORT.md`
- Cập nhật ma trận truy vết tại:
  `docs/decisions/TRACEABILITY_MATRIX.md`

---

## 3. CÁC BƯỚC THỰC THI 6 TẦNG

### Tầng 1: Quét Ranh Giới Kiến Trúc & Guardrails [TL/SA Agent]
- **Kỹ năng sử dụng**: `sa-guard`, `clean-arch-guard`
- Chạy `./scripts/guard-rails.sh`. Quét tĩnh dependencies, chặn rò rỉ hạ tầng/CSDL lên tầng trên, vi phạm phân tầng kiến trúc và rò rỉ dữ liệu ngoài phạm vi.

### Tầng 2: Quét Ma Trận Truy Vết Khép Kín [BA Agent]
- **Kỹ năng sử dụng**: `ba-trace`, `traceability-auditor`
- Đối soát toàn bộ `spec.md` với mã nguồn và tests. Phát hiện mã mồ côi (không có yêu cầu) hoặc yêu cầu bị bỏ quên chưa lập trình.

### Tầng 3: Đánh Giá Độ Bao Phủ Kiểm Thử & Fuzzing [EC/QC Agent]
- **Kỹ năng sử dụng**: `ec-test`, `ec-fuzz`, `rbac-permission-fuzzer`, `ec-contract`, `ec-mutation`
- Chạy toàn bộ test suite 4 tầng. Thực hiện fuzzing ma trận phân quyền RBAC và kiểm tra góc khuất dữ liệu. Xuất báo cáo % coverage và Mutation score.

### Tầng 4: Đối Soát Mức Độ Hội Tụ Mã Nguồn [Dev Agent]
- **Kỹ năng sử dụng**: `dev-converge`
- Đối soát toàn diện các checklist `tasks.md` trong mọi Epic đối chiếu với mã nguồn thực tế. Đảm bảo 100% công việc đã hội tụ trọn vẹn, không có đầu việc dở dang.

### Tầng 5: Kiểm Toán Shadow QA & Triệt Tiêu Mock Ngầm [QA Agent]
- **Kỹ năng sử dụng**: `qa-shadow-sentinel`, `qa-gate-audit`
- Chạy `./scripts/qa-shadow-sentinel.sh`:
  - Đo Token Context (Cảnh báo 60%, Báo động đỏ 80%).
  - Quét Git diff phát hiện mock ngầm, fallback fake data.
  - Kiểm toán bài test QC: Cấm Shallow Assertion (`is_visible()`), bắt buộc đối soát CSDL thật.
  - Chạy `./scripts/audit_wireframe_fields.py` đảm bảo không bị cắt xén controls biểu mẫu.

### Tầng 6: Quét Kỷ Luật Thư Mục Chống Rác & Xuất Báo Cáo Tổng Hợp [QA & SA Agent]
- **Kỹ năng sử dụng**: `sa-analyze`, `xong`
- Quét cây thư mục toàn dự án theo quy tắc Zero-Tolerance Root Dumping.
- Xuất bản Release Readiness Scorecard tại `docs/decisions/AUDIT_REPORT.md` với phán quyết:
  `[AUDIT PASS - READY FOR PRODUCTION / RELEASE GO]` hoặc `[AUDIT FAILED - ACTION ITEMS REQUIRED / RELEASE NO-GO]`.
