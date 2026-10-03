---
name: po-course
description: "Kỹ năng Nắn dòng & Chống Trôi dạt Nghiệp vụ (Course Correction Specialist). Đối chiếu trạng thái mã nguồn và spec hiện tại với mục tiêu ban đầu của Basic Design; phát hiện độ lệch (Requirement Drift) và lập kế hoạch đưa dự án trở lại đúng quỹ đạo."
---

# Kỹ Năng: po-course (Nắn Dòng & Chống Trôi Dạt Dự Án)

> **Role Chịu Trách Nhiệm**: PO/PM Agent (`po-pm`) — Product Owner & Project Manager.  
> **Cổng Kiểm Soát**: Scope Alignment & Anti-Drift Gatekeeper.

---

## 1. NGUYÊN TẮC NẮN DÒNG (COURSE CORRECTION PRINCIPLES)

1. **Phát Hiện Trôi Dạt Sớm (Early Drift Detection)**:
   - Dự án rất dễ bị trôi dạt khi Dev mải mê tối ưu kỹ thuật (Over-engineering), BA viết thêm tính năng ngoài tầm nhìn, hoặc QC phát hiện lỗi rồi tự ý sửa flow.
2. **So Sánh Ba Điểm Neo (Three-Point Anchor Comparison)**:
   - Điểm neo 1: Tầm nhìn gốc & Ranh giới trong `docs/01-basic-design/BD-00-overview.md`.
   - Điểm neo 2: Đặc tả kỹ thuật hiện tại trong `specs/[epic-id]/spec.md`.
   - Điểm neo 3: Mã nguồn thực tế đã code trong `src/`.

---

## 2. QUY TRÌNH THỰC THI 3 BƯỚC

### Bước 1: Đo Lường Độ Lệch (Delta Measurement)
- Quét và liệt kê các điểm khác biệt:
  - Những gì có trong code nhưng không có trong Basic Design ban đầu (Unplanned Scope).
  - Những gì có trong Basic Design nhưng bị cắt bỏ hoặc làm sai lệch (Missing Intent).

### Bước 2: Phân Loại Mức Độ Trôi Dạt
- **Mức Nhẹ (Minor Drift)**: Sai khác về tên trường, format UI $\rightarrow$ Điều chỉnh spec hoặc code cho khớp.
- **Mức Trung Bình (Scope Drift)**: Thêm chức năng phụ ngoài MVP $\rightarrow$ Cắt gọt, dời sang P2/Post-MVP trong `backlog/`.
- **Mức Nghiêm Trọng (Architectural Drift)**: Sai lệch luồng nghiệp vụ cốt lõi $\rightarrow$ Dừng code ngay lập tức (HALT), triệu tập `po-party` để tái định vị.

### Bước 3: Lập Kế Hoạch Đưa Về Quỹ Đạo (Recovery Plan)
- Xuất danh sách các việc cần xóa (Deprecate), việc cần sửa (Refactor) và cập nhật lại `specs/[epic-id]/tasks.md`.
