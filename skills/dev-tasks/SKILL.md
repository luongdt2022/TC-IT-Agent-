---
name: dev-tasks
description: "Phân rã danh sách công việc kỹ thuật chi tiết [BE]/[FE]/[Test] có tiêu chí kiểm chứng [x] bám sát 1:1 theo plan.md và spec.md, tuân thủ kỷ luật 5 Entity Lifecycle và 5 UX States."
---

# Kỹ Năng: dev-tasks (Phân Rã Checklist Công Việc Kỹ Thuật)

> **Role Chịu Trách Nhiệm**: Dev Agent (`dev`) — Senior Full-Stack Developer.  
> **Cổng Kiểm Soát**: Pre-Implementation Task Breakdown Gate (Gate 2).

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
   - Phase 5: Frontend UI Components với 5 Hành vi Entity Lifecycle & 5 UX States (`WebApp`)
   - Phase 6: E2E Integration & Verification (`tests/e2e/`)

2. **KỶ LUẬT BẮT BUỘC: 5 HÀNH VI VÒNG ĐỜI THỰC THỂ (MANDATORY ENTITY LIFECYCLE)**:
   Mọi phân hệ nghiệp vụ có dữ liệu bắt buộc phải bóc tách đủ 5 hành vi tương ứng theo sơ đồ định tuyến và phân quyền:
   - `[FE-LIST]`: Danh sách hiển thị, bộ lọc đa tiêu chí, phân trang kèm 5 UX states (`<Async>`).
   - `[FE-DETAIL]`: Màn hình xem chi tiết bản ghi (Read-only, masking cho dữ liệu nhạy cảm).
   - `[FE-CREATE]`: Form tạo mới đầy đủ 100% trường dữ liệu theo Wireframe HTML gốc.
   - `[FE-EDIT]`: Form chỉnh sửa bản nháp (Draft edit) cho chủ sở hữu (`Owner`) có Optimistic Locking.
   - `[FE-STATUS]`: Luồng chuyển đổi trạng thái (Gửi duyệt, Thu hồi, Đóng hồ sơ, Soft-delete).
   *(Nếu task thuần hạ tầng không có UI thì bỏ qua; nếu có UI mà thiếu bất kỳ hành vi nào trong 5 hành vi trên thì SA lập tức đánh rớt Gate 2).*

3. **Quy Cách Đặt Tên Task**:
   - Từng task bắt buộc có mã prefix: `[BE]`, `[FE]`, `[DB]`, `[TEST]`.
   - Bắt buộc có tiêu chuẩn kiểm chứng cụ thể (Verification Criterion).

---

## 3. CẤU TRÚC CHUẨN TẬP TIN TASKS.MD

```markdown
# DANH SÁCH CÔNG VIỆC THỰC THI (TASKS MANIFEST): [TÊN EPIC]

- **Mã Epic**: [EPIC-ID]
- **Tình trạng**: [ ] 0/X Hoàn tất

## Giai Đoạn 1: CSDL & Thực Thể (Database & Domain)
- [ ] `TASK-01` [DB]: Tạo Migration schema bảng `entities` kèm các cột, index và khóa ngoại.
  - *Kiểm chứng*: Chạy migration thành công trong CSDL.
- [ ] `TASK-02` [BE]: Định nghĩa Domain Entity và các Value Objects.
  - *Kiểm chứng*: Khởi tạo Entity đúng ranh giới Clean Architecture.

## Giai Đoạn 2: Xử Lý Nghiệp Vụ & Validation (Application)
- [ ] `TASK-03` [BE]: Viết Command/Query và Handler xử lý.
  - *Kiểm chứng*: Use case xử lý ghi nhận dữ liệu hợp lệ.
- [ ] `TASK-04` [BE]: Viết FluentValidation kiểm tra `BR-*`.
  - *Kiểm chứng*: Trả về validation error khi dữ liệu đầu vào sai.

## Giai Đoạn 3: Kiểm Thử Đơn Vị (Unit Testing)
- [ ] `TASK-05` [TEST]: Viết Unit Test bao phủ 100% các quy tắc `BR-*`.
  - *Kiểm chứng*: Chạy lệnh test đơn vị đạt 100% Green.

## Giai Đoạn 4: Giao Diện Người Dùng (Frontend 5 Entity Lifecycle & 5 UX States)
- [ ] `TASK-06` [FE-LIST]: Dựng màn hình danh sách `/portal/...` bọc qua `<Async>` (5 UX States: Loading, Empty, Error, Success, Partial).
- [ ] `TASK-07` [FE-DETAIL]: Dựng màn hình xem chi tiết hồ sơ `/portal/.../[id]` có data masking.
- [ ] `TASK-08` [FE-CREATE]: Dựng form tạo mới 100% trường dữ liệu theo wireframe HTML gốc (Controls coverage >= 80%).
- [ ] `TASK-09` [FE-EDIT]: Dựng form chỉnh sửa bản nháp có kiểm tra quyền Owner và Optimistic Locking.
- [ ] `TASK-10` [FE-STATUS]: Cài đặt hành động chuyển trạng thái hồ sơ (Gửi duyệt / Hủy bỏ).

## Giai Đoạn 5: Kiểm Thử Độc Lập & Xác Minh (QC Gate 4)
- [ ] `TASK-11` [TEST]: Viết E2E Black-box test (Zero-Mock, Real DB Query assertion).
  - *Kiểm chứng*: Test chạy xanh trên môi trường thật, 0 mock token.
```
