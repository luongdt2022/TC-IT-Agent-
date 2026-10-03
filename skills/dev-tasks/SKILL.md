---
name: dev-tasks
description: "Phân rã danh sách công việc kỹ thuật chi tiết [BE]/[FE]/[Test] có tiêu chí kiểm chứng [x] bám sát 1:1 theo plan.md và spec.md."
---

# Kỹ Năng: dev-tasks (Phân Rã Checklist Công Việc Kỹ Thuật)

> **Role Chịu Trách Nhiệm**: Dev Agent (`dev`) — Senior Full-Stack Developer.  
> **Cổng Kiểm Soát**: Pre-Implementation Task Breakdown Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Đặc tả `specs/[epic-id]/spec.md` và kế hoạch kỹ thuật `specs/[epic-id]/plan.md`.
- **Target Output File**: `specs/[epic-id]/tasks.md`
- **NGHIÊM CẤM**: Không tạo các file task lẻ tẻ ngoài thư mục `specs/[epic-id]/`.

---

## 2. NGUYÊN TẮC PHÂN RÃ CÔNG VIỆC CHUẨN MỰC

1. **Tuần Tự Từng Tầng (Bottom-Up Execution Order)**:
   - Phase 1: Database Migration & Entities (`Domain` + `Infrastructure`)
   - Phase 2: Business Logic & Use Cases & Validators (`Application`)
   - Phase 3: Unit Tests cho Business Rules (`tests/unit/`)
   - Phase 4: API Controllers & Middlewares (`Presentation`)
   - Phase 5: Frontend UI Components với 5 UX States (`WebApp`)
   - Phase 6: E2E Integration & Verification (`tests/e2e/`)
2. **Quy Cách Đặt Tên Task**:
   - Từng task bắt buộc có mã prefix: `[BE]`, `[FE]`, `[DB]`, `[TEST]`.
   - Bắt buộc có tiêu chuẩn kiểm chứng cụ thể (Verification Criterion).

---

## 3. CẤU TRÚC CHUẨN TẬP TIN TASKS.MD

```markdown
# DANH SÁCH CÔNG VIỆC THỰC THI (TASKS MANIFEST): [TÊN EPIC]

- **Mã Epic**: [EPIC-ID]
- **Tình trạng**: [ ] 0/X Hoàn tất

## Giai Đoạn 1: CSDL & Thực Thể (Database & Domain)
- [ ] `TASK-01` [DB]: Tạo Migration schema bảng `users` kèm các cột, index và khóa ngoại.
  - *Kiểm chứng*: Chạy migration thành công trong CSDL.
- [ ] `TASK-02` [BE]: Định nghĩa Domain Entity `User` và các Value Objects.
  - *Kiểm chứng*: Khởi tạo Entity đúng ranh giới Clean Architecture.

## Giai Đoạn 2: Xử Lý Nghiệp Vụ & Validation (Application)
- [ ] `TASK-03` [BE]: Viết Command `RegisterUserCommand` và Handler xử lý.
  - *Kiểm chứng*: Use case xử lý ghi nhận dữ liệu hợp lệ.
- [ ] `TASK-04` [BE]: Viết FluentValidation kiểm tra `BR-AUTH-001` và `BR-AUTH-002`.
  - *Kiểm chứng*: Trả về validation error khi dữ liệu đầu vào sai.

## Giai Đoạn 3: Kiểm Thử Đơn Vị (Unit Testing)
- [ ] `TASK-05` [TEST]: Viết Unit Test bao phủ 100% các quy tắc `BR-AUTH-*`.
  - *Kiểm chứng*: Chạy lệnh test đơn vị đạt 100% Green.

## Giai Đoạn 4: Giao Diện Người Dùng (Frontend 5 UX States)
- [ ] `TASK-06` [FE]: Dựng form đăng ký bọc qua component `<Async>` hiển thị đủ 5 trạng thái UX: Loading, Empty, Error, Success, Updating.
  - *Kiểm chứng*: Render đúng UI trên trình duyệt web.
```
