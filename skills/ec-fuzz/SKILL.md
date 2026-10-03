---
name: ec-fuzz
description: "Chuyên gia Thẩm định & Fuzzing Phân quyền (Scoped RBAC & Security Fuzzer). Tự động kiểm thử ma trận phân quyền đa vai trò, giả lập leo thang đặc quyền (Privilege Escalation) và rò rỉ dữ liệu ngoài phạm vi (IDOR / Multi-tenant leak)."
---

# Kỹ Năng: ec-fuzz (Fuzzing Bảo Mật & Ma Trận Phân Quyền RBAC)

> **Role Chịu Trách Nhiệm**: EC Agent (`ec`) — Edge-Case Hunter & QC Specialist.  
> **Cổng Kiểm Soát**: Gate 4 Security & RBAC Compliance Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Ma trận phân quyền tại Mục 2 trong `specs/[epic-id]/spec.md` và các API endpoints trong `docs/02-detail-design/DD-02-api-contracts.md`.
- **Target Output File**: `tests/security/FUZZING_REPORT.md`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. 4 KỊCH BẢN FUZZING BẢO MẬT BẮT BUỘC

1. **Kiểm Tra Không Có Token (Unauthenticated Access)**:
   - Gửi request đến tất cả các endpoint yêu cầu đăng nhập mà không đính kèm Header `Authorization`.
   - Kỳ vọng: 100% trả về `401 Unauthorized`.
2. **Kiểm Tra Sai Vai Trò (Vertical Privilege Escalation)**:
   - Dùng token của người dùng thông thường (`Role: User`) để gọi API quản trị (`POST /api/v1/admin/users`, `DELETE /api/v1/settings`).
   - Kỳ vọng: 100% trả về `403 Forbidden`.
3. **Kiểm Tra Tấn Công Vượt Quyền Ngang Hàng (Horizontal Privilege Escalation / IDOR)**:
   - User A gửi request xem hoặc chỉnh sửa đơn hàng của User B bằng cách sửa `orderId` trên URL (`GET /api/v1/orders/{user_b_order_id}`).
   - Kỳ vọng: Hệ thống phải kiểm tra quyền sở hữu (Ownership Check) và trả về `404 Not Found` hoặc `403 Forbidden`.
4. **Kiểm Tra Rò Rỉ Đa Tenant (Cross-Tenant Data Leakage)**:
   - Trong hệ thống Multi-tenant, Tenant 1 tìm cách truy cập dữ liệu của Tenant 2 qua tham số `tenant_id` hoặc header giả mạo.

---

## 3. CẤU TRÚC BÁO CÁO FUZZING_REPORT.MD

```markdown
# BÁO CÁO KIỂM THỬ BẢO MẬT & PHÂN QUYỀN (RBAC FUZZING REPORT)

- **Thời gian quét**: [YYYY-MM-DD HH:mm]
- **Số lượng Endpoint kiểm tra**: [X]
- **Số vai trò (Roles) giả lập**: [Admin, Manager, User, Guest]

## KẾT QUẢ KIỂM THỬ MA TRẬN
| Endpoint | Phương Thức | Quyền Kỳ Vọng | Quyền Thử Nghiệm | Mã HTTP Trả Về | Đánh Giá |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `/api/v1/users` | GET | `admin` | `guest` | 401 | [PASS] |
| `/api/v1/users/export` | POST | `admin` | `user` | 403 | [PASS] |
| `/api/v1/orders/123` | GET | `owner` | `other_user` | 404 | [PASS] |

## KẾT LUẬN GATE 4 SECURITY
- [x] Không có lỗ hổng IDOR.
- [x] Không có lỗ hổng leo thang đặc quyền.
- **Phán quyết**: [RBAC COMPLIANCE PASS]
```
