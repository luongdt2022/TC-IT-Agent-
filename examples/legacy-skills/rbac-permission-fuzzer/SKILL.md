---
name: rbac-permission-fuzzer
description: "Chuyên gia Thẩm định & Fuzzing Phân quyền (3D Scoped RBAC Fuzzer). Tự động kiểm thử ma trận phân quyền 10 Roles, giả lập các trường hợp leo thang đặc quyền (Privilege Escalation) và rò rỉ dữ liệu ngoài phạm vi (Cross-Tenant/Cross-Scope)."
metadata:
  short-description: Fuzzing và kiểm thử ma trận phân quyền 10 roles 3D Scoped RBAC
---

# 3D Scoped RBAC Permission Fuzzer (`rbac-permission-fuzzer`)

Skill chuyên trách dành cho **Agent QC** và **Agent TechLead / SA** để bảo vệ an ninh hệ thống và phân quyền đa chiều.

## 1. MÔ HÌNH PHÂN QUYỀN 3 CHỮ SỐ (3D SCOPED RBAC)
Trong hệ sinh thái NacenTech, quyền hạn không chỉ phụ thuộc vào `Role` mà phụ thuộc vào 3 chiều:
1. **Role (Vai trò)**: 10 Roles (SuperAdmin, Admin, SubAdmin, DN_CongNghe, DN_SanXuat, ChuyenGia_Full, ChuyenGia_Basic, HocVien, KhachHang, VangLai).
2. **Scope (Phạm vi dữ liệu)**: Toàn hệ thống (Global), Đơn vị sở tại (Org/Tenant), Bản ghi cá nhân (Personal/Owner), Phạm vi địa bàn (Province/Region).
3. **Action (Hành động)**: Create, Read, Update, Delete, Approve, Export, Audit.

## 2. QUY TRÌNH THỰC THI KIỂM THỬ PHÂN QUYỀN

### Bước 1: Trích Xuất Ma Trận Quyền Của Endpoint
- Đọc đặc tả API trong `spec.md` hoặc code controller.
- Xác định rõ: Endpoint này ai được gọi? Dữ liệu trả về giới hạn ở Scope nào?

### Bước 2: Thiết Lập Ma Trận Thử Nghiệm Đối Kháng (Adversarial Matrix)
Chạy thử nghiệm với 4 kịch bản vi phạm thường gặp:
1. **Unauthenticated Access**: Gọi API không có Bearer Token $\rightarrow$ Kỳ vọng: `401 Unauthorized`.
2. **Wrong Role Call**: Dùng token `HocVien` hoặc `KhachHang` gọi API duyệt bài / sửa thông tin công nghệ $\rightarrow$ Kỳ vọng: `403 Forbidden`.
3. **Cross-Tenant IDOR (Insecure Direct Object Reference)**:
   - User A (Doanh nghiệp A) cố tình truyền `id` hồ sơ của Doanh nghiệp B vào URL Update $\rightarrow$ Kỳ vọng: `403 Forbidden` hoặc `404 Not Found`.
4. **Elevation of Privilege**: Gửi payload cố tình chèn trường `"role": "SuperAdmin"` hoặc `"isApproved": true` trong request DTO $\rightarrow$ Kỳ vọng: Hệ thống bỏ qua hoặc báo lỗi.

### Bước 3: Xuất Báo Cáo An Ninh Phân Quyền
```markdown
### BÁO CÁO KIỂM TRA PHÂN QUYỀN 3D RBAC: [ENDPOINT / MODULE]
- Endpoint: `[METHOD] /api/v1/...`
- Ma trận đã test: ... kịch bản
- Kết quả:
  - [x] Unauthenticated: 401 PASS
  - [x] Wrong Role: 403 PASS
  - [x] IDOR Cross-Scope: PASS (Không truy cập chéo được)
  - [x] Parameter Tampering: PASS (Không bị leo thang)
- Kết luận: [SECURE] / [VULNERABILITY DETECTED]
```
