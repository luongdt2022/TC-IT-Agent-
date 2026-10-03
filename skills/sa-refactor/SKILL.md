---
name: sa-refactor
description: "Quét phân tích toàn diện dự án mã nguồn có sẵn (Brownfield / Legacy), đánh giá nợ kỹ thuật, cấu trúc thư mục, độ phụ thuộc module và lập Đề Xuất Giải Pháp Refactor an toàn (không làm hỏng hay sai khác hệ thống cũ)."
---

# Kỹ Năng: sa-refactor (Quét & Đề Xuất Giải Pháp Tái Cấu Trúc An Toàn)

> **Role Chịu Trách Nhiệm**: TL/SA Agent (`techlead-sa`) — Software Architect & Tech Lead.  
> **Cổng Kiểm Soát**: Legacy System Modernization & Refactoring Gate.

---

## 1. NGUYÊN TẮC BẤT BIẾN: AN TOÀN TUYỆT ĐỐI (NON-DESTRUCTIVE SCAN)

1. **Chế Độ Quét Chỉ Đọc (Strictly Read-Only)**:
   - Kỹ năng này **TUYỆT ĐỐI KHÔNG** tự ý sửa đổi, xóa, di chuyển hay đổi tên bất kỳ tệp tin mã nguồn nào trong hệ thống hiện tại.
2. **Không Tái Cấu Trúc Kiểu Đập Đi Xây Lại (No Big-Bang Rewrite)**:
   - Mọi đề xuất phải dựa trên mô hình **Strangler Fig Pattern** (Bọc dần từng phần): Giữ nguyên hệ thống cũ hoạt động ổn định, bóc tách dần từng module sang kiến trúc mới qua Adapter / Facade.
3. **Bảo Tồn Nghiệp Vụ Hiện Hữu (Preserve Existing Business Invariants)**:
   - Đảm bảo các luồng tính toán, API contracts và cấu trúc dữ liệu hiện tại không bị sai lệch.

---

## 2. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Toàn bộ mã nguồn hiện hữu của dự án (trong `src/`, `backend/`, `frontend/`...).
- **Target Output Directory**: Lưu tại thư mục tài liệu quản trị, không xả file ra root:
  - `docs/02-detail-design/AS_IS_SYSTEM_ANALYSIS.md` (Báo cáo phân tích hiện trạng kiến trúc As-Is)
  - `docs/02-detail-design/TO_BE_ARCHITECTURE.md` (Bản thiết kế kiến trúc đích To-Be)
  - `docs/00-presale-proposal/REFACTORING_PROPOSAL.md` (Hồ sơ đề xuất giải pháp & Dự toán nỗ lực cho Giám đốc/Khách hàng)
  - `backlog/REFACTORING_ROADMAP.md` (Lộ trình tái cấu trúc từng giai đoạn an toàn)

---

## 3. 5 BƯỚC QUÉT VÀ PHÂN TÍCH HỆ THỐNG CŨ

### Bước 1: Khảo Sát Tổng Thể Ngữ Cảnh Kỹ Thuật (Tech Stack & Footprint Discovery)
- Quét các file cấu hình build: `package.json`, `pom.xml`, `.csproj`, `go.mod`, `requirements.txt`...
- Nhận diện: Ngôn ngữ, Framework, Phiên bản, Thư viện bên thứ ba (Third-party packages) và các thư viện đã hết hạn bảo mật (Deprecated/Vulnerable).
- Nhận diện cấu trúc thư mục hiện tại: Monolith phẳng, Spaghetti code, hay đã có phân tầng sơ bộ.

### Bước 2: Quét Phân Tích CSDL & Rò Rỉ Tầng Dữ Liệu (Data Layer & Leakage Scan)
- Quét ORM / CSDL: Entity Framework, Hibernate, Prisma, TypeORM, Raw SQL.
- Phát hiện các rò rỉ:
  - Controller gọi trực tiếp câu lệnh SQL / Query CSDL.
  - Thiếu chỉ mục (Indexes) trên các bảng lớn.
  - Thiếu khóa ngoại (Foreign Keys) gây mồ côi dữ liệu.
  - Vấn đề N+1 query tiềm ẩn.

### Bước 3: Đánh Giá Nợ Kỹ Thuật & Điểm Nghẽn (Technical Debt & Code Smells)
- **God Classes / God Functions**: Các class hoặc controller dài hơn 1,000 dòng gánh vác quá nhiều trách nhiệm.
- **Tight Coupling (Khớp nối quá chặt)**: Các module gọi chéo phụ thuộc vòng tròn (Circular Dependency).
- **Hardcoded Secrets**: Chuỗi kết nối CSDL, API Keys, Passwords nằm trực tiếp trong code thay vì đọc từ biến môi trường (`.env`).
- **Thiếu Kiểm Thử**: Tỷ lệ bao phủ Unit Test hiện tại (thường là 0% hoặc rất thấp ở dự án cũ).

### Bước 4: Thiết Kế Kiến Trúc Đích (To-Be Architecture)
- Lập sơ đồ kiến trúc mục tiêu chuẩn hóa theo **Clean Architecture / Modular Monolith**:
  - `Domain` độc lập.
  - `Application` xử lý Use Cases.
  - `Infrastructure` bao bọc CSDL và Third-party.
  - `Presentation` chuẩn hóa DTOs và Response Result Pattern.

### Bước 5: Lập Lộ Trình Tái Cấu Trúc An Toàn (Strangler Fig Roadmap)
- Chia nhỏ quá trình refactor thành các giai đoạn độc lập:
  - **Phase 1 (Bọc An Toàn - Safety Net)**: Viết Integration Tests bao phủ các luồng then chốt trước khi sửa code.
  - **Phase 2 (Tách Lõi - Core Extraction)**: Trích xuất các thực thể Domain và quy tắc nghiệp vụ quan trọng nhất.
  - **Phase 3 (Thay Cổng - Facade & API Routing)**: Dựng API Gateway / Adapter bọc ngoài để chuyển hướng dần request sang code mới.
  - **Phase 4 (Dọn Rác - Deprecation)**: Vô hiệu hóa code cũ an toàn sau khi code mới đã chạy ổn định 100%.
