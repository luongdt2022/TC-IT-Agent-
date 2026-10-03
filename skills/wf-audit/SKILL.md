# QUY TRÌNH KIỂM TOÁN TOÀN DIỆN: wf-audit (KIỂM TOÁN HỘI TỤ, TRUY VẾT & DỌN RÁC)

> **Mã Quy Trình**: `wf-audit`  
> **Tác Tử Chủ Trì**: **TL/SA Agent (`techlead-sa`)**  
> **Tác Tử Phối Hợp**: **BA Agent (`ba`)**, **EC Agent (`ec`)**  
> **Cổng Kết Thúc**: Pre-Release Audit Sign-off

---

## 1. MỤC TIÊU CỐT LÕI
Chạy định kỳ cuối mỗi Sprint hoặc trước các đợt phát hành lớn (Release):
1. **Kiểm toán Ranh giới Kiến trúc**: Quét toàn bộ mã nguồn `src/` để đảm bảo không có rò rỉ CSDL hay vi phạm Clean Architecture.
2. **Kiểm toán Truy vết Khép kín**: Quét ma trận `REQ-` ↔ `BR-` ↔ `DB-` ↔ `API-` ↔ `Test`, phát hiện mã mồ côi hoặc yêu cầu thiếu test.
3. **Kiểm toán Kỷ luật Thư mục Chống Rác**: Đảm bảo thư mục gốc (`root`) tuyệt đối sạch sẽ, không có file rác.
4. **Kiểm toán Mức độ Hội tụ Mã Nguồn**: Đảm bảo toàn bộ task trong `specs/` đã được chuyển sang `[x]` và khớp với code chạy thực tế.

---

## 2. BẢNG ĐIỀU HƯỚNG TỆP TIN ĐẦU RA (ENFORCED DIRECTORY CONTRACT)
- Báo cáo kiểm toán tổng thể BẮT BUỘC lưu tại:
  `docs/decisions/AUDIT_REPORT.md`
- Cập nhật ma trận truy vết tại:
  `docs/decisions/TRACEABILITY_MATRIX.md`

---

## 3. CÁC BƯỚC THỰC THI 4 TẦNG

### Tầng 1: Quét Ranh Giới Kiến Trúc [TL/SA Agent]
- **Kỹ năng sử dụng**: `sa-guard`
- Quét tĩnh dependencies, chặn rò rỉ `DbContext`, rò rỉ Presentation xuống Domain và vi phạm Clean Architecture.

### Tầng 2: Quét Ma Trận Truy Vết Khép Kín [BA Agent]
- **Kỹ năng sử dụng**: `ba-trace`
- Đối soát toàn bộ `spec.md` với `src/` và `tests/`. Phát hiện mã mồ côi (không có yêu cầu) hoặc yêu cầu bị bỏ quên chưa lập trình.

### Tầng 3: Đánh Giá Độ Bao Phủ Kiểm Thử & Fuzzing [EC Agent]
- **Kỹ năng sử dụng**: `ec-test` & `ec-fuzz`
- Chạy toàn bộ test suite 3 tầng (Unit, Integration, E2E). Thực hiện fuzzing ma trận phân quyền RBAC và kiểm tra góc khuất dữ liệu. Xuất báo cáo % coverage.

### Tầng 4: Đối Soát Mức Độ Hội Tụ Mã Nguồn [Dev Agent]
- **Kỹ năng sử dụng**: `dev-converge`
- Đối soát toàn diện các checklist `tasks.md` trong mọi Epic đối chiếu với mã nguồn thực tế. Đảm bảo 100% công việc đã hội tụ trọn vẹn, không có đầu việc dở dang.

### Tầng 5: Quét Kỷ Luật Thư Mục Chống Rác & Xuất Báo Cáo Tổng Hợp [TL/SA Agent]
- **Kỹ năng sử dụng**: `sa-analyze`
- Quét cây thư mục toàn dự án theo quy tắc Zero-Tolerance Root Dumping. Nếu có file lạ ở root hoặc sai vị trí, lập danh sách chấn chỉnh hoặc gom về đúng thư mục quy định.
- Xuất báo cáo tổng kết tại `docs/decisions/AUDIT_REPORT.md` với phán quyết: `[AUDIT PASS - READY FOR PRODUCTION]` hoặc `[AUDIT FAILED - ACTION ITEMS REQUIRED]`.
