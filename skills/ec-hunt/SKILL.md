---
name: ec-hunt
description: "Săn tìm kịch bản lỗi biên, góc khuất và ngoại lệ logic (BMad Edge-Case Hunter): spam click, ngắt mạng bất ngờ, payload dị thường, dữ liệu rỗng hoặc cực đại."
---

# Kỹ Năng: ec-hunt (Săn Tìm Lỗi Biên & Ngoại Lệ Góc Khuất)

> **Role Chịu Trách Nhiệm**: EC Agent (`ec`) — Edge-Case Hunter & QC Specialist.  
> **Cổng Kiểm Soát**: Gate 4 Edge-Case Verification.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Đặc tả `specs/[epic-id]/spec.md` và mã nguồn triển khai trong `src/`.
- **Target Output File**: `tests/edge-cases/DEFECT_LOG.md`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. 6 CHIẾN LƯỢC SĂN LỖI BIÊN (EDGE-CASE HUNTING PATTERNS)

EC Agent tiếp cận hệ thống với tâm thế của một người dùng cố tình phá hoại hoặc người dùng thiếu kinh nghiệm thao tác sai:

1. **Thao Tác Dồn Dập & Spam Click (Rapid Double Actions)**:
   - Bấm nút gửi đơn hàng / chuyển tiền 5 lần liên tiếp trong 100ms.
   - Hệ thống có bị trừ tiền 2 lần không? Có tạo ra 2 đơn hàng trùng lặp không?
2. **Giá Trị Cực Hạn (Boundary & Extreme Values)**:
   - Thử số 0, số âm, số thực có 10 chữ số thập phân, chuỗi ký tự dài 10,000 ký tự.
   - Thử các ký tự đặc biệt Unicode, Emoji, SQL Injection payload, XSS script.
3. **Gián Đoạn Mạng & Trạng Thái Dở Dang (Network Latency & Offline)**:
   - Ngắt mạng giữa chừng khi request đang gửi.
   - Timeout từ dịch vụ bên thứ ba (Cổng thanh toán, SMS OTP).
   - Hệ thống có rollback giao dịch an toàn không? Có hiển thị thông báo lỗi thân thiện kèm nút Retry không?
4. **Xung Đột Đồng Thời (Concurrent Race Conditions)**:
   - Hai người dùng cùng lúc bấm mua món hàng cuối cùng trong kho (Inventory = 1).
   - Hệ thống có bảo vệ tính toàn vẹn và chỉ cho phép 1 người mua thành công không?
5. **Session & Token Hết Hạn Đột Ngột**:
   - Token JWT hết hạn ngay giữa quá trình điền form gồm 5 bước.
   - Dữ liệu người dùng đã nhập có bị mất trắng không?
6. **Lỗi Rỗng & Dữ Liệu Thiếu (Null/Empty Payloads)**:
   - Gửi payload JSON rỗng `{}`, hoặc mảng rỗng `[]`, hoặc thiếu các trường tùy chọn.

---

## 3. CẤU TRÚC BÁO CÁO LỖI (DEFECT REPORT FORMAT)
Mọi lỗi phát hiện bắt buộc phải ghi vào `tests/edge-cases/DEFECT_LOG.md` với đầy đủ 4 yếu tố:
1. *Mức độ nghiêm trọng*: `[BLOCKER]`, `[CRITICAL]`, `[MAJOR]`, `[MINOR]`.
2. *Điều kiện tiên quyết (Preconditions)*.
3. *Các bước tái hiện (Steps to Reproduce)*.
4. *Kết quả thực tế vs Kết quả kỳ vọng kèm Log/Screenshot*.
