---
name: wf-uiux
description: "Quy trình thiết kế & thi công giao diện toàn trình (Design Intelligence, 5 Trạng Thái UX, Playwright Visual QA & Quality Gate 4)."
---

# QUY TRÌNH GIAO DIỆN & TRẢI NGHIỆM NGƯỜI DÙNG: wf-uiux (DESIGN INTELLIGENCE, 5 TRẠNG THÁI UX & VISUAL QA v2.0.0)

> **Mã Quy Trình**: `wf-uiux`  
> **Tác Tử Chủ Trì**: **Dev Agent (`dev`)** — Frontend Implementation  
> **Tác Tử Phối Hợp**: **SA Agent (`sa`)** (Design System), **EC Agent (`ec`)** (Visual QA & A11y), **PO Agent (`po`)** (Gate Sign-off)  
> **Cổng Kết Thúc**: Quality Gate 4 (Frontend Pass & Screenshot Verification)

---

## 1. MỤC TIÊU CỐT LÕI
1. **Thiết lập Single Source of Truth**: Khởi tạo và lưu vết Design System chuẩn ngành tại `design-system/<project>/MASTER.md` thông qua bộ máy suy luận `ui-ux-pro-max`.
2. **Quy chuẩn lập trình theo Framework**: Tra cứu thực hành chuẩn Do/Don't cho 22 Tech Stacks, loại bỏ hoàn toàn mã màu hex ad-hoc.
3. **Đảm bảo 100% màn hình tuân thủ nguyên lý 5 Trạng Thái UX**:
   - `Loading`: Skeleton loader khớp cấu trúc dữ liệu.
   - `Empty`: Minh họa thân thiện kèm Call-to-Action.
   - `Error`: Xử lý ngoại lệ lịch sự kèm nút Thử lại (Retry).
   - `Success`: Hiển thị dữ liệu chuẩn chỉnh, hỗ trợ phân trang mượt mà.
   - `Updating`: Khóa nút bấm, hiển thị chỉ báo lưu nền chống double click.
4. **Mô hình hóa gián đoạn tương tác**: Xử lý `AbortController` khi hủy tác vụ, chống rò rỉ bộ nhớ và cảnh báo mất dữ liệu khi rời trang.
5. **Tự động chụp ảnh màn hình bằng Playwright**: Chụp ở 2 độ phân giải Desktop (1440×900) và Mobile (390×844) làm bằng chứng kiểm chứng độc lập cho PO và khách hàng.
6. **Vượt qua 100% Pre-Delivery Checklist**: Không emoji làm icon, contrast văn bản >= 4.5:1, touch target >= 44px, focus phím rõ ràng.

---

## 2. BẢNG ĐIỀU HƯỚNG TỆP TIN ĐẦU RA (ENFORCED DIRECTORY CONTRACT)
- Hệ thống thiết kế chuẩn: `design-system/<project>/MASTER.md` và `pages/<page>.md`
- Mã nguồn UI: `src/WebApp/` hoặc `SourceCode/frontend/src/`
- Kịch bản test giao diện: `tests/e2e/[epic-id]-ui.spec.ts`
- Thư mục ảnh chụp màn hình kiểm chứng: `tests/e2e/screenshots/[epic-id]/`

---

## 3. CÁC BƯỚC THỰC THI 6 GIAI ĐOẠN

### Bước 1: Khởi Tạo & Lưu Vết Hệ Thống Thiết Kế [SA / Product Designer]
- **Kỹ năng sử dụng**: `ui-ux-pro-max`, `sa-design`
- **Hành động**:
  - Chạy lệnh sinh Design System theo ngành và loại sản phẩm:
    ```bash
    python3 skills/ui-ux-pro-max/scripts/search.py "<product_type/industry>" --design-system --persist -p "<ProjectName>" --output-dir "."
    ```
  - Kiểm tra tệp sinh ra tại `design-system/<project>/MASTER.md`.
  - Cấu hình CSS Variables hoặc Tailwind Tokens vào dự án dựa trên các thông số đã sinh.

### Bước 2: Dựng Khung Giao Diện & Áp Dụng Tokens [Dev Agent]
- **Kỹ năng sử dụng**: `dev-uiux`, `speckit-uiux`
- **Hành động**:
  - Đọc `MASTER.md` để lấy đúng mã biến màu (CSS Variables), cỡ chữ, font chữ Google Fonts.
  - Tra cứu hướng dẫn framework nếu cần:
    ```bash
    python3 skills/ui-ux-pro-max/scripts/search.py "layout" --stack <framework>
    ```
  - Dựng khung component theo đúng cấu trúc Wireframe từ Basic Design.

### Bước 3: Chuẩn Hóa 5 Trạng Thái UX & Xử Lý Gián Đoạn [Dev Agent]
- **Kỹ năng sử dụng**: `dev-code`, `dev-uiux`
- **Hành động**:
  - Bọc khối giao diện bằng `<Async>` với đủ 5 trạng thái (Loading Skeleton, Empty State CTA, Error Retry, Success, Updating chống double-click).
  - Tích hợp `AbortController` để hủy request khi người dùng đóng modal hoặc chuyển trang.
  - Tự rà soát Pre-Delivery Checklist (Không dùng emoji làm icon, kiểm tra `cursor-pointer`, focus ring).

### Bước 4: Soạn Kịch Bản Chụp Ảnh Visual QA [EC Agent]
- **Kỹ năng sử dụng**: `ec-e2e`
- **Hành động**:
  - Viết kịch bản Playwright giả lập lần lượt 5 trạng thái UX:
    - Giả lập mạng chậm (`page.route` throttle) để chụp `Loading`.
    - Mock API trả mảng rỗng `[]` để chụp `Empty`.
    - Mock API trả lỗi HTTP 500 để chụp `Error`.
    - Nạp dữ liệu chuẩn để chụp `Success`.
    - Bấm nút submit và chụp chỉ báo `Updating`.

### Bước 5: Chạy Kịch Bản & Xuất Ảnh Kiểm Chứng [EC Agent]
- **Kỹ năng sử dụng**: `ec-test`
- **Hành động**:
  - Chạy lệnh test headless browser:
    ```bash
    npx playwright test tests/e2e/[epic-id]-ui.spec.ts
    ```
  - Toàn bộ ảnh chụp Desktop (1440×900) và Mobile (390×844) được lưu tại `tests/e2e/screenshots/[epic-id]/`.
  - Kiểm tra độ tương phản màu sắc và tính truy cập (A11y).

### Bước 6: PO Nghiệm Thu Trực Quan Gate 4 [PO/PM Agent]
- **Kỹ năng sử dụng**: `po-gate`
- **Hành động**:
  - PO mở thư mục ảnh `tests/e2e/screenshots/[epic-id]/`, đối chiếu ảnh chụp thực tế với:
    1. Wireframe nguồn trong Basic Design.
    2. Bảng màu và quy chuẩn trong `design-system/<project>/MASTER.md`.
    3. Đủ 5 trạng thái UX và responsive trên Mobile.
  - Ký biên bản Quality Gate 4 cho phép tích hợp và đóng Epic.
