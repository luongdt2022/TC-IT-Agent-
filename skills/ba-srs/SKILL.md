---
name: ba-srs
description: "Biên soạn tài liệu Đặc tả Yêu cầu Phần mềm (SRS) chuẩn 7 mục khép kín: Tổng quan, Tác nhân & Quyền, Yêu cầu Chức năng (REQ-*), Quy tắc Nghiệp vụ (BR-*), Yêu cầu Dữ liệu & UI, Yêu cầu Phi chức năng, và Ma trận Truy vết."
---

# Kỹ Năng: ba-srs (Đặc Tả Phần Mềm SRS Chuẩn 7 Mục)

> **Role Chịu Trách Nhiệm**: BA Agent (`ba`) — Senior Business Analyst.  
> **Cổng Kiểm Soát**: Gate 1 Detailed Specification Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Thiết kế cơ sở tại `docs/01-basic-design/` và phạm vi Epic từ `backlog/ROADMAP.md`.
- **Target Output File**: `specs/[epic-id]/spec.md` (Ví dụ: `specs/EPIC-01-AUTH/spec.md`).
- **NGHIÊM CẤM**: Không tạo các file đặc tả lẻ tẻ ngoài thư mục `specs/[epic-id]/`.

---

## 2. CẤU TRÚC BẮT BUỘC CỦA TÀI LIỆU SRS 7 MỤC

Mọi tài liệu `specs/[epic-id]/spec.md` bắt buộc phải có đầy đủ 7 mục theo cấu trúc chuẩn sau:

### Mục 1: Thông Tin Chung & Bối Cảnh Nghiệp Vụ
- Mã Epic, Tên phân hệ, Mục tiêu kinh doanh, Mức độ ưu tiên (P1/P2/P3).
- Định nghĩa thuật ngữ & Từ viết tắt.

### Mục 2: Ma Trận Phân Quyền & Tác Nhân (Actor & RBAC)
- Danh sách Actor (Admin, Manager, User, Guest...).
- Ma trận quyền hạn CRUD trên từng thực thể: Create, Read, Update, Delete, Export, Approve.

### Mục 3: Yêu Cầu Chức Năng Chi Tiết (Functional Requirements)
- Bắt buộc mã hóa dạng: `REQ-[EPIC]-[STT]` (Ví dụ: `REQ-AUTH-001`, `REQ-CART-002`).
- Mô tả User Story: *Là một [Actor], tôi muốn [Hành động] để [Lợi ích]* kèm Preconditions và Postconditions.

### Mục 4: Quy Tắc Nghiệp Vụ Chặt Chẽ (Business Rules)
- Bắt buộc mã hóa dạng: `BR-[EPIC]-[STT]` (Ví dụ: `BR-AUTH-001`, `BR-PAY-003`).
- Quy định chi tiết các điều kiện biên, logic kiểm tra tính hợp lệ, công thức tính toán, trạng thái luồng.

### Mục 5: Yêu Cầu Dữ Liệu & Giao Diện (Data & UI/UX States)
- Từ điển dữ liệu sơ bộ: Tên trường, Kiểu dữ liệu, Bắt buộc/Tùy chọn, Ràng buộc min/max.
- Yêu cầu 5 trạng thái UX: Loading (Skeleton), Empty, Error (Retry), Success, Updating.

### Mục 6: Yêu Cầu Phi Chức Năng (Non-Functional Requirements)
- Thời gian phản hồi API (p95 < 200ms), bảo mật thông tin (Mã hóa mật khẩu Bcrypt/Argon2, Mask dữ liệu PII).

### Mục 7: Tiêu Chí Nghiệm Thu Khép Kín (Acceptance Criteria - AC)
- Bắt buộc mã hóa dạng: `AC-[EPIC]-[STT]`.
- Viết theo chuẩn Gherkin: *Given (Cho)... When (Khi)... Then (Thì)...*.
- Phải ánh xạ 1:1 sang `REQ-*` và `BR-*`.

---

## 3. CỔNG DUYỆT 1 CHIỀU (GATED SIGN-OFF)
- BA Agent chỉ bàn giao `spec.md` cho TL/SA Agent khi tài liệu có đủ 7 mục và không còn mục nào mang trạng thái nháp (`Draft`).
