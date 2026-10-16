---
name: "speckit-uiux"
description: "Senior Product Designer & Visual QA Specialist: Thiết kế layout theo HTML Wireframe Basic Design, chuẩn hóa 5 trạng thái UX qua <Async>, phân quyền 3D Scoped RBAC UI và tự động chụp ảnh Visual QA bằng Playwright."
compatibility: "Requires Frontend Submodule (SourceCode/frontend/ or frontend/) with Playwright"
metadata:
  author: "Enterprise Architecture Team"
  source: "custom/speckit-uiux"
  version: "2.4.0"
---

# Kỹ Năng Thiết Kế Giao Diện & Kiểm Thử Trực Quan Enterprise (`speckit-uiux`)

## 1. Mục Đích & Vai Trò
Khi dự án bước vào giai đoạn thiết kế và thi công giao diện Frontend tại `SourceCode/frontend/` (hoặc `frontend/`), skill này đóng vai trò là **Senior Product Designer & Visual QA Specialist**:
1. **Bảo toàn 100% nghiệp vụ từ Basic Design**:
   - Đối soát trực tiếp với các file HTML Wireframe mô phỏng trong tài liệu Basic Design (`Specification/02_BASIC_DESIGN/` hoặc `docs/design/`).
   - Đối chiếu danh mục trường thông tin và controls tương tác; tỷ lệ bao phủ controls wireframe phải đạt tối thiểu $\ge 80\%$.
2. **Quy chuẩn Enterprise Design System**:
   - **Bảng màu chủ đạo**: Primary Blue/Navy (`#1e40af`), Accent Cyan (`#06b6d4`), Success Emerald (`#10b981`), Neutral Slate (`#0f172a`).
   - Hỗ trợ mượt mà **Light / Dark Mode**.
   - Typography: Font chữ hiện đại `Plus Jakarta Sans` hoặc `Inter` cho text tiếng Việt chuẩn UTF-8, `JetBrains Mono` cho mã định danh.
3. **Chuẩn hóa trải nghiệm người dùng vi mô (Micro-UX)**:
   - Bắt buộc mọi View/Screen đều có đủ 5 trạng thái tương tác bọc trong component `<Async>`.
4. **Phân quyền giao diện theo ngữ cảnh (3D Scoped RBAC UI)**:
   - Kiểm soát trường thông tin và nút bấm theo PlatformRoles và ScopeTypes (Global, Tenant, Department, User).
5. **Nghiệm thu trực quan thực tế (Visual QA)**:
   - Tự động dùng Playwright chụp ảnh màn hình ở 2 độ phân giải Desktop (1440×900) và Mobile (390×844).

---

## 2. Quy Trình Thiết Kế UI/UX 5 Bước Chi Tiết

### Bước 1: Khảo Sát Wireframe Từ Basic Design
Tra cứu chính xác file HTML mockup tương ứng với Task/Epic đang thực hiện:
- Đọc file wireframe mẫu tương ứng, lập danh mục toàn bộ inputs, buttons, tables, filters, modals.
- Chạy script kiểm toán đối soát nếu có: `python scripts/audit_wireframe_fields.py`.

### Bước 2: Bố Cục Giao Diện (Layout Specification)
- **Desktop (>= 1280px)**:
  - Header: Logo dự án, Menu điều hướng, thanh tìm kiếm thông minh, Avatar và Scope Badge.
  - Main Layout: Thường chia 2 cột: Cột trái (25-30%) là Bộ lọc đa tầng hoặc Menu quản trị; Cột phải (70-75%) là Bảng dữ liệu / Form nhập liệu.
- **Mobile (< 768px)**:
  - Tự động co về 1 cột dọc (Single column responsive).
  - Bộ lọc nâng cao được đưa vào Bottom Sheet / Drawer trượt từ dưới lên.
  - Các nút hành động chính (Duyệt, Lưu, Nộp hồ sơ) dính cố định ở đáy màn hình (Sticky Bottom Bar).

### Bước 3: Ánh Xạ UI Components Chuẩn Hóa
Không viết style ad-hoc, bắt buộc dùng các components dùng chung trong `frontend/src/components/`:
- `<FormField>`: Tự động render Label, cờ bắt buộc `*`, tooltip giải thích, thông báo lỗi inline đỏ khi vi phạm rule.
- `<LoadingButton>`: Chống click đúp, tự động xoay Spinner và disabled khi đang gọi API.
- `<StatusBadge>`: Component hiển thị huy hiệu trạng thái với màu sắc trực quan tương ứng (Draft, Pending, Active, Rejected, Inactive).
- `<Toast>`: Thông báo nổi góc trên/dưới xác nhận lưu thành công hoặc cảnh báo.

### Bước 4: Chuẩn Hóa 5 Trạng Thái UX Bắt Buộc (`<Async>`)
Mọi màn hình gọi dữ liệu từ API Backend bắt buộc phải bọc trong component cấu trúc:
```tsx
<Async status={queryStatus}>
  <Async.Loading>
    <TableSkeleton rows={5} />
  </Async.Loading>
  <Async.Empty 
    message="Không tìm thấy bản ghi nào phù hợp với bộ lọc." 
    actionLabel="Đặt lại bộ lọc" 
    onAction={resetFilter} 
  />
  <Async.Error 
    message={error.message} 
    onRetry={refetch} 
  />
  <Async.Success>
    {(data) => <RecordList items={data.items} />}
  </Async.Success>
  <Async.Partial>
    {(data) => <RecordList items={data.items} isLoadingMore={true} />}
  </Async.Partial>
</Async>
```

### Bước 5: Kiểm Thử Trực Quan Visual QA Bằng Playwright
1. **Kịch bản chụp ảnh tự động**:
   - Sử dụng Playwright headless mở trang ở 2 độ phân giải:
     + **Desktop**: 1440 × 900
     + **Mobile**: 390 × 844 (iPhone)
   - Lưu ảnh vào: `SourceCode/frontend/tests/visual-qa/screenshots/<task-id>/<screen-name>-desktop.png` và `-mobile.png`.
2. **Đối soát & Báo cáo**:
   - So sánh ảnh chụp thực tế với wireframe HTML nguồn trong Basic Design để đảm bảo độ chuẩn xác.

---

## 3. Tiêu Chí Nghiệm Thu UI/UX (Definition of Done)
- [ ] Khớp $\ge 80\%$ các trường dữ liệu và controls tương tác từ file HTML Wireframe Basic Design.
- [ ] Tuân thủ bảng màu chuẩn của Design System và hoạt động mượt mà ở cả Light/Dark Mode.
- [ ] 100% các màn hình có đủ 5 trạng thái UX xử lý qua `<Async>`.
- [ ] Giao diện tự động thích ứng hoàn hảo giữa Desktop (1440px) và Mobile (390px).
- [ ] Đã chạy Playwright chụp ảnh Visual QA đầy đủ và lưu vào thư mục screenshots.
- [ ] Không có nút chết, không có dummy array giả lập trong khối `catch` (Tuân thủ Zero-Mock).
