---
name: ec-contract
description: "Chuyên gia Kiểm định Hợp đồng API (Contract Testing Specialist): Tự động xác thực tính tương thích API giữa Consumer (Frontend / Client API SDK) và Provider (Backend API / Microservices), phát hiện Breaking Changes và lệch DTO."
---

# Kỹ Năng: ec-contract (Kiểm Định Hợp Đồng API Consumer-Provider)

> **Role Chịu Trách Nhiệm**: EC Agent (`ec`) — Edge-Case Hunter & QC Specialist.  
> **Cổng Kiểm Soát**: Gate 4 API Compatibility Gatekeeper.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: 
  - Consumer: Client API layer, API hooks, SDK callers.
  - Provider: Controllers, Routers, DTOs backend.
  - Schema: OpenAPI (Swagger json/yaml), Protobuf, GraphQL schema, hoặc CSDL model.
- **Target Output File**: `tests/contract/CONTRACT_VERIFICATION_REPORT.md` (hoặc `docs/decisions/CONTRACT_VERIFICATION_REPORT.md`)
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. NGUYÊN LÝ KIỂM THỬ HỢP ĐỒNG (CONSUMER-DRIVEN CONTRACT TESTING)

Đảm bảo hai bên độc lập không bao giờ "nói khác ngôn ngữ":
```
[ Consumer: Frontend / WebApp ]  ----(Gửi Request theo DTO kỳ vọng)----> [ Contract: OpenAPI / DTO Schema ]
                                                                                   |
[ Provider: Backend API Service ] <---(Phải trả về đúng Response Schema)-----------+
```

### 4 Trụ Cột Thẩm Định Contract:
1. **Phát Hiện Breaking Changes (Tương Thích Ngược)**:
   - Phát hiện các trường (fields) bị xoá bỏ, đổi tên (`snake_case` vs `camelCase`).
   - Phát hiện các trường bắt buộc (`required`) mới được thêm vào request body khiến client cũ bị lỗi 400 Bad Request.
2. **Kiểm Tra Định Dạng Dữ Liệu (Payload Type Verification)**:
   - Kiểu số vs kiểu chuỗi (`id: string` vs `id: number`), định dạng ngày giờ ISO 8601 (`YYYY-MM-DDTHH:mm:ss.sssZ`).
   - Trạng thái Nullable/Optional giữa DTO backend và interface frontend.
3. **Mã Trạng Thái & Lỗi Chuẩn Hóa (HTTP Status Codes & Error Shapes)**:
   - Các mã lỗi 400, 401, 403, 404, 409, 422, 500 bắt buộc có cấu trúc thống nhất: `{ statusCode, message, error, timestamp, path }`.
4. **Cô Lập Đa Tổ Chức & Ngữ Cảnh Bảo Mật (Tenant / Auth Context Header)**:
   - Hợp đồng bắt buộc yêu cầu Header xác thực hoặc Tenant Context (Tenant ID / Org ID) trong JWT token. Mọi API nghiệp vụ không có tenant context đều bị coi là vi phạm Contract.

---

## 3. CẤU TRÚC BÁO CÁO CONTRACT_VERIFICATION_REPORT.MD

```markdown
# BÁO CÁO KIỂM THỬ HỢP ĐỒNG API (API CONTRACT REPORT)

- **Thời gian**: [YYYY-MM-DD HH:mm]
- **Kiểm định viên**: EC Agent

## 1. TỔNG HỢP KIỂM ĐỊNH CONTRACT
| Endpoint | Method | Consumer | Provider | Trạng Thái | Breaking Changes |
| :--- | :---: | :--- | :--- | :---: | :---: |
| `/api/v1/users` | GET | `WebApp Client` | `User Service` | [PASS] | Không |
| `/api/v1/orders` | POST | `WebApp Client` | `Order Service` | [PASS] | Không |

## 2. CHI TIẾT VI PHẠM (NẾU CÓ)
- [Cảnh báo/Lỗi]: Thiếu trường hoặc lệch type.
```
