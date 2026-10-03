---
name: ba-trace
description: "Chuyên gia Kiểm toán Truy vết Khép kín (Closed-Loop Traceability Auditor). Quét và kiểm tra tự động ma trận liên kết giữa REQ-, BR-, DB-, API-, UI- và Test Cases; phát hiện mã mồ côi (Orphan Code) và thiếu sót kiểm thử."
---

# Kỹ Năng: ba-trace (Kiểm Toán Ma Trận Truy Vết Khép Kín)

> **Role Chịu Trách Nhiệm**: BA Agent (`ba`) — Senior Business Analyst.  
> **Cổng Kiểm Soát**: Pre-Release Traceability Audit.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Toàn bộ các file `specs/[epic-id]/spec.md`, `specs/[epic-id]/plan.md`, `src/` và `tests/`.
- **Target Output File**: `docs/decisions/TRACEABILITY_MATRIX.md`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. NGUYÊN TẮC LIÊN KẾT KHÉP KÍN (CLOSED-LOOP TRACEABILITY)

Hệ thống yêu cầu sợi dây liên kết 6 mắt xích không được đứt đoạn:

$$\text{Yêu Cầu (REQ-)} \longleftrightarrow \text{Quy Tắc (BR-)} \longleftrightarrow \text{CSDL (DB-)} \longleftrightarrow \text{API (API-)} \longleftrightarrow \text{Mã Nguồn (src/)} \longleftrightarrow \text{Kiểm Thử (tests/)}$$

1. **Phát hiện Yêu Cầu Thiếu Code (Missing Implementation)**:
   - Một `REQ-*` hoặc `BR-*` có trong `spec.md` nhưng không tìm thấy hàm/endpoint xử lý trong `src/`.
2. **Phát hiện Mã Mồ Côi (Orphan Code)**:
   - Một method, entity hoặc API endpoint tồn tại trong `src/` nhưng không truy vết được về bất kỳ `REQ-*` nào.
3. **Phát hiện Kiểm Thử Chưa Bao Phủ (Missing Test Coverage)**:
   - Một `BR-*` quan trọng nhưng không có Unit Test tương ứng trong `tests/unit/`.

---

## 3. CẤU TRÚC MA TRẬN TRACEABILITY_MATRIX.MD

```markdown
# MA TRẬN TRUY VẾT KHÉP KÍN (TRACEABILITY MATRIX)

| Mã REQ | Mã BR | Tệp/Hàm Domain | Endpoint API (API-) | Bảng CSDL (DB-) | Mã Test Case | Trạng Thái Truy Vết |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| `REQ-AUTH-01` | `BR-AUTH-01` | `User.ValidatePassword()` | `POST /api/v1/auth/login` | `users` | `test_auth_br01` | [FULL TRACE PASS] |
| `REQ-AUTH-02` | `BR-AUTH-02` | `User.LockAccount()` | `POST /api/v1/auth/lock` | `users.status` | `test_auth_br02` | [FULL TRACE PASS] |

## BÁO CÁO PHÁT HIỆN LỖ HỔNG (GAP FINDINGS)
- Tổng số Yêu cầu REQ: [X]
- Tổng số Quy tắc BR: [Y]
- Độ bao phủ kiểm thử: [Z]%
- Số mã mồ côi phát hiện: [0]
```
