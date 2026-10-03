---
name: "speckit-roadmap"
description: "Master Roadmap & Epic Registry Manager: Tra cứu tiến độ tổng thể các Epic, đối soát tự động tiến độ từ tasks.md và cập nhật specs/ROADMAP.md cho ManageAgent."
compatibility: "Requires spec-kit project structure with specs/ and specs/ROADMAP.md"
metadata:
  author: "github-spec-kit"
  source: "custom/speckit-roadmap"
---

# Kỹ Năng Quản Lý Master Roadmap (`speckit-roadmap`)

## 1. Mục Đích & Vai Trò
Skill này đóng vai trò là "Nhạc trưởng điều phối & Giám sát tiến độ dự án" (Master Project Controller):
- **Single Source of Truth**: Duy trì tài liệu trung tâm `specs/ROADMAP.md`.
- **Audit & Sync tự động**: Quét toàn bộ thư mục `specs/###-*` để đọc trạng thái `tasks.md` và đồng bộ tỷ lệ hoàn thành, số lượng tasks thực tế vào Roadmap.
- **Thêm/Sửa Epic**: Ghi nhận Epic mới phát sinh hoặc chia tách từ Epic cũ kèm lý do vào Lịch sử thay đổi (Changelog / Decision Log).

---

## 2. Các Lệnh Điều Khiển

Người dùng hoặc Agent có thể gọi skill với các tham số:
1. `/speckit-roadmap` hoặc `/speckit-roadmap view`:
   - Hiển thị bảng tóm tắt tiến độ hiện tại của tất cả các Epic, trạng thái triển khai, và các Epic tiếp theo cần thực thi.
2. `/speckit-roadmap sync`:
   - Tự động duyệt qua tất cả các thư mục con trong `specs/` (ví dụ: `001-auth-dang-nhap`, `006-kb-ingestion-document`, `008-kb-rut-chu-va-han-muc`...).
   - Đếm số lượng task hoàn thành `[x]` trên tổng số task `[ ]` trong `tasks.md`.
   - Cập nhật tỷ lệ % và trạng thái tương ứng vào `specs/ROADMAP.md`.
3. `/speckit-roadmap add <Mã> <Tên Epic> <Lý do>`:
   - Đăng ký Epic mới vào bảng Master Roadmap.
   - Tạo thư mục `specs/<Mã>-<Tên>/` với cấu trúc chuẩn Spec Kit nếu chưa tồn tại.
   - Ghi lý do vào Decision Log trong `specs/ROADMAP.md`.

---

## 3. Quy Trình Thực Thi Chi Tiết

### Chế độ SYNC (Audit & Đồng bộ tự động)
Khi được kích hoạt chế độ `sync`:
1. **Quét danh mục thư mục**:
   - Liệt kê toàn bộ thư mục khớp pattern `specs/[0-9]*`.
2. **Đọc và Phân tích `tasks.md`**:
   - Đối với mỗi thư mục, kiểm tra file `tasks.md`:
     - Đếm tổng số `[ ]` và `[x]`.
     - Nếu không có file `tasks.md` hoặc 0 tasks: Trạng thái là `📝 Đang chuẩn bị` hoặc `📋 Đã có Spec`.
     - Nếu `[x] > 0` và `[x] < tổng`: Trạng thái là `🔵 Đang thi công (x/y tasks)`.
     - Nếu `[x] == tổng` và `tổng > 0`: Trạng thái là `✅ 100% Hoàn thành (x/x tasks)`.
3. **Cập nhật `specs/ROADMAP.md`**:
   - Dùng tool chỉnh sửa chính xác các dòng trong Bảng 1 của file `specs/ROADMAP.md`.
4. **Báo cáo kết quả**:
   - Xuất bảng tóm tắt trực quan ra màn hình chat cho người dùng xem.

---

## 4. Bắt Buộc Tuân Thủ
- **Không tự ý xóa Epic**: Không được xóa bất kỳ Epic nào khỏi Roadmap mà không có yêu cầu rõ ràng từ người dùng.
- **Ghi chép Decision Log**: Bất kỳ khi nào thêm Epic mới hoặc thay đổi trạng thái lớn, bắt buộc phải cập nhật bảng Lịch sử thay đổi (Changelog) ở cuối file `specs/ROADMAP.md`.
