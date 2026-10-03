---
name: sa-review
description: "Rà soát mã nguồn đối kháng (Adversarial Code Review - Gate 3). Thẩm định code của Dev bằng tư duy hoài nghi khắt khe: tìm kiếm điểm nghẽn hiệu năng, lỗi N+1 query, rò rỉ bộ nhớ, race conditions và lỗ hổng bảo mật trước khi chuyển sang QC."
---

# Kỹ Năng: sa-review (Rà Soát Mã Nguồn Đối Kháng - Gate 3)

> **Role Chịu Trách Nhiệm**: TL/SA Agent (`techlead-sa`) — Software Architect & Tech Lead.  
> **Cổng Kiểm Soát**: Gate 3 Code Review & Technical Approval Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Mã nguồn do Dev Agent triển khai trong `src/` và danh sách công việc `specs/[epic-id]/tasks.md`.
- **Target Output File**: `docs/decisions/CODE_REVIEW_GATE3.md`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. 7 TIÊU CHÍ RÀ SOÁT ĐỐI KHÁNG BẮT BUỘC (ADVERSARIAL CHECKLIST)

SA Agent tiếp cận mã nguồn với con mắt hoài nghi, kiểm tra tối thiểu 7 khía cạnh then chốt:

1. **Hiệu Năng CSDL & Lỗi N+1 Query**:
   - Kiểm tra các truy vấn Entity Framework / Prisma: Có bị duyệt vòng lặp `foreach` rồi gọi query trong loop không? Có thiếu `.AsNoTracking()` cho truy vấn đọc không? Có thiếu Index cho các cột trong mệnh đề `WHERE` hay `JOIN` không?
2. **Xử Lý Bất Đồng Bộ & Khóa Lạc Quan (Async & Concurrency)**:
   - Các hàm async có dùng `await` đúng cách không? Có nguy cơ dead-lock không? Các nghiệp vụ cập nhật số dư, tồn kho, trạng thái có cơ chế khóa lạc quan chống Race Condition không?
3. **Idempotency & Khả Năng Tự Phục Hồi**:
   - Nếu client gửi lại cùng 1 request do rớt mạng (Retry), API có xử lý an toàn không hay tạo 2 bản ghi trùng lặp?
4. **Bảo Mật & Phân Quyền (Security & Scoped RBAC)**:
   - Có kiểm tra quyền hạn (Role/Scope) trên endpoint không? Có nguy cơ tấn công IDOR (sửa ID trên URL để đọc/sửa dữ liệu của người khác) không?
5. **Xử Lý Lỗi & Quản Lý Exception**:
   - Có dùng `try-catch` nuốt lỗi ngầm (Empty catch block) không? Lỗi trả về client có bị lộ StackTrace hay thông tin nhạy cảm của CSDL không?
6. **Bao Phủ Unit Test**:
   - Các Business Rules (`BR-*`) trong `spec.md` đã có Unit Test tương ứng trong `tests/unit/` chưa?
7. **Clean Code & Đặt Tên**:
   - Mã nguồn có dễ đọc, biến/hàm đặt tên rõ nghĩa không? Có tồn tại mã thừa, comment vô nghĩa không?

---

## 3. KẾT LUẬN REVIEW GATE 3
- **PASS**: Đạt toàn bộ 7 tiêu chí. Ký duyệt cho phép chuyển mã nguồn sang cho EC Agent tiến hành kiểm thử 3 tầng (Gate 4).
- **REQUEST CHANGES**: Chỉ rõ từng file, số dòng, mô tả lỗi và giải pháp khắc phục yêu cầu Dev sửa lại.
