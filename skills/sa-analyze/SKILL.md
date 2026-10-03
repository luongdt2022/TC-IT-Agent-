---
name: sa-analyze
description: "Phân tích tính nhất quán chéo 3 chiều (Spec ↔ Plan ↔ Tasks Consistency Checker - Gate 2). Phát hiện mâu thuẫn, khoảng trống yêu cầu hoặc thiếu sót kỹ thuật trước khi cho phép bắt đầu lập trình."
---

# Kỹ Năng: sa-analyze (Phân Tích Tính Nhất Quán Chéo 3 Chiều - Gate 2)

> **Role Chịu Trách Nhiệm**: TL/SA Agent (`techlead-sa`) — Software Architect & Tech Lead.  
> **Cổng Kiểm Soát**: Gate 2 Pre-Implementation Quality Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Bộ 3 tài liệu của Epic tại `specs/[epic-id]/`:
  - `specs/[epic-id]/spec.md` (Đặc tả nghiệp vụ từ BA)
  - `specs/[epic-id]/plan.md` (Kế hoạch kỹ thuật từ SA)
  - `specs/[epic-id]/tasks.md` (Checklist công việc từ Dev/SA)
- **Target Output Action**: Xuất báo cáo thẩm định Gate 2 trực tiếp và cập nhật checklist xác nhận trong `specs/[epic-id]/checklist.md`.
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. 4 CHIỀU ĐỐI SOÁT NHẤT QUÁN BẮT BUỘC

1. **Chiều 1: Spec ➔ Plan (Độ Phủ Kiến Trúc)**:
   - Toàn bộ các yêu cầu `REQ-*` và quy tắc `BR-*` trong `spec.md` đã có tệp tin Entity, DTO, Command/Query hoặc Endpoint tương ứng được định nghĩa trong `plan.md` chưa?
2. **Chiều 2: Plan ➔ Tasks (Độ Phủ Công Việc)**:
   - Từng tệp tin được liệt kê trong `plan.md` (File Manifest) đã có task cụ thể trong `tasks.md` để tạo mới/chỉnh sửa chưa? Có file nào trong plan bị "bỏ quên" không có task làm không?
3. **Chiều 3: Tasks ➔ Spec (Khả Năng Kiểm Chứng Nghiệm Thu)**:
   - Từng task trong `tasks.md` có tiêu chí kiểm chứng rõ ràng không? Có task nào tự chế thêm tính năng không thuộc phạm vi `spec.md` không?
4. **Chiều 4: Database & API Alignment (Đồng Nhất Dữ Liệu)**:
   - Các trường dữ liệu trong `spec.md` có khớp 100% về tên, kiểu dữ liệu, ràng buộc null/not null với schema trong `plan.md` không?

---

## 3. PHÁN QUYẾT GATE 2
- **GATE 2 PASS (PHÊ DUYỆT)**: Không có mâu thuẫn chéo, phân rã công việc đầy đủ, sẵn sàng cho Dev Agent thực thi mã nguồn (`dev-code`).
- **GATE 2 BLOCKED (CHẶN)**: Phát hiện mâu thuẫn hoặc khoảng trống, yêu cầu BA hoặc SA cập nhật lại tài liệu trước khi gõ code.
