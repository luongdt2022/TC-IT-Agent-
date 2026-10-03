---
name: sa-design
description: "Thiết kế kỹ thuật chi tiết (Detail Design - Shousai Sekkei): Schema CSDL & ERD (DD-01), Hợp đồng API OpenAPI/gRPC (DD-02), Sơ đồ Tuần tự luồng phức tạp (DD-03), và Máy trạng thái thực thể (DD-04)."
---

# Kỹ Năng: sa-design (Thiết Kế Kỹ Thuật Chi Tiết - Shousai Sekkei)

> **Role Chịu Trách Nhiệm**: TL/SA Agent (`techlead-sa`) — Software Architect & Tech Lead.  
> **Cổng Kiểm Soát**: Gate 2 Detailed Design Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Thiết kế cơ sở tại `docs/01-basic-design/` và đặc tả `specs/[epic-id]/spec.md`.
- **Target Output Directory**: `docs/02-detail-design/`
  - `docs/02-detail-design/DD-01-database-erd.md` (Schema CSDL, Data Dictionary, Indexing, Khóa ngoại)
  - `docs/02-detail-design/DD-02-api-contracts.md` (OpenAPI REST / gRPC Contracts, mã lỗi chuẩn)
  - `docs/02-detail-design/DD-03-sequence-flows.md` (Sơ đồ tuần tự cho các luồng giao dịch phức tạp)
  - `docs/02-detail-design/DD-04-state-machines.md` (Máy trạng thái hữu hạn cho các thực thể quan trọng)
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. NỘI DUNG 4 TÀI LIỆU THIẾT KẾ CHI TIẾT

### 1. `DD-01-database-erd.md` (CSDL & Quan Hệ Thực Thể)
- Sơ đồ quan hệ thực thể (ERD) bằng cú pháp Mermaid `erDiagram`.
- Từ điển dữ liệu chi tiết: Tên bảng (`DB-[TÊN_BẢNG]`), Cột, Kiểu dữ liệu, Nullable, Default, Khóa chính (PK), Khóa ngoại (FK), và Đánh chỉ mục (Indexing: B-Tree, GIN, Unique).
- Chiến lược Partitioning / Sharding (nếu dữ liệu lớn) và cơ chế khóa lạc quan (`xmin` hoặc `RowVersion`).

### 2. `DD-02-api-contracts.md` (Hợp Đồng API Chuẩn Hóa)
- Định nghĩa từng endpoint: `[METHOD] /api/v1/[resource]`.
- Mã định danh API: `API-[MODULE]-[STT]` (Ví dụ: `API-AUTH-001`).
- Request Headers, Query Params, Path Params, JSON Request Body Schema.
- Response Body: Format chuẩn theo Result Pattern:
  ```json
  {
    "success": true,
    "data": { ... },
    "error": null,
    "timestamp": "2026-10-03T16:00:00Z"
  }
  ```
- Danh mục mã lỗi cụ thể (Error Codes: `AUTH_INVALID_CREDENTIALS`, `RESOURCE_NOT_FOUND`...).

### 3. `DD-03-sequence-flows.md` (Sơ Đồ Tuần Tự)
- Vẽ bằng Mermaid `sequenceDiagram` biểu diễn tương tác giữa Client ➔ Gateway ➔ Controller ➔ MediatR/Service ➔ Repository ➔ DB/Queue ➔ External Services.

### 4. `DD-04-state-machines.md` (Máy Trạng Thái)
- Biểu diễn bằng Mermaid `stateDiagram-v2` cho các thực thể có vòng đời phức tạp (ví dụ: Trạng thái đơn hàng: `DRAFT` ➔ `PENDING_PAYMENT` ➔ `PAID` ➔ `SHIPPED` ➔ `CANCELLED`).
