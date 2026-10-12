---
name: traceability-auditor
description: "Chuyên gia Kiểm toán Truy vết Khép kín (Closed-Loop Traceability Auditor). Quét và kiểm tra tự động ma trận liên kết giữa REQ-, BR-, DB-, UI-, API- và Test Cases; phát hiện mã mồ côi và thiếu sót kiểm thử."
metadata:
  short-description: Kiểm toán và rà soát ma trận truy vết REQ- BR- DB- UI- API-
---

# Closed-Loop Traceability Auditor (`traceability-auditor`)

Skill chuyên trách dành cho **Agent BA** và **Agent QC** nhằm đảm bảo mọi yêu cầu nghiệp vụ đều được hiện thực hóa và kiểm thử trọn vẹn.

## 1. NGUYÊN TẮC TRUY VẾT BẮT BUỘC (TRACEABILITY INVARIANTS)
1. **Không Có Yêu Cầu Mồ Côi (No Orphan Requirements)**:
   - Mỗi `REQ-[MODULE]-[STT]` bắt buộc phải gắn kết với ít nhất một quy tắc nghiệp vụ `BR-*` và một điểm chạm người dùng `UI-*` hoặc dịch vụ `API-*`.
2. **Bao Phủ Dữ Liệu 100%**:
   - Mọi trường dữ liệu nghiệp vụ quan trọng phải tương ứng với một định danh cột/bảng trong `DB-[TABLE]-[STT]`.
3. **Bao Phủ Kiểm Thử Khép Kín**:
   - Mỗi `BR-*` phải có ít nhất một Unit Test kiểm chứng rẽ nhánh.
   - Mỗi `REQ-*` phải có kịch bản E2E Acceptance Test hoặc Manual Verification Test tương ứng.

## 2. QUY TRÌNH QUÉT & BÁO CÁO
Khi được kích hoạt trên một file spec hoặc thư mục module (`Specification/SRS/` hoặc `SourceCode/specs/`):

### Bước 1: Trích Xuất Toàn Bộ Mã Định Danh
Quét toàn bộ văn bản để thu thập danh sách:
- Danh sách `REQ-*`
- Danh sách `BR-*`
- Danh sách `DB-*`
- Danh sách `UI-*` / `API-*`

### Bước 2: Đối Soát Ma Trận Ánh Xạ
Kiểm tra từng cặp quan hệ:
- `REQ-*` $\rightarrow$ `BR-*`
- `REQ-*` $\rightarrow$ `UI-*` / `API-*`
- `BR-*` $\rightarrow$ `DB-*` (nếu có lưu trữ/tính toán)
- `BR-*` $\rightarrow$ Test case trong `tasks.md` hoặc code test.

### Bước 3: Xuất Biên Bản Thẩm Định Truy Vết
Xuất báo cáo dưới dạng bảng Markdown:
```markdown
### BÁO CÁO KIỂM TOÁN TRUY VẾT: [TÊN PHÂN HỆ]
- Tổng số REQ: ... | Tổng số BR: ... | Tổng số DB: ... | Tổng số API/UI: ...
- Độ bao phủ liên kết: ...%
- Cảnh báo mã mồ côi (Orphans):
  - [ ] REQ-XXX: Chưa có BR nào ràng buộc logic
  - [ ] BR-YYY: Chưa có Unit Test tương ứng trong tasks.md
- Kết luận: [PASS] Đạt chuẩn chuyển giao / [FAIL] Cần bổ sung trước khi handoff
```
