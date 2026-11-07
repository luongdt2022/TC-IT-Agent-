---
name: "speckit-uiux"
description: "Senior Product Designer & Visual QA Specialist (v3.0.0): Tích hợp bộ máy UI/UX Pro Max sinh Design System chuẩn ngành, đối soát HTML Wireframe Basic Design, chuẩn hóa 5 trạng thái UX qua <Async>, mô hình hóa ma trận gián đoạn, phân quyền 3D Scoped RBAC UI và tự động chụp ảnh Visual QA bằng Playwright."
compatibility: "Requires Frontend Submodule (SourceCode/frontend/ or src/WebApp/) with Playwright"
metadata:
  author: "NacenTwin Architecture Team & UI/UX Pro Max Engine"
  source: "custom/speckit-uiux-nacentech"
  version: "3.0.0"
---

# Kỹ Năng Thiết Kế Giao Diện & Kiểm Thử Trực Quan Chuẩn Hóa (`speckit-uiux`)

## 1. Mục Đích & Vai Trò
Khi dự án bước vào giai đoạn thiết kế và thi công giao diện Frontend tại `SourceCode/frontend/` hoặc `src/WebApp/`, kỹ năng này đóng vai trò là **Senior Product Designer & Visual QA Specialist**, kết hợp sức mạnh giữa **Bộ máy suy luận thiết kế UI/UX Pro Max** và **Kỷ luật kiến trúc NacenTwin**:

1. **Khởi tạo & Quản trị Hệ thống Thiết kế (Design System Governance)**:
   - Tự động sinh `design-system/<project>/MASTER.md` bằng bộ máy suy luận `ui-ux-pro-max` với bảng màu chuẩn vai trò UX, cặp typography Google Fonts, khoảng cách spacing scale và anti-patterns cần tránh.
   - Hỗ trợ mô hình Master + Overrides (`pages/<page>.md`) để chống trôi dạt nhận diện thương hiệu (Design Drift).
2. **Bảo toàn 100% nghiệp vụ từ Basic Design**:
   - Đối soát trực tiếp với các file HTML Wireframe mô phỏng tại `Specification/02_BASIC_DESIGN/TASK-XX/`.
   - Giữ trọn vẹn các cấu trúc nghiệp vụ đặc thù (Form 225 trường, Bộ lọc 1,479 quy tắc cho 18 ngành, Thang đo TRL 1-9, Cây đơn vị 63 Sở KH&CN Tỉnh...).
3. **Quy chuẩn Design Tokens & Theme Support**:
   - Tôn trọng Design System dự án: Dự án NacenTwin áp dụng bảng màu Tech Navy Blue (`#1e40af`), Vibrant Cyan (`#06b6d4`), Innovation Emerald (`#10b981`), Neutral Dark (`#0f172a`); các dự án khác áp dụng bảng màu chuyên biệt do `ui-ux-pro-max` sinh ra.
   - Hỗ trợ mượt mà **Light / Dark Mode** với độ tương phản văn bản đạt tối thiểu 4.5:1 (WCAG AA).
4. **Chuẩn hóa trải nghiệm người dùng vi mô (Micro-UX)**:
   - Bắt buộc mọi View/Screen đều có đủ 5 trạng thái tương tác bọc trong component `<Async>`.
   - Mô hình hóa Vòng đời 5 pha và Ma trận 7 kịch bản gián đoạn tương tác.
5. **Phân quyền giao diện theo ngữ cảnh (3D Scoped RBAC UI)**:
   - Kiểm soát trường thông tin và nút bấm theo 10 PlatformRoles và 4 ScopeTypes.
6. **Nghiệm thu trực quan thực tế (Visual QA)**:
   - Tự động dùng Playwright chụp ảnh màn hình ở 2 độ phân giải Desktop (1440×900) và Mobile (390×844) làm bằng chứng nghiệm thu Gate 4/5.

---

## 2. Quy Trình Thiết Kế UI/UX 7 Bước Chi Tiết

### Bước 0: Khởi Tạo & Quản Trị Hệ Thống Thiết Kế (Design System Reasoning & Token Governance)
Trước khi đi vào chi tiết màn hình, Agent bắt buộc phải kiểm tra và sinh Design System chuẩn ngành:

1. **Kiểm tra tệp Master hiện hữu**:
   - Kiểm tra xem `design-system/<project-slug>/MASTER.md` đã tồn tại chưa.
   - Nếu đã tồn tại: Đọc tệp này để lấy đúng bảng màu, typography, CSS variables. Không tự ý ghi đè làm mất quyết định cũ.
2. **Khởi tạo mới qua bộ máy UI/UX Pro Max** (nếu chưa có `MASTER.md`):
   ```bash
   python3 skills/ui-ux-pro-max/scripts/search.py "<loại_sản_phẩm_hoặc_ngành>" --design-system --persist -p "<TênDựÁn>" --output-dir "."
   ```
   *Ví dụ cho Fintech:*
   `python3 skills/ui-ux-pro-max/scripts/search.py "fintech banking" --design-system --persist -p "FintechApp" --output-dir "."`
3. **Ghi đè đặc thù cho trang (Page Overrides)**:
   - Nếu màn hình hiện tại có yêu cầu thị giác riêng (ví dụ màn hình `dashboard` cần visual density cao hơn landing page):
   ```bash
   python3 skills/ui-ux-pro-max/scripts/search.py "<yêu_cầu_màn_hình>" --design-system --persist -p "<TênDựÁn>" --output-dir "." --page "<page-slug>"
   ```

---

### Bước 1: Khảo Sát Wireframe Từ Basic Design
Tra cứu chính xác file HTML mockup tương ứng với Task đang thực hiện trong `Specification/02_BASIC_DESIGN/`:
- `TASK-01`: Đọc `TASK-01_TONG_QUAN_VA_KIEN_TRUC_HOME/wireframe_home.html` (Landing, Sitemap, Menu, Chatbot AI).
- `TASK-02`: Đọc `TASK-02_HO_SO_DOANH_NGHIEP_DMST/form_dn_dmst.html` (Form 10 nhóm trường 225 fields, MST).
- `TASK-03`: Đọc `TASK-03_HO_SO_TIM_MUA_BUYER/survey_buyer.html` (Khảo sát nhu cầu công nghệ DNNVV, Triển lãm Cung VHLĐ).
- `TASK-04`: Đọc `TASK-04_HO_SO_CHAO_BAN_SELLER_VA_BO_LOC/bo_loc_cban_view.html` (Bộ lọc 1,479 rules cho 18 ngành, widget 3 điều kiện, TRL 1-9).
- `TASK-05`: Đọc `TASK-05_HO_SO_CHUYEN_GIA_KHCN/cv_scanner_flow.html` (LLKH chuẩn Bộ KH&CN, luồng AI OCR bóc tách file CV).
- `TASK-06`: Đọc `TASK-06_HE_THONG_DANH_MUC_NGANH_MA_TRAN/matrix_lv_cn.html` (Ma trận 109 cặp quan hệ LV-CN).
- `TASK-07`: Đọc `TASK-07_PHAN_QUYEN_QUAN_TRI_ADMIN/admin_approval.html` (Bảng điều khiển 5 quyền hạt nhân Admin).

---

### Bước 2: Bố Cục Giao Diện & Tra Cứu Stack Guidelines
1. **Thiết kế Responsive 2 tầng**:
   - **Desktop (>= 1280px)**:
     - Header: Logo, Menu điều hướng, thanh tìm kiếm thông minh, Avatar và Scope Badge (ví dụ: *[Sở KH&CN Hà Nội]*).
     - Main Layout: Thường chia 2 cột: Cột trái (25-30%) là Bộ lọc đa tầng hoặc Menu quản trị; Cột phải (70-75%) là Bảng dữ liệu / Form nhập liệu.
   - **Mobile (< 768px)**:
     - Tự động co về 1 cột dọc (Single column responsive).
     - Bộ lọc nâng cao được đưa vào Bottom Sheet / Drawer trượt từ dưới lên.
     - Các nút hành động chính (Duyệt, Lưu, Nộp hồ sơ) dính cố định ở đáy màn hình (Sticky Bottom Bar), có chừa khoảng an toàn Safe-Area.
2. **Tra cứu quy chuẩn Framework từ `ui-ux-pro-max`**:
   - Khi triển khai layout phức tạp hoặc xử lý form, bắt buộc tra cứu hướng dẫn framework:
     ```bash
     python3 skills/ui-ux-pro-max/scripts/search.py "responsive layout" --stack <react|nextjs|vue|flutter|html-tailwind>
     python3 skills/ui-ux-pro-max/scripts/search.py "form validation" --stack <react|nextjs|vue|flutter>
     ```

---

### Bước 3: Ánh Xạ UI Components Chuẩn Hóa Theo Design Tokens
Không viết style ad-hoc, không hardcode mã màu hex. Bắt buộc dùng CSS Variable Tokens từ `MASTER.md` kết hợp components dùng chung:
- **Ánh xạ Tokens**: Dùng `var(--color-primary)`, `var(--color-background)`, `var(--color-card)`, v.v.
- `<FormField>`: Tự động render Label, cờ bắt buộc `*`, tooltip giải thích, thông báo lỗi inline đỏ khi vi phạm rule.
- `<LoadingButton>`: Chống click đúp, tự động xoay Spinner và disabled khi đang gọi API.
- `<TRLBadge value={1..9}>`: Component hiển thị huy hiệu thang đo mức độ sẵn sàng công nghệ với màu sắc trực quan (TRL 1-3 Đỏ, 4-6 Vàng, 7-9 Xanh lá).
- `<SectorTag>`: Hiển thị 18 ngành TT17 kèm icon chuyên ngành (icon SVG từ thư viện Lucide, không dùng Emoji).
- `<AIUploadDropzone>`: Khu vực kéo thả file CV/LLKH hỗ trợ xem trước và tiến trình scan AI.
- `<Toast>`: Thông báo nổi góc trên/dưới xác nhận lưu thành công hoặc cảnh báo.

---

### Bước 4: Chuẩn Hóa 5 Trạng Thái UX Bắt Buộc (`<Async>`) & Vòng Đời Tương Tác Gián Đoạn
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

#### Mô hình hóa 5 Pha Tương Tác & Ma Trận 7 Kịch Bản Gián Đoạn
Đối với các Form nhập liệu lớn, Modal thao tác, Wizard đa bước hoặc Thao tác hàng loạt (Bulk Actions):
1. **5 Pha Tương Tác**:
   - `Starting`: Bắt đầu kích hoạt (Click/Focus/Drag) -> Khởi tạo state, vô hiệu hóa submit đúp.
   - `Ending at once`: Người dùng kết thúc ngay (nhấp chuột nhanh, Esc) -> Reset state sạch sẽ.
   - `Extended`: Thao tác kéo dài (nhập dữ liệu form, kéo thả) -> Theo dõi dirty state (`isDirty = true`).
   - `While extended`: Đang trong tiến trình tương tác -> Live validation, auto-save nháp (nếu có).
   - `Finishing`: Xác nhận / Submit -> Kích hoạt AbortController, commit dữ liệu, dọn dẹp state.
2. **Bảng Ma Trận 7 Kịch Bản Gián Đoạn (Interrupt Matrix)**:
   - `[User Abort]`: Bấm Esc, nút "Hủy", click overlay -> Hủy gọi API qua `AbortController.abort()`, đóng modal, rollback form.
   - `[Mid-way Navigation]`: Chuyển trang khi đang điền dở -> Route Leave Guard cảnh báo mất dữ liệu.
   - `[Background Complete]`: Hành vi submit dở dang -> Khóa nút, tránh gửi trùng lặp (Idempotent request).
   - `[Environment Failure]`: Rớt mạng, timeout API -> Giữ nguyên dữ liệu đã nhập, thông báo lịch sự + nút Thử lại.
   - `[Page Reload / Tab Close]`: F5 hoặc tắt tab -> Sự kiện `beforeunload` cảnh báo form dirty.
   - `[External Mutation]`: Dữ liệu bị người khác sửa cùng lúc -> Báo lỗi `409 Conflict`, hỗ trợ nạp lại bản mới nhất.
   - `[Input Channel Change]`: Chuyển chuột/phím tắt, browser autofill -> Re-validate schema Zod toàn diện.

---

### Bước 5: Phân Quyền UI (3D Scoped RBAC UI) & Kiểm Thử Trực Quan Visual QA (Playwright)
1. **Phân quyền giao diện (Scoped RBAC)**:
   - Ẩn/hiện và disabled các trường form, nút duyệt, nút xóa theo ma trận phân quyền (PlatformRoles & ScopeTypes).
2. **Kịch bản chụp ảnh tự động bằng Playwright**:
   - Sử dụng Playwright headless mở trang ở 2 độ phân giải:
     + **Desktop**: 1440 × 900
     + **Mobile**: 390 × 844 (iPhone)
   - Lưu ảnh vào: `tests/visual-qa/screenshots/<task-id>/<screen-name>-desktop.png` và `-mobile.png`.
3. **Đối soát & Báo cáo**:
   - So sánh ảnh chụp thực tế với wireframe HTML nguồn trong Basic Design để đảm bảo độ chuẩn xác 100%.

---

### Bước 6: Tổng Hợp Wireframe Nguồn Bắt Buộc (Wireframe Source Library)
Sau khi **tạo mới hoặc cập nhật** bất kỳ file HTML wireframe nào trong `Specification/02_BASIC_DESIGN/TASK-XX/`:
- **File tổng hợp chuẩn**: `Specification/02_BASIC_DESIGN/wireframe_tong_the_nacentwin.html`.
- Thêm một tab/mục mới với: mã TASK, tên màn hình, mô tả ngắn, đường dẫn tương đối đến file HTML nguồn và icon Lucide phù hợp.
- File tổng hợp phải hiển thị **trực tiếp wireframe HTML nguồn qua iframe**. Không tự vẽ lại hoặc thay thế bằng mockup mới.
- Nếu TASK chưa có file HTML wireframe nguồn: Hiển thị trạng thái `Chưa có wireframe HTML nguồn`, kèm đường dẫn thư mục TASK. Tuyệt đối không suy diễn.

---

### Bước 7: Pre-Delivery Quality Gate (Đối Soát Chuẩn UI/UX Pro Max)
Trước khi ký bàn giao giao diện, Agent chạy rà soát lần cuối:
- [ ] **Không dùng Emoji**: 100% icon cấu trúc và trạng thái là vector SVG (Lucide/Heroicons).
- [ ] **Con trỏ & Focus**: `cursor-pointer` trên toàn bộ phần tử click được; focus-ring hiển thị rõ ràng khi bấm phím Tab.
- [ ] **Độ tương phản (WCAG AA)**: Văn bản chính đạt tỷ lệ tương phản >= 4.5:1 so với nền ở cả 2 theme Light và Dark.
- [ ] **Vùng chạm cảm ứng**: Mọi nút bấm trên Mobile đạt tối thiểu 44×44px (iOS/Web) hoặc 48×48dp (Android).
- [ ] **Tôn trọng Reduced Motion**: Các chuyển động CSS/GSAP được bọc trong `@media (prefers-reduced-motion: reduce)`.
- [ ] **Bố cục bền vững**: Văn bản dài và badge không bị tràn viền hay vỡ khung; tiêu đề áp dụng `text-wrap: balance` khi thích hợp.

---

## 3. Tiêu Chí Nghiệm Thu Hoàn Thành (Definition of Done)
- [ ] Tệp `design-system/<project>/MASTER.md` đã được sinh và ánh xạ tokens vào ứng dụng.
- [ ] Khớp 100% các trường dữ liệu và luồng tương tác từ file HTML Wireframe Basic Design.
- [ ] 100% các màn hình có đủ 5 trạng thái UX xử lý qua component `<Async>`.
- [ ] Đã mô hình hóa Ma trận gián đoạn và xử lý `AbortController`.
- [ ] Giao diện tự động thích ứng hoàn hảo giữa Desktop (1440px) và Mobile (390px).
- [ ] Đã chạy Playwright chụp ảnh Visual QA đầy đủ và lưu vào thư mục screenshots.
- [ ] Vượt qua 100% các hạng mục trong Pre-Delivery Quality Gate (Bước 7).
- [ ] Mọi wireframe HTML mới/cập nhật đã được đăng ký và mở đúng trong thư viện tổng hợp.
