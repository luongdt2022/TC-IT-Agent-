---
name: "dev-uiux"
description: "Thi công giao diện người dùng chuẩn hóa (v2.0.0): Áp dụng Design Tokens từ MASTER.md, tra cứu quy chuẩn 22 Framework từ UI/UX Pro Max, triển khai trọn vẹn 5 trạng thái UX qua component <Async>, và vượt qua Pre-Delivery Checklist (WCAG AA)."
---

# Kỹ Năng: dev-uiux (Thi Công Giao Diện Chuẩn Hóa Frontend v2.0.0)

> **Role Chịu Trách Nhiệm**: Dev Agent (`dev`) — Senior Full-Stack Developer.  
> **Cổng Kiểm Soát**: Frontend UX & Accessibility Quality Gate (Gate 4).

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**:
  - Thiết kế Wireframe & Yêu cầu UI trong `specs/[epic-id]/spec.md` hoặc Basic Design.
  - Hệ thống Design System chuẩn tại `design-system/<project>/MASTER.md` (hoặc `pages/<page>.md`).
- **Target Output Directory**: `src/WebApp/` hoặc `SourceCode/frontend/src/` (Components, Pages, Styles).
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`) và không hardcode mã màu hex tùy tiện trong code.

---

## 2. QUY CHUẨN DESIGN TOKENS (BẮT BUỘC)
Trước khi viết mã giao diện, Dev Agent bắt buộc đọc tệp `design-system/<project>/MASTER.md`:
1. **Ánh xạ biến màu chuẩn (CSS Variables)**:
   - Màu chủ đạo: `var(--color-primary)` và `var(--color-on-primary)`
   - Màu phụ: `var(--color-secondary)` và `var(--color-on-secondary)`
   - Màu hành động / CTA: `var(--color-accent)` và `var(--color-on-accent)`
   - Nền & Thẻ: `var(--color-background)`, `var(--color-card)`, `var(--color-muted)`
   - Viền & Trạng thái: `var(--color-border)`, `var(--color-destructive)`, `var(--color-ring)`
2. **Typography**:
   - Sử dụng đúng font chữ đã khai báo (qua `@import` Google Fonts trong `MASTER.md`).
   - Cỡ chữ body tối thiểu 16px (14px cho chú thích phụ), line-height tối thiểu 1.5.

---

## 3. TRA CỨU QUY CHUẨN FRAMEWORK (STACK GUIDELINES)
Dev Agent không được đoán mò cách tối ưu component. Khi gặp các trường hợp: Xử lý Form, Tối ưu Re-render, Responsive Layout, Quản lý State hoặc Animation, bắt buộc tra cứu hướng dẫn framework bằng công cụ cục bộ:

```bash
# Cú pháp:
python3 skills/ui-ux-pro-max/scripts/search.py "<vấn_đề>" --stack <tên_stack>

# Ví dụ thực tế:
python3 skills/ui-ux-pro-max/scripts/search.py "form validation" --stack react
python3 skills/ui-ux-pro-max/scripts/search.py "responsive layout" --stack html-tailwind
python3 skills/ui-ux-pro-max/scripts/search.py "re-render optimization" --stack nextjs
python3 skills/ui-ux-pro-max/scripts/search.py "touch safe-area" --stack flutter
```

Tuân thủ nghiêm ngặt các khuyến nghị `Do / Don't` và `Code Good / Code Bad` trả về từ kết quả tìm kiếm.

---

## 4. CHUẨN MỰC 5 TRẠNG THÁI UX BẮT BUỘC QUA COMPONENT <ASYNC>

Mọi màn hình hoặc khối giao diện có gọi API bất đồng bộ bắt buộc phải bọc qua component chuẩn `<Async>` hoặc cấu trúc tương đương hỗ trợ đủ 5 trạng thái:

1. **`Loading` (Đang Tải Dữ Liệu)**:
   - Hiển thị Skeleton Loading khớp chính xác với bố cục nội dung thực tế (không dùng vòng quay Spinner đơn điệu ở giữa trang làm giật layout - Layout Shift CLS).
2. **`Empty` (Chưa Có Dữ Liệu)**:
   - Hiển thị hình minh họa trạng thái rỗng thân thiện kèm thông điệp rõ ràng và nút kêu gọi hành động (Call-to-Action: ví dụ *"Thêm sản phẩm đầu tiên"*).
3. **`Error` (Lỗi / Mất Kết Nối)**:
   - Xử lý ngoại lệ lịch sự, giải thích dễ hiểu (không hiển thị lỗi kỹ thuật 500 thô), kèm nút "Thử lại" (Retry refetch).
4. **`Success` (Thành Công / Đầy Đủ Dữ Liệu)**:
   - Hiển thị dữ liệu chuẩn chỉnh, hỗ trợ phân trang mượt mà hoặc cuộn vô tận.
5. **`Updating / Submitting` (Đang Cập Nhật Nền)**:
   - Khi người dùng bấm lưu/cập nhật, khóa nút bấm (`disabled`), hiển thị chỉ báo đang ghi nền (Optimistic UI hoặc Button Spinner) để ngăn chặn hoàn toàn việc người dùng bấm nhiều lần (Double-click / Duplicate submission).

### Mẫu Component `<Async>` Chuẩn:
```tsx
<Async
  status={query.status} // 'loading' | 'empty' | 'error' | 'success'
  isFetching={query.isFetching} // Updating state
  loadingFallback={<UserListSkeleton />}
  emptyFallback={<EmptyState title="Chưa có dữ liệu" action={<Button>Tạo mới</Button>} />}
  errorFallback={(error) => <ErrorState message={error.message} onRetry={query.refetch} />}
>
  {(data) => <UserListView items={data} />}
</Async>
```

---

## 5. PRE-DELIVERY CHECKLIST TRƯỚC KHI BÀN GIAO (BẮT BUỘC PASS 100%)

Trước khi đánh dấu hoàn thành Task hoặc chuyển giao cho EC Agent kiểm thử, Dev Agent phải tự kiểm tra mã nguồn theo checklist sau:

- [ ] **Icon cấu trúc**: 100% sử dụng icon vector SVG (Lucide, Heroicons, Phosphor). **TUYỆT ĐỐI KHÔNG** dùng emoji (🎨, 🚀, ⚙️, ❌, ✅) làm icon điều hướng, nút bấm hay badge hệ thống.
- [ ] **Tương tác chuột**: Mọi phần tử có thể click (`button`, `a`, thẻ có sự kiện `onClick`) bắt buộc phải có thuộc tính `cursor-pointer`.
- [ ] **Chuyển tiếp (Transitions)**: Có hiệu ứng hover/focus mượt mà với thời gian chuyển tiếp hợp lý (150ms – 250ms), không đổi layout đột ngột gây giật màn hình.
- [ ] **Độ tương phản (WCAG AA)**: Văn bản chính đạt tỷ lệ tương phản tối thiểu 4.5:1 so với nền (chú thích phụ >= 3:1). Kiểm tra cẩn thận ở cả Light Mode và Dark Mode.
- [ ] **Điều hướng bàn phím**: Đường viền focus (Focus Ring / Outline) hiển thị rõ nét khi người dùng nhấn phím `Tab` duyệt trang.
- [ ] **Kích thước vùng chạm**: Trên thiết bị cảm ứng, mọi nút bấm hoặc liên kết phải có diện tích bấm tối thiểu 44×44px (iOS/Web) hoặc 48×48dp (Android).
- [ ] **Tôn trọng Reduced Motion**: Tôn trọng thiết lập giảm hoạt ảnh của người dùng qua `@media (prefers-reduced-motion: reduce)`.
- [ ] **Xử lý ngắt dòng & văn bản dài**: Tiêu đề áp dụng `text-wrap: balance` khi cần; nhãn chip, tag, URL dài tự động xuống dòng hoặc dàn lại, không bị cắt cụt hay làm tràn container ngang (`overflow-x: hidden`).
