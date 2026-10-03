# BIỂU MẪU TỔNG QUAN DỰ ÁN (PROJECT BRIEF TEMPLATE)
*Khung khơi gợi ý tưởng và xác lập phạm vi ban đầu (BMad Analyst Style) trước khi soạn thảo chi tiết SRS 7 mục*

---

## 1. THÔNG TIN CHUNG (METADATA)

- **Tên dự án / Phân hệ**: [Tên dự án hoặc module cần khảo sát]
- **Mã định danh**: `BRIEF-[MODULE]-[NĂM]`
- **Business Analyst**: [Tên BA phụ trách]
- **Product Owner / Stakeholder**: [Tên các bên liên quan]
- **Trạng thái**: [DỰ THẢO / ĐÃ DUYỆT]
- **Căn cứ tài liệu gốc**: [Liệt kê các file: at-hang-phan-mem-nhung.xlsx (danh mục chức năng đặt hàng), Tai_Lieu_Danh_Gia_NACENTECH.docx...]

---

## 2. VẤN ĐỀ & MỤC TIÊU CỐT LÕI (PROBLEM STATEMENT & CORE GOALS)

### 2.1. Nỗi đau hiện tại (Pain Points)
*Mô tả thực trạng của quy trình hiện tại dẫn đến nhu cầu cần xây dựng hoặc nâng cấp hệ thống:*
- Nỗi đau 1: [Dữ liệu công nghệ bị phân tán, chưa chuẩn hóa theo chuẩn quốc tế và phân loại TRL]
- Nỗi đau 2: [Thiếu kênh kết nối trực tuyến hiệu quả giữa doanh nghiệp có nhu cầu công nghệ và đội ngũ chuyên gia]
- Nỗi đau 3: [Đào tạo, chuyển giao tri thức công nghệ chưa được số hóa và quản lý tập trung]

### 2.2. Mục tiêu hệ thống & Kết quả kỳ vọng (Business Objectives & Outcomes)
*Định lượng kết quả cần đạt được:*
- Mục tiêu 1: [Xây dựng kho dữ liệu công nghệ chuẩn hóa, hỗ trợ tra cứu thông minh và phân loại theo ngành kinh tế / TRL]
- Mục tiêu 2: [Thiết lập nền tảng đào tạo trực tuyến (LMS) phục vụ chuyển giao công nghệ]
- Mục tiêu 3: [Cung cấp mạng lưới kết nối chuyên gia, đặt lịch tư vấn và đánh giá phản hồi]

---

## 3. KHÁCH HÀNG & TÁC NHÂN HỆ THỐNG (TARGET ACTORS & BENEFICIARIES)

| Tác nhân (Actor) | Vai trò thực tế | Nhu cầu chính (Core Need) | Giá trị nhận được (Value Delivered) |
| :--- | :--- | :--- | :--- |
| Doanh nghiệp / Nhà nghiên cứu | Đơn vị sở hữu công nghệ | Đăng tải, quảng bá và tìm kiếm đối tác chuyển giao công nghệ | Tiếp cận thị trường nhanh, bảo vệ quyền sở hữu |
| Doanh nghiệp có nhu cầu | Đơn vị tìm kiếm công nghệ | Tìm kiếm công nghệ theo ngành, mức TRL; kết nối chuyên gia | Tiếp cận giải pháp phù hợp, có tư vấn chuyên sâu |
| Chuyên gia công nghệ | Cung cấp tri thức tư vấn | Đăng ký hồ sơ, chia sẻ kiến thức, nhận lịch tư vấn | Mở rộng mạng lưới, nâng cao uy tín chuyên môn |
| Học viên / Cán bộ kỹ thuật | Người học | Tham gia các khóa đào tạo trực tuyến, cấp chứng nhận | Nâng cao năng lực làm chủ công nghệ |
| Quản trị viên hệ thống | Vận hành nền tảng | Phân quyền RBAC, kiểm duyệt nội dung, quản lý kho dữ liệu | Kiểm soát chất lượng thông tin, vận hành an toàn |

---

## 4. PHẠM VI DỰ KIẾN (SCOPE BOUNDARIES)

### 4.1. Trong phạm vi (In-Scope)
- [Module Kho dữ liệu công nghệ: Quản lý sản phẩm, phân loại TRL, phân loại ngành kinh tế VN, tìm kiếm nâng cao]
- [Module Đào tạo trực tuyến: Quản lý khóa học, bài giảng video/tài liệu, tiến độ học viên]
- [Module Kết nối chuyên gia: Hồ sơ chuyên gia, đặt lịch tư vấn, đánh giá]
- [Module Quản trị & Phân quyền: RBAC TracePro, xác thực, báo cáo thống kê]

### 4.2. Ngoài phạm vi (Out-of-Scope)
- [Liệt kê rõ những tính năng chưa làm trong giai đoạn này để tránh Scope Creep]

### 4.3. Giả định & Ràng buộc (Assumptions & Constraints)
- **Giả định**: [Dữ liệu sản phẩm công nghệ ban đầu được các đơn vị cung cấp theo biểu mẫu chuẩn]
- **Ràng buộc công nghệ**: [Nền tảng Cloud, hạ tầng cơ sở dữ liệu, giao diện Responsive Web/Mobile]
- **Ràng buộc pháp lý**: [Tuân thủ quy định về sở hữu trí tuệ và an toàn thông tin mạng]

---

## 5. KIẾN TRÚC VÀ ĐẶC TẢ KỸ THUẬT NỀN TẢNG (PLATFORM ARCHITECTURE & TECH SPECS)

- **Giao diện người dùng**: Web Portal (Responsive) & Mobile App
- **Kiến trúc Backend**: RESTful API / GraphQL, microservices hoặc monolithic modular
- **Cơ sở dữ liệu**: Database quan hệ (PostgreSQL/MySQL) kết hợp Search Engine (Elasticsearch) cho kho dữ liệu
- **Lưu trữ đa phương tiện**: Object Storage (S3/MinIO) cho tài liệu nghiên cứu và video đào tạo

---

## 6. MA TRẬN TIÊU CHÍ THÀNH CÔNG (SUCCESS METRICS & ACCEPTANCE CRITERIA)

| Mã tiêu chí | Chỉ số đo lường (KPI / Metric) | Ngưỡng chấp nhận (Acceptance Threshold) | Phương thức đo lường |
| :--- | :--- | :--- | :--- |
| **KPI-01** | Thời gian phản hồi tìm kiếm công nghệ | $\le 500$ ms với dữ liệu lớn | Load test / APM monitor |
| **KPI-02** | Tải đồng thời trên hệ thống đào tạo | Chịu tải $\ge 1.000$ học viên trực tuyến | Kịch bản stress test |
| **KPI-03** | Tính chuẩn hóa của kho dữ liệu | 100% sản phẩm có thông tin ngành & TRL | Đối soát dữ liệu kho công nghệ |

---

## 7. BƯỚC TIẾP THEO (NEXT STEPS)
- [ ] Chốt toàn bộ nội dung Project Brief với Product Owner (`[CONFIRMED]`).
- [ ] Khởi tạo dự thảo SRS 7 mục bám theo [`TEMPLATE-SRS-7-muc.md`](../templates/TEMPLATE-SRS-7-muc.md).
- [ ] Bắt đầu thảo luận Mục 1 bằng `$ba-srs-copilot`.
