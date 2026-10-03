# TÀI LIỆU THIẾT KẾ CHI TIẾT HỢP ĐỒNG API (API CONTRACT SPECIFICATION)

*Mã tài liệu: `DD-02-API-CONTRACTS` | Dự án: `{{PROJECT_NAME}}` | Định dạng: `RESTful JSON`*

---

## 1. TIÊU CHUẨN GIAO THỨC CHUNG (GLOBAL API CONVENTIONS)
- **Base URL**: `https://api.{{DOMAIN}}/api/v1`
- **Authentication**: Bearer Token (JWT) truyền qua Header: `Authorization: Bearer <token>`
- **Content-Type**: `application/json; charset=utf-8`
- **Format Phản Hồi Chuẩn (Envelope Result Pattern)**:
  ```json
  {
    "success": true,
    "data": { ... },
    "error": null,
    "timestamp": "2026-10-03T16:00:00Z"
  }
  ```
- **Format Phản Hồi Lỗi Chuẩn**:
  ```json
  {
    "success": false,
    "data": null,
    "error": {
      "code": "AUTH_INVALID_CREDENTIALS",
      "message": "Email hoặc mật khẩu không chính xác.",
      "details": []
    },
    "timestamp": "2026-10-03T16:00:00Z"
  }
  ```

---

## 2. DANH SÁCH ENDPOINTS CHI TIẾT

### Endpoint 1: Đăng Nhập Hệ Thống
- **Mã API**: `API-AUTH-001`
- **Method & Route**: `POST /api/v1/auth/login`
- **Quyền Hạn (RBAC)**: Public (Không cần Token)
- **Mục đích**: Xác thực người dùng và cấp phát Access Token + Refresh Token.

#### Request Headers:
| Header | Giá Trị | Bắt Buộc |
| :--- | :--- | :---: |
| `Content-Type` | `application/json` | YES |

#### Request Body:
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Response Body (`200 OK`):
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "expiresIn": 3600,
    "refreshToken": "d8e39f82-...",
    "user": {
      "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
      "email": "user@example.com",
      "fullName": "Nguyễn Văn A",
      "roles": ["USER"]
    }
  },
  "error": null,
  "timestamp": "2026-10-03T16:00:00Z"
}
```

#### Mã Lỗi Nghiệp Vụ Có Thể Xảy Ra:
| Mã HTTP | Mã Lỗi (Error Code) | Mô Tả |
| :---: | :--- | :--- |
| `400` | `VALIDATION_FAILED` | Định dạng email không hợp lệ hoặc thiếu mật khẩu |
| `401` | `AUTH_INVALID_CREDENTIALS` | Sai email hoặc mật khẩu |
| `403` | `AUTH_ACCOUNT_LOCKED` | Tài khoản đã bị khóa do đăng nhập sai quá 5 lần |
| `429` | `RATE_LIMIT_EXCEEDED` | Gửi quá nhiều request đăng nhập trong 1 phút |
