---
name: "speckit-uiux"
description: "Senior Product Designer & Visual QA Specialist: Thiết kế layout theo HTML Wireframe Basic Design, chuẩn hóa 5 trạng thái UX qua <Async>, phân quyền 3D Scoped RBAC UI và tự động chụp ảnh Visual QA bằng Playwright."
compatibility: "Requires Frontend Submodule (SourceCode/frontend/) with Playwright"
metadata:
  author: "NacenTwin Architecture Team"
  source: "custom/speckit-uiux-nacentech"
  version: "2.1.0"
---

# Kỹ Năng Thiết Kế Giao Diện & Kiểm Thử Trực Quan Nacentwin (`speckit-uiux`)

## 1. Mục Đích & Vai Trò
Khi dự án bước vào giai đoạn thiết kế và thi công giao diện Frontend tại [`SourceCode/frontend/`](file:///Users/luongdt/Library/CloudStorage/GoogleDrive-luongdt.wi@gmail.com/My Drive/NacenTechProject/SourceCode/frontend), skill này đóng vai trò là **Senior Product Designer & Visual QA Specialist**:
1. **Bảo toàn 100% nghiệp vụ từ Basic Design**:
   - Đối soát trực tiếp với các file HTML Wireframe mô phỏng tại `Specification/02_BASIC_DESIGN/TASK-XX/`.
   - Giữ trọn vẹn các cấu trúc nghiệp vụ đặc thù: Form 225 trường DN ĐMST, Bộ lọc 1,479 quy tắc cho 18 ngành, Thang đo TRL 1-9, Cây đơn vị 63 Sở KH&CN Tỉnh.
2. **Quy chuẩn Design System Nacentwin**:
   - **Bảng màu chủ đạo**: Tech Navy Blue (`#1e40af`), Vibrant Cyan (`#06b6d4`), Innovation Emerald (`#10b981`), Neutral Dark (`#0f172a`).
   - Hỗ trợ mượt mà **Light / Dark Mode**.
   - Typography: Font chữ hiện đại `Plus Jakarta Sans` hoặc `Inter` cho text tiếng Việt chuẩn UTF-8, `JetBrains Mono` cho mã định danh.
3. **Chuẩn hóa trải nghiệm người dùng vi mô (Micro-UX)**:
   - Bắt buộc mọi View/Screen đều có đủ 5 trạng thái tương tác bọc trong component `<Async>`.
4. **Phân quyền giao diện theo ngữ cảnh (3D Scoped RBAC UI)**:
   - Kiểm soát trường thông tin và nút bấm theo 10 PlatformRoles và 4 ScopeTypes.
5. **Nghiệm thu trực quan thực tế (Visual QA)**:
   - Tự động dùng Playwright chụp ảnh màn hình ở 2 độ phân giải Desktop (1440×900) và Mobile (390×844).

---

## 2. Quy Trình Thiết Kế UI/UX 5 Bước Chi Tiết

### Bước 1: Khảo Sát Wireframe Từ Basic Design
Tra cứu chính xác file HTML mockup tương ứng với Task đang thực hiện trong `Specification/02_BASIC_DESIGN/`:
- `TASK-01`: Đọc `TASK-01_TONG_QUAN_VA_KIEN_TRUC_HOME/wireframe_home.html` (Landing, Sitemap, Menu, Chatbot AI).
- `TASK-02`: Đọc `TASK-02_HO_SO_DOANH_NGHIEP_DMST/form_dn_dmst.html` (Form 10 nhóm trường 225 fields, MST).
- `TASK-03`: Đọc `TASK-03_HO_SO_TIM_MUA_BUYER/survey_buyer.html` (Khảo sát nhu cầu công nghệ DNNVV, Triển lãm Cung VHLĐ).
- `TASK-04`: Đọc `TASK-04_HO_SO_CHAO_BAN_SELLER_VA_BO_LOC/bo_loc_cban_view.html` (Bộ lọc 1,479 rules cho 18 ngành, widget 3 điều kiện, TRL 1-9).
- `TASK-05`: Đọc `TASK-05_HO_SO_CHUYEN_GIA_KHCN/cv_scanner_flow.html` (LLKH chuẩn Bộ KH&CN, luồng AI OCR bóc tách file CV).
- `TASK-06`: Đọc `TASK-06_HE_THONG_DANH_MUC_NGANH_MA_TRAN/matrix_lv_cn.html` (Ma trận 109 cặp quan hệ LV-CN).
- `TASK-07`: Đọc `TASK-07_PHAN_QUYEN_QUAN_TRI_ADMIN/admin_approval.html` (Bảng điều khiển 5 quyền hạt nhân Admin).

### Bước 2: Bố Cục Giao Diện (Layout Specification)
- **Desktop (>= 1280px)**:
  - Header: Logo Nacentwin, Menu điều hướng, thanh tìm kiếm thông minh, Avatar và Scope Badge (ví dụ: *[Sở KH&CN Hà Nội]*).
  - Main Layout: Thường chia 2 cột: Cột trái (25-30%) là Bộ lọc đa tầng hoặc Menu quản trị; Cột phải (70-75%) là Bảng dữ liệu / Form nhập liệu.
- **Mobile (< 768px)**:
  - Tự động co về 1 cột dọc (Single column responsive).
  - Bộ lọc nâng cao được đưa vào Bottom Sheet / Drawer trượt từ dưới lên.
  - Các nút hành động chính (Duyệt, Lưu, Nộp hồ sơ) dính cố định ở đáy màn hình (Sticky Bottom Bar).

### Bước 3: Ánh Xạ UI Components Chuẩn Hóa
Không viết style ad-hoc, bắt buộc dùng các components dùng chung trong `frontend/src/components/`:
- `<FormField>`: Tự động render Label, cờ bắt buộc `*`, tooltip giải thích, thông báo lỗi inline đỏ khi vi phạm rule.
- `<LoadingButton>`: Chống click đúp, tự động xoay Spinner và disabled khi đang gọi API.
- `<TRLBadge value={1..9}>`: Component hiển thị huy hiệu thang đo mức độ sẵn sàng công nghệ với màu sắc trực quan (TRL 1-3 Đỏ, 4-6 Vàng, 7-9 Xanh lá).
- `<SectorTag>`: Hiển thị 18 ngành TT17 kèm icon chuyên ngành.
- `<AIUploadDropzone>`: Khu vực kéo thả file CV/LLKH hỗ trợ xem trước và tiến trình scan AI.
- `<Toast>`: Thông báo nổi góc trên/dưới xác nhận lưu thành công hoặc cảnh báo.

### Bước 4: Chuẩn Hóa 5 Trạng Thái UX Bắt Buộc (`<Async>`)
Mọi màn hình gọi dữ liệu từ API Backend bắt buộc phải bọc trong component cấu trúc:
```tsx
<Async status={queryStatus}>
  <Async.Loading>
    <TableSkeleton rows={5} />
  </Async.Loading>
  <Async.Empty 
    message="Không tìm thấy công nghệ nào phù hợp với bộ lọc." 
    actionLabel="Đặt lại bộ lọc" 
    onAction={resetFilter} 
  />
  <Async.Error 
    message={error.message} 
    onRetry={refetch} 
  />
  <Async.Success>
    {(data) => <TechnologyList items={data.items} />}
  </Async.Success>
  <Async.Partial>
    {(data) => <TechnologyList items={data.items} isLoadingMore={true} />}
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
   - So sánh ảnh chụp thực tế với wireframe HTML nguồn trong Basic Design để đảm bảo độ chuẩn xác 100%.

### Bước 6: Tổng hợp Wireframe Nguồn Bắt Buộc (Wireframe Source Library)

Sau khi **tạo mới hoặc cập nhật** bất kỳ file HTML wireframe nào trong `Specification/02_BASIC_DESIGN/TASK-XX/`, Agent bắt buộc phải cập nhật thư viện tổng hợp:

- **File tổng hợp chuẩn**: `Specification/02_BASIC_DESIGN/wireframe_tong_the_nacentwin.html`.
- Thêm một tab/mục mới với: mã TASK, tên màn hình, mô tả ngắn, đường dẫn tương đối đến file HTML nguồn và icon Lucide phù hợp.
- File tổng hợp phải hiển thị **trực tiếp wireframe HTML nguồn qua iframe**. Không được tự vẽ lại hoặc thay thế giao diện nguồn bằng mockup mới trong file tổng hợp.
- Nếu TASK đã có đặc tả nhưng **chưa có file HTML wireframe nguồn**, phải hiển thị trạng thái `Chưa có wireframe HTML nguồn`, kèm đường dẫn thư mục TASK. Tuyệt đối không suy diễn để dựng màn hình thay thế.
- Lớp bao của thư viện tổng hợp được chuẩn hóa theo Design System NacenTwin (logo, màu Navy/Cyan/Emerald, font Plus Jakarta Sans, icon Lucide, tab điều hướng, preview Desktop/Mobile); nội dung bên trong iframe phải giữ nguyên để phục vụ đối chiếu thiết kế.
- Trước khi bàn giao, xác minh mọi đường dẫn được đăng ký trong thư viện tổng hợp đều tồn tại và tab mở đúng wireframe tương ứng.

Mục đích là duy trì một **nguồn xem tổng thể duy nhất** của tất cả wireframe thực tế, làm đầu vào trực tiếp cho đội UI Design/Frontend mà không làm mất dấu vết nguồn.

---

## 3. Tiêu Chí Nghiệm Thu UI/UX (Definition of Done)
- [ ] Khớp 100% các trường dữ liệu và luồng tương tác từ file HTML Wireframe Basic Design.
- [ ] Tuân thủ bảng màu công nghệ NacenTech và hoạt động mượt mà ở cả Light/Dark Mode.
- [ ] 100% các màn hình có đủ 5 trạng thái UX xử lý qua `<Async>`.
- [ ] Giao diện tự động thích ứng hoàn hảo giữa Desktop (1440px) và Mobile (390px).
- [ ] Đã chạy Playwright chụp ảnh Visual QA đầy đủ và lưu vào thư mục screenshots.
- [ ] Mọi wireframe HTML mới/cập nhật đã được đăng ký và mở đúng trong `Specification/02_BASIC_DESIGN/wireframe_tong_the_nacentwin.html`.
- [ ] Các TASK chưa có HTML nguồn được đánh dấu rõ trong thư viện tổng hợp, không có mockup suy diễn thay thế.
