# QUY TRÌNH GIAO DIỆN & TRẢI NGHIỆM NGƯỜI DÙNG: wf-uiux (5 TRẠNG THÁI UX & VISUAL QA)

> **Mã Quy Trình**: `wf-uiux`  
> **Tác Tử Chủ Trì**: **Dev Agent (`dev`)** — Frontend Implementation  
> **Tác Tử Phối Hợp**: **EC Agent (`ec`)** — Visual QA & Screenshots  
> **Cổng Kết Thúc**: Visual QA Pass & Screenshot Verification

---

## 1. MỤC TIÊU CỐT LÕI
1. Đảm bảo 100% màn hình tương tác người dùng tuân thủ nguyên lý **5 Trạng Thái UX**:
   - `Loading`: Skeleton loader khớp bố cục.
   - `Empty`: Minh họa thân thiện kèm Call-to-Action.
   - `Error`: Xử lý ngoại lệ lịch sự kèm nút Thử lại (Retry).
   - `Success`: Hiển thị dữ liệu chuẩn chỉnh.
   - `Updating`: Khóa nút bấm, hiển thị chỉ báo lưu nền chống double click.
2. Tự động chụp ảnh màn hình bằng Playwright ở các độ phân giải (Desktop, Tablet, Mobile) làm bằng chứng nghiệm thu cho PO và khách hàng.

---

## 2. BẢNG ĐIỀU HƯỚNG TỆP TIN ĐẦU RA (ENFORCED DIRECTORY CONTRACT)
- Mã nguồn UI: `src/WebApp/`
- Kịch bản test giao diện: `tests/e2e/[epic-id]-ui.spec.ts`
- Thư mục ảnh chụp màn hình kiểm chứng: `tests/e2e/screenshots/[epic-id]/`

---

## 3. CÁC BƯỚC THỰC THI

### Bước 1: Dựng Khung Giao Diện & Component <Async> [Dev Agent]
- **Kỹ năng sử dụng**: `dev-uiux`
- **Hành động**: Dựng các component React/Next.js/Vue bọc qua `<Async>`. Tích hợp trạng thái rỗng, tải, lỗi và cập nhật.

### Bước 2: Kết Nối API & Quản Lý State [Dev Agent]
- **Kỹ năng sử dụng**: `dev-code`
- **Hành động**: Kết nối API REST/GraphQL, xử lý Optimistic Update và phân trang.

### Bước 3: Soạn Kịch Bản Chụp Ảnh Visual QA [EC Agent]
- **Kỹ năng sử dụng**: `ec-e2e`
- **Hành động**: Viết kịch bản Playwright giả lập lần lượt 5 trạng thái UX (giả lập mạng chậm để chụp loading, mock API trả về rỗng để chụp empty, mock lỗi 500 để chụp error...).

### Bước 4: Chạy Kịch Bản & Xuất Ảnh Kiểm Chứng [EC Agent]
- **Kỹ năng sử dụng**: `ec-test`
- Chạy lệnh test headless browser:
  ```bash
  npx playwright test tests/e2e/[epic-id]-ui.spec.ts
  ```
- Toàn bộ ảnh chụp 5 trạng thái UX được lưu tại `tests/e2e/screenshots/[epic-id]/`.

### Bước 5: PO Nghiệm Thu Trực Quan Gate 4/5 [PO/PM Agent]
- **Kỹ năng sử dụng**: `po-gate`
- PO xem qua các ảnh chụp màn hình trong thư mục screenshots và xác nhận đạt chuẩn giao diện trước khi xuất xưởng.
