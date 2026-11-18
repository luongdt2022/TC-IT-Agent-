# KHUNG THAM CHIẾU KỸ NĂNG BASIC DESIGN (PO / LEAD BA FRAMEWORK)
## Tích hợp: Japanese Kihon Sekkei × Jeff Patton Story Mapping × C4 Model × Domain-Driven Design

---

## 1. BẢN CHẤT VÀ SỰ KHÁC BIỆT GIỮA BASIC DESIGN VÀ DETAIL DESIGN (SRS)

| Tiêu chí | Basic Design (Thiết kế cơ sở - Khung xương sống) | Detail Design / SRS (Thiết kế chi tiết) |
| :--- | :--- | :--- |
| **Vai trò chính** | **Product Owner (PO) / Lead System Architect / Senior BA** | **Business Analyst (BA) / Tech Lead / Dev** |
| **Mục tiêu** | Định hình bức tranh toàn cảnh, kiến trúc hệ thống, dòng giá trị và bộ khung xương sống (Backbone) không thể lay chuyển | Đặc tả từng màn hình, quy tắc nghiệp vụ (`BR-`), cấu trúc bảng (`DB-`), tham số API (`API-`) chi tiết |
| **Độ chi tiết** | **High-Level & Súc tích (10–25 trang)**. Tập trung vào sơ đồ (Mermaid), bảng phân rã và quyết định chiến lược | **Deep-Dive (50–200+ trang)**. Tỉ mỉ từng field, validation, error codes, state machines |
| **Trọng tâm trả lời** | *What & Why*: Hệ thống làm gì, giải quyết bài toán lớn nào, các phân hệ phối hợp ra sao, đi từ đâu đến đâu? | *How*: Hệ thống thực thi chính xác như thế nào trong từng tương tác người dùng? |
| **Đầu ra cốt lõi** | C4 Context/Container, Story Map Backbone, Walking Skeleton, Domain Model, Phasing MVP | 7 Mục SRS, Wireframe chi tiết, DDL Script, API Swagger contracts |

---

## 2. BỐN TRỤ CỘT PHƯƠNG PHÁP LUẬN ĐƯỢC TÍCH HỢP

### Trụ cột 1: Chuẩn Thiết kế Cơ bản Nhật Bản (Kihon Sekkei - 基本設計)
- **Tập trung vào Ranh giới Hệ thống (System Boundary)**: Xác định rõ ranh giới In-Scope vs Out-of-Scope, External Actors và Third-party Systems.
- **Sơ đồ phân rã chức năng (Functional Decomposition)**: Cây phân cấp logic `Hệ thống` $\rightarrow$ `Phân hệ (Subsystem)` $\rightarrow$ `Module` $\rightarrow$ `Core Capability`.
- **Giao diện đối ngoại (External Interface Definition)**: Định nghĩa các kênh tích hợp dữ liệu vĩ mô (SSO, Bộ KH&CN, Cổng thông tin doanh nghiệp, Cổng thanh toán/SMS/Email).

### Trụ cột 2: User Story Mapping & Backbone (Jeff Patton)
- **Trục hoành (Horizontal Axis - The Backbone)**: Hành trình trải nghiệm theo thời gian từ trái qua phải:
  $$\text{Khám phá / Tiếp cận} \longrightarrow \text{Định danh / Đăng ký} \longrightarrow \text{Khảo sát Nhu cầu / Đăng tải Công nghệ} \longrightarrow \text{Khớp nối & Tư vấn Chuyên gia} \longrightarrow \text{Đào tạo & Chuyển giao} \longrightarrow \text{Đánh giá & Quản trị}$$
- **Walking Skeleton (Phiên bản sống tối thiểu)**: Lát cắt mỏng nhất (thực thi được end-to-end) đi xuyên suốt từ đầu đến cuối hành trình để sớm chứng minh tính khả thi về mặt kỹ thuật và nghiệp vụ.
- **Lát cắt phát hành (Release Slicing)**: Phân tầng rạch ròi:
  - *Slice 1: Walking Skeleton (Khung chạy được)*
  - *Slice 2: MVP (Tối thiểu khả dụng cho người dùng thực)*
  - *Slice 3: Phase 1 (Mở rộng & Nâng cao)*

### Trụ cột 3: C4 Architecture Model (Simon Brown)
- **Level 1 - System Context**: Vị trí của nền tảng NacenTech trong bức tranh tổng thể: tương tác với Doanh nghiệp DNNVV, Doanh nghiệp cung ứng công nghệ, Viện/Trường, Đội ngũ Chuyên gia và Cán bộ Quản trị.
- **Level 2 - Container Diagram**: Kiến trúc phân tầng các khối phần mềm có thể deploy độc lập:
  - Client Containers: Web Portal (Responsive), Mobile App/PWA, Admin Portal.
  - Gateway & API Layer: API Gateway, Reverse Proxy, Identity Provider (IAM/RBAC).
  - Backend Services: Tech Catalog Service, Matching Engine, Expert Network Service, LMS Service, Survey Service.
  - Data Stores: Relational Database (PostgreSQL), Full-text Search Engine (Elasticsearch), Object Storage (MinIO/S3), Cache (Redis).

### Trụ cột 4: Domain-Driven Design (DDD) High-Level Domain Model
- Phân định các **Bounded Contexts** cốt lõi:
  1. *Identity & Profile Context*: Quản lý danh tính, hồ sơ năng lực DN và Chuyên gia.
  2. *Technology Catalog Context*: Quản lý danh mục công nghệ, TRL 1–9, ngành kinh tế VSIC.
  3. *Survey & Demand Context*: Khảo sát nhu cầu công nghệ DNNVV, phiếu đánh giá.
  4. *Matching & Advisory Context*: Thuật toán gợi ý, kết nối DN - Chuyên gia, lịch hẹn tư vấn.
  5. *Knowledge & E-Learning Context*: Khóa đào tạo chuyển giao công nghệ, bài giảng, chứng chỉ.
- Xác định các **Core Aggregate Roots**: `Technology`, `DemandTicket`, `ExpertProfile`, `ConsultationSession`, `Course`, `EnterpriseUser`.

---

## 3. CHECKLIST KIỂM ĐỊNH CHẤT LƯỢNG BASIC DESIGN (DEFINITION OF DONE)

Một tài liệu Basic Design chỉ được coi là hoàn thiện khi đáp ứng đầy đủ 6 tiêu chí:

1. **Tính Tổng Thể (Holistic View)**: Bất kỳ lập trình viên hay stakeholder nào đọc xong trong 15 phút đều hiểu rõ toàn bộ dự án làm gì và không làm gì.
2. **Tính Xương Sống (Backbone Clarity)**: Có Story Map chỉ rõ hành trình người dùng và lát cắt Walking Skeleton chạy thông suốt từ đầu đến cuối.
3. **Tính Phân Ranh Giới (Clear Boundaries)**: Không có sự nhập nhằng giữa các Bounded Contexts; ranh giới In/Out rõ ràng.
4. **Không Sa Vào Chi Tiết Vụn Vặt (Zero Field-Level Fluff)**: Không liệt kê từng trường dữ liệu form, không vẽ mockup pixel-perfect, không viết code SQL/API endpoints chi tiết (để dành cho SRS & Detail Design).
5. **Khả Năng Phân Rã (Decomposition Readiness)**: Mỗi phân hệ trong Basic Design có thể tách độc lập thành một tài liệu SRS 7 mục hoặc một Spec Kit Epic.
6. **Thống Nhất Thuật Ngữ (Ubiquitous Language)**: Sử dụng chuẩn thuật ngữ đồng nhất: DNNVV, TRL (1–9), VSIC (Hệ thống ngành kinh tế VN), Đơn vị sở hữu công nghệ, Chuyên gia tư vấn.
