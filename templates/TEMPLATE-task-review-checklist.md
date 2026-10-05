# CHECKLIST TỰ RÀ SOÁT TASK (TASK-LEVEL REVIEW CHECKLIST)
*Dành cho Developer thực thi trong quá trình hoàn thành từng task trong `specs/TASK-XX/tasks.md`*

---

## 1. GIAI ĐOẠN 1: TRƯỚC KHI CODE (PRE-IMPLEMENTATION GROOMING)
- [ ] **Mã định danh nghiệp vụ**: Đã xác định rõ các mã `REQ-`, `BR-`, `DB-`, `UI-`, `API-` tương ứng với Task chưa?
- [ ] **Ranh giới tác động (Scope Boundary)**: Task này thuộc Backend, Frontend, hay Database Migration? Có đụng chạm đến module khác không?
- [ ] **Cross-Surface Impact**: Nếu thay đổi dữ liệu/trường (field), đã xem xét tác động đồng thời lên: DTO, Entity, Database Migration, Web UI, và Mobile App chưa?
- [ ] **Cơ chế xác thực & Phân quyền**: Task này có yêu cầu Scoped RBAC (Role, Scope, Action) hoặc phân tách quyền theo Tenant/Org không?

---

## 2. GIAI ĐOẠN 2: TRONG KHI TRIỂN KHAI (IMPLEMENTATION INTEGRITY)

### A. Đối với Backend (Clean Architecture / Service Layer)
- [ ] **Ranh giới tầng (Clean Architecture Boundary)**:
  - Controller / Endpoints chỉ nhận Handler/Service/Mediator, **TUYỆT ĐỐI CẤM** tiêm trực tiếp `DbContext` hay ORM context.
  - Tầng `Domain` không tham chiếu đến hạ tầng ngoài.
  - Tách bạch CQRS: Queries dùng read-only (NoTracking), trả về DTO; Commands thao tác qua Aggregate Root / Entity methods.
- [ ] **Database & ORM**:
  - Không có câu truy vấn N+1 (đã dùng Eager loading hoặc Select projection).
  - Migration phi phá hủy: Không xóa/đổi tên cột trực tiếp; cột mới có default value hoặc nullable.
  - Các bảng trạng thái quan trọng có Concurrency Token (Optimistic Locking).
- [ ] **Xử lý Biên & An Ninh**:
  - Đã validate đầu vào cho các trường null, empty, min/max length, số âm.
  - Chống IDOR: Mọi query/update dữ liệu sở hữu bắt buộc kèm điều kiện `TenantId` / `OrgId` / `UserId`.
  - Upload file: Bắt buộc kiểm tra Magic Bytes thực tế, giới hạn kích thước tối đa.
- [ ] **Bất đồng bộ & Hủy bỏ (Async/Await & Cancellation)**:
  - 100% các thao tác I/O, Database, Http đều dùng `async/await` kèm `CancellationToken` (nếu ngôn ngữ hỗ trợ).

### B. Đối với Frontend (React / Vue / Mobile)
- [ ] **Bao phủ 5 trạng thái UX qua `<Async>`**:
  - Đầy đủ 5 trạng thái: `Loading` (Skeleton) $\rightarrow$ `Empty` (mảng rỗng) $\rightarrow$ `Error` (kèm nút Thử lại) $\rightarrow$ `Success` (dữ liệu thật) $\rightarrow$ `Partial` (phân trang).
- [ ] **Chống Double Submit**:
  - Nút bấm Submit form tự động disable và hiển thị loading spinner ngay khi click.
- [ ] **Zero-Mock & SSOT Data**:
  - Không hardcode mảng dữ liệu danh mục tĩnh tại từng file page; dữ liệu dùng chung gọi qua hook/SDK tập trung.
  - Kết nối API thật qua Client SDK/Hook, không dùng mock state trong RAM.
- [ ] **Responsive & Text Overflow**:
  - Layout hiển thị chuẩn trên màn hình máy tính và thiết bị di động, không bị vỡ giao diện khi văn bản quá dài.

---

## 3. GIAI ĐOẠN 3: ĐỊNH NGHĨA HOÀN THÀNH TASK (TASK DEFINITION OF DONE - DoD)
- [ ] **Unit Test nghiệp vụ**: Đã viết Unit Test bao phủ 100% các quy tắc trong `BR-[MODULE]-[STT]` liên quan.
- [ ] **Kiểm thử cục bộ (Local Verification)**:
  - Backend: Build release pass 100% (0 Error, 0 Warning).
  - Frontend: Lint & Typecheck pass 100%.
- [ ] **Cập nhật tiến độ**: Đã tích `[x]` vào checkbox của task tương ứng trong `specs/TASK-XX/tasks.md`.
