---
name: nacen-aggregate-srs
description: Tự động tổng hợp tài liệu SRS tổng thể Master từ tất cả các Living spec.md của từng Epic trong SourceCode/specs/, đồng thời xuất bản ra file Word DOCX theo chuẩn báo cáo nghiệm thu.
metadata:
  short-description: Tổng hợp Master SRS từ các Epic sống và xuất file Word
---

# NacenTech Master SRS Aggregation Skill (`nacen-aggregate-srs`)

## 1. Mục Tiêu & Cơ Chế Hoạt Động

Skill này hiện thực hóa nguyên tắc **"Living Modular SSOT"**:
- Trong suốt quá trình phát triển, các kỹ sư và BA liên tục cập nhật, tinh chỉnh chi tiết trong từng file `SourceCode/specs/00X-.../spec.md`.
- Khi cần báo cáo Tiến độ, Bàn giao Sản phẩm, hoặc Trình Hội đồng Nghiệm thu: Skill này sẽ tự động **quét và tổng hợp (Compile/Aggregate)** toàn bộ nội dung mới nhất từ các Epic để tạo ra:
  1. `Specification/SRS/NACENTECH_MASTER_SRS.md` (Markdown tổng thể chuẩn hóa 7 mục).
  2. `Specification/SRS/NACENTECH_MASTER_SRS.docx` (File Word hoàn chỉnh có trang bìa, mục lục, bảng biểu đẹp mắt).

---

## 2. Quy Trình Thực Thi 4 Bước

### Bước 1: Quét và Thu Thập Dữ Liệu Từ Các Epic
- Đọc file `SourceCode/specs/ROADMAP.md` để lấy danh sách các Epic đang hoạt động và thứ tự ưu tiên.
- Quét qua tất cả các thư mục `SourceCode/specs/00X-*/`:
  - Đọc `spec.md` của từng phân hệ: User Stories, `REQ-*`, `BR-*`, `DB-*`, `UI-*`, `API-*`, `NFR-*`.
  - Đọc tóm tắt kiến trúc từ `plan.md` (nếu có).

### Bước 2: Sắp Xếp Dữ Liệu Theo Cấu Trúc 7 Mục Chuẩn Hóa
Ghép nối nội dung theo đúng cấu trúc của `BA Agent/templates/TEMPLATE-SRS-7-muc.md`:
- **Mục 1: Quản trị & Siêu dữ liệu**: Bảng thông tin dự án, danh sách các phân hệ, ngày biên dịch tự động, version Master (ví dụ v1.1.0).
- **Mục 2: Bối cảnh, Mục tiêu & Phạm vi**: Trích xuất từ `Specification/PROJECT-BRIEF-NACENTECH.md` và các mục tiêu chung của hệ thống NacenTech.
- **Mục 3: Yêu cầu Chức năng Toàn Hệ thống**: Gom toàn bộ User Stories và danh mục `REQ-*` từ tất cả các Epic, phân loại theo từng phân hệ.
- **Mục 4: Giao diện & Luồng Người dùng**: Gom toàn bộ sơ đồ luồng, trạng thái UX và danh mục `UI-*`.
- **Mục 5: Quy tắc Nghiệp vụ & Cơ sở Dữ liệu**: Tổng hợp từ điển dữ liệu (`DB-*`) và ma trận quy tắc nghiệp vụ (`BR-*`), đặc biệt là bộ tiêu chí TRL 1–9 và phân loại ngành kinh tế VSIC.
- **Mục 6: Yêu cầu Phi chức năng (NFR)**: Tổng hợp bảng chỉ số đo lường hiệu năng (`NFR-*`).
- **Mục 7: Giao diện Dịch vụ & API Contracts**: Tổng hợp danh mục các điểm cuối `API-*` của toàn hệ thống.

### Bước 3: Ghi Nhận File Markdown Tổng Thể
- Ghi nội dung đã biên dịch vào `Specification/SRS/NACENTECH_MASTER_SRS.md`.
- Ghi nhận báo cáo hội tụ và thống kê: tổng số REQ, BR, DB, UI, API có mặt trong tài liệu.

### Bước 4: Tự Động Biên Dịch Ra File Word DOCX
- Kích hoạt script chuyển đổi:
  ```bash
  python3 "BA Agent/md-to-docx-review/scripts/md_to_docx.py" \
    "Specification/SRS/NACENTECH_MASTER_SRS.md" \
    "Specification/SRS/NACENTECH_MASTER_SRS.docx"
  ```
- Báo cáo đường dẫn file Word cho người dùng kèm bảng tóm tắt nội dung vừa tổng hợp.
