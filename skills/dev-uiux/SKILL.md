---
name: dev-uiux
description: "Chuẩn hóa giao diện người dùng hiển thị đầy đủ 5 trạng thái UX (Loading, Empty, Error, Success, Updating) qua component chuẩn <Async> và layout đáp ứng (Responsive UI)."
---

# Kỹ Năng: dev-uiux (Chuẩn Hóa Giao Diện 5 Trạng Thái UX)

> **Role Chịu Trách Nhiệm**: Dev Agent (`dev`) — Senior Full-Stack Developer.  
> **Cổng Kiểm Soát**: Frontend UX Quality Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Thiết kế layout Wireframe và yêu cầu UI trong `specs/[epic-id]/spec.md`.
- **Target Output Directory**: `src/WebApp/` (Components, Pages, Styles).
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. CHUẨN MỰC 5 TRẠNG THÁI UX BẮT BUỘC

Mọi màn hình hoặc khối giao diện có gọi API bất đồng bộ bắt buộc phải bọc qua component chuẩn `<Async>` hoặc cấu trúc tương đương hỗ trợ đủ 5 trạng thái:

1. **`Loading` (Đang Tải Dữ Liệu)**:
   - Hiển thị Skeleton Loading khớp với bố cục nội dung thực tế (không dùng vòng quay Spinner đơn điệu làm giật layout).
2. **`Empty` (Chưa Có Dữ Liệu)**:
   - Hiển thị hình minh họa trạng thái rỗng thân thiện kèm thông điệp rõ ràng và nút kêu gọi hành động (Call-to-Action: ví dụ *"Thêm sản phẩm đầu tiên"*).
3. **`Error` (Lỗi / Mất Kết Nối)**:
   - Xử lý ngoại lệ lịch sự, giải thích dễ hiểu (không hiển thị lỗi kỹ thuật 500 thô), kèm nút "Thử lại" (Retry).
4. **`Success` (Thành Công / Đầy Đủ Dữ Liệu)**:
   - Hiển thị dữ liệu chuẩn chỉnh, hỗ trợ phân trang mượt mà hoặc cuộn vô tận.
5. **`Updating / Submitting` (Đang Cập Nhật Nền)**:
   - Khi người dùng bấm lưu/cập nhật, khóa nút bấm, hiển thị chỉ báo đang ghi nền (Optimistic UI hoặc Button Spinner) để ngăn chặn người dùng bấm nhiều lần (Double-click / Duplicate submission).

---

## 3. MẪU COMPONENT <ASYNC> CHUẨN

```tsx
<Async
  status={query.status} // 'loading' | 'empty' | 'error' | 'success'
  isFetching={query.isFetching} // Updating state
  loadingFallback={<UserListSkeleton />}
  emptyFallback={<EmptyState title="Chưa có người dùng" action={<Button>Tạo mới</Button>} />}
  errorFallback={(error) => <ErrorState message={error.message} onRetry={query.refetch} />}
>
  {(data) => <UserListView items={data} />}
</Async>
```
