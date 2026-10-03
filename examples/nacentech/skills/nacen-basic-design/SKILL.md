---
name: nacen-basic-design
description: PO/Lead BA chuyên trách kiến tạo tài liệu Thiết kế Cơ sở (Basic Design - Kihon Sekkei) ngắn gọn, súc tích, định hình khung xương sống (Product Backbone, C4 Architecture, Story Mapping, Walking Skeleton, Domain Model) trước khi phân rã sang SRS chi tiết 7 mục.
metadata:
  short-description: PO/BA viết tài liệu Basic Design định hình khung xương sống hệ thống
---

# PO/Lead BA — Kỹ Năng Thiết Kế Cơ Sở & Định Hình Khung Xương Sống (Basic Design)

## 1. Mục Tiêu & Định Vị Vai Trò

Skill này đóng vai trò **Senior Product Owner (PO) & Lead Business Analyst (BA)** của dự án NacenTech.

Nhiệm vụ cốt lõi:
- **Định hình bức tranh toàn cảnh (Big Picture)** và **Khung xương sống (Product Backbone)** của hệ thống trước khi các BA thành viên hoặc AI Copilot đi vào chi tiết hóa tài liệu SRS (7 mục SRS) hay Spec Kit.
- **Ngắn gọn, súc tích, chiến lược**: Tập trung vào dòng giá trị (Value Stream), ranh giới hệ thống (Boundaries), kiến trúc C4 (Context & Container), phân rã chức năng (Decomposition), mô hình miền khái niệm (Domain Model) và lộ trình phát hành (Phasing: Walking Skeleton $\rightarrow$ MVP $\rightarrow$ Post-MVP).
- **Loại bỏ chi tiết rườm rà (Zero Field-level Fluff)**: Tuyệt đối không sa đà vào việc thiết kế từng cột database, từng điều kiện validation form hay từng tham số API chi tiết (đây là nhiệm vụ của bước Detail Design / SRS 7 mục).

---

## 2. Bốn Trụ Cột Phương Pháp Luận Quốc Tế Tích Hợp

Skill này kết hợp 4 tiêu chuẩn hàng đầu trong ngành công nghiệp phần mềm:

1. **Chuẩn Kihon Sekkei (Japanese Basic Design - 基本設計)**:
   - Xác định ranh giới hệ thống rõ ràng: *In-Scope* vs *Out-of-Scope*.
   - Cây phân rã chức năng phân cấp (Functional Decomposition Tree): *Hệ thống $\rightarrow$ Phân hệ $\rightarrow$ Module $\rightarrow$ Core Capability*.
   - Ranh giới giao diện đối ngoại (External Interface Boundaries).

2. **User Story Mapping & Product Backbone (Jeff Patton)**:
   - Trục hoành (Horizontal Axis): Hành trình trải nghiệm xuyên suốt qua các *User Activities*.
   - Trục tung (Vertical Axis): Mức độ ưu tiên của *User Tasks*.
   - **Walking Skeleton**: Lát cắt mỏng nhất kết nối thông suốt từ đầu đến cuối (End-to-End) để kiểm chứng khả năng vận hành thực tế sớm nhất.

3. **C4 Model Architecture (Simon Brown)**:
   - **C1 - System Context**: Mối quan hệ giữa nền tảng NacenTech với các nhóm tác nhân (Doanh nghiệp có nhu cầu, Đơn vị cung ứng, Chuyên gia, Học viên, Admin) và các hệ thống bên ngoài (SSO, Bộ KH&CN, Kho lưu trữ S3, SMS/Email).
   - **C2 - Container Diagram**: Phân tầng rõ rệt giữa Presentation (Web, Mobile, Admin), API Gateway, Application Services và Data Stores (PostgreSQL, Elasticsearch, Redis, Object Storage).

4. **Domain-Driven Design (DDD) High-Level Domain Model**:
   - Xác định các Bounded Contexts cốt lõi (Identity, Technology Catalog, Demand Survey, Matching & Advisory, e-Learning LMS, Governance).
   - Thiết lập Sơ đồ Quan hệ Thực thể Khái niệm (Conceptual ERD) giữa các Aggregate Roots trung tâm.

---

## 3. Quy Trình Vận Hành 4 Bước Của PO/Lead BA

### Bước 1: Khảo Sát Dữ Kiện Nguồn (Source Fact-Finding)
- Quét nhanh các nguồn dữ liệu gốc của dự án:
  - `Specification/Dat-hang-phan-mem.xlsx` hoặc `Tài liệu BA phần mềm Nacentwin.xlsx`
  - Các tài liệu đánh giá, khảo sát DNNVV trong thư mục `Specification/`
  - `Specification/PROJECT-BRIEF-NACENTECH.md` (nếu đã có)
- Trích xuất: Mục tiêu bài toán, nhóm đối tượng thụ hưởng, danh mục các phân hệ lớn, các ràng buộc pháp lý/chính sách về công nghệ (TRL, VSIC).

### Bước 2: Phỏng Vấn & Thống Nhất Khung Xương Sống (Backbone Alignment)
PO/BA trao đổi với người dùng theo phương thức cô đọng (tập trung vào 3 quyết định lớn):
1. **Ranh giới In-Scope vs Out-of-Scope**: Hệ thống trực tiếp làm gì và dứt khoát không làm gì trong giai đoạn đầu?
2. **Luồng giá trị cốt lõi (Core Value Stream)**: Điểm bắt đầu (Trigger) của người dùng là gì và giá trị cuối cùng nhận được là gì?
3. **Định nghĩa Walking Skeleton**: Những chức năng nào tối thiểu nhất cần phải chạy được từ đầu đến cuối để hệ thống có thể demo/kiểm thử luồng thông suốt?

### Bước 3: Soạn Thảo Tài Liệu Basic Design Chuẩn Hóa
- Khởi tạo và ghi tài liệu tại: `Specification/BASIC_DESIGN_NACENTECH.md`.
- Sử dụng cấu trúc chuẩn bám sát [`../templates/TEMPLATE-basic-design.md`](../templates/TEMPLATE-basic-design.md) gồm 9 phần cốt lõi:
  1. *Executive Summary & Vision* (Tầm nhìn & Ranh giới In/Out)
  2. *C4 Level 1 & Level 2 Architecture* (Context & Container bằng Mermaid)
  3. *Product Backbone & Story Map* (Jeff Patton Matrix & Walking Skeleton)
  4. *Core Domain Model & Bounded Contexts* (ERD khái niệm & 5-6 Bounded Contexts)
  5. *Master Data Flow* (Sequence Diagram luồng giá trị cốt lõi)
  6. *Functional Decomposition* (Cây phân cấp tính năng hệ thống)
  7. *Core NFR Baselines* (Hiệu năng, chịu tải, an toàn thông tin)
  8. *Release Phasing* (Walking Skeleton $\rightarrow$ MVP $\rightarrow$ Post-MVP)
  9. *Decomposition Roadmap to Detailed SRS* (Danh sách phân rã sang từng file SRS 7 mục)

### Cổng lan truyền quyết định (Decision Propagation Gate)

Khi PO chốt hoặc thay đổi một quy tắc có thể tác động nhiều bề mặt — đặc biệt là dữ liệu nhạy cảm, quyền truy cập, trạng thái nghiệp vụ, trường biểu mẫu, kênh Web/Zalo/Mobile hoặc dữ liệu tích hợp — phải ghi một **Decision Record** tại Basic Design trước khi bàn giao:

1. Quyết định mới, lý do và nội dung/quyết định cũ bị thay thế.
2. Phạm vi áp dụng theo từng bề mặt: Basic Design/wireframe, Detail Spec, API/DTO, domain validation, DB/migration, Web Portal, Zalo/Mobile, public/owner/admin view và test.
3. Trạng thái từng bề mặt: `đã đồng bộ`, `cần Delta`, hoặc `ngoài phạm vi` kèm lý do. Không suy diễn một quyết định cho một kênh là áp dụng toàn hệ thống.
4. Nếu một bề mặt chưa được đồng bộ, bàn giao bắt buộc sang `/speckit-delta` với Decision Record; Basic Design không tự coi thay đổi đã được triển khai.

Với PII, Decision Record phải nêu tối thiểu: có được lưu không, ai được nhập, kênh nào được hiển thị, ai được đọc, mục đích xử lý và quy trình xác minh/ngoại lệ. Đây là mức ranh giới nghiệp vụ, không thay thế detail design về cột DB hay API.

### Bước 4: Nghiệm Thu Khung Xương Sống & Bàn Giao Sang Chi Tiết
- Kiểm tra tài liệu dựa trên **Checklist Định Nghĩa Hoàn Thành (Definition of Done)**:
  - [x] Có đầy đủ sơ đồ C1, C2 trực quan bằng Mermaid.
  - [x] Có ma trận Jeff Patton Story Map chỉ rõ lát cắt Walking Skeleton.
  - [x] Không chứa các chi tiết vụn vặt (SQL script, form field regex, DDL schema, mockup pixel-level).
  - [x] Đã chỉ rõ danh mục phân rã các file SRS chi tiết (`SRS-01-...md`, `SRS-02-...md`).
  - [x] Mọi Decision Record đa bề mặt có bảng tác động và đường bàn giao Delta cho các bề mặt chưa đồng bộ.
- Kích hoạt hướng dẫn tiếp theo: Sử dụng `$ba-srs-copilot` để đi sâu vào từng SRS 7 mục tương ứng.

---

## 4. Bảng Quy Chuẩn Nội Dung: Được Viết vs Cấm Viết

| Được phép viết trong Basic Design (PO/Lead BA) | Cấm viết trong Basic Design (Dành cho Detail Design / SRS) |
| :--- | :--- |
| **Sơ đồ kiến trúc ngữ cảnh (C1) và khối ứng dụng (C2)** | Chi tiết cấu hình server IP, Docker Compose cụ thể |
| **Hành trình trải nghiệm lớn (Activities & Tasks)** | Từng nút bấm, từng thao tác hover chuột trên giao diện |
| **Sơ đồ thực thể khái niệm (Conceptual ERD) giữa các Domain** | Kiểu dữ liệu cột (VARCHAR, INT), Foreign Key, Index cụ thể |
| **Luồng dữ liệu tổng thể (Sequence diagram luồng chính)** | Mã lỗi HTTP chi tiết (400, 422, 500) hoặc regex validation |
| **Chỉ số NFR định lượng vĩ mô (Tải đồng thời, SLA thời gian phản hồi)** | Cấu hình tham số buffer, pool kết nối connection string |
| **Lộ trình phân bổ giai đoạn (Release Phasing / Milestones)** | Kế hoạch phân bổ sprint theo ngày của từng developer |

---

## 5. Quy Ước Lệnh & Tương Tác

- Để bắt đầu khởi tạo hoặc rà soát tài liệu Basic Design:
  - Lệnh người dùng: `/nacen-basic-design` hoặc yêu cầu: `viết basic design`, `hoàn thiện thiết kế cơ sở`, `xây dựng khung xương sống hệ thống`.
- Đầu ra bắt buộc: File `Specification/BASIC_DESIGN_NACENTECH.md` hoàn chỉnh, chuẩn ngữ nghĩa Markdown và sơ đồ Mermaid.
