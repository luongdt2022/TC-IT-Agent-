---
name: ps-estimate
description: "Bóc tách khối lượng công việc (WBS), tính toán nhân sự (Man-Month/Man-Day), dự toán chi phí phát triển và TCO hạ tầng Cloud (AWS/GCP/Azure) cho dự án IT."
---

# Kỹ Năng: ps-estimate (Bóc Tách Khối Lượng & Dự Toán Chi Phí)

> **Role Chịu Trách Nhiệm**: PS Agent (`ps`) — Presale & IT Solution Consultant.  
> **Cổng Kiểm Soát**: Pre-Project Financial Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Danh mục tính năng sơ bộ từ đề bài hoặc `docs/00-presale-proposal/PROPOSAL.md`.
- **Target Output File**: `docs/00-presale-proposal/ESTIMATION_AND_COST.md`
- **NGHIÊM CẤM**: Không ghi file ra ngoài thư mục `docs/00-presale-proposal/`.

---

## 2. NGUYÊN TẮC TÍNH TOÁN DỰ TOÁN (ESTIMATION RULES)

1. **Công thức Man-Month chuẩn**:
   $$1 \text{ Man-Month (MM)} = 22 \text{ Man-Days (MD)} = 176 \text{ Giờ làm việc tiêu chuẩn}$$
2. **Hệ số rủi ro & Buffer**:
   - Dự án công nghệ quen thuộc (CRUD, Monolith chuẩn): Thêm 15% buffer.
   - Dự án tích hợp hệ thống phức tạp / Third-party / Real-time: Thêm 25% buffer.
   - Dự án có AI / BigData / High-concurrency: Thêm 35% buffer.
3. **Phân bổ nỗ lực theo vai trò (Effort Breakdown Standard)**:
   - **BA (Nghiệp vụ)**: 12% - 15% tổng nỗ lực.
   - **SA / Tech Lead (Kiến trúc & Review)**: 10% - 15% tổng nỗ lực.
   - **Backend Dev**: 30% - 35% tổng nỗ lực.
   - **Frontend / Mobile Dev**: 25% - 30% tổng nỗ lực.
   - **EC / QC (Kiểm thử & Automation)**: 15% - 20% tổng nỗ lực.
   - **PM / PO**: 8% - 10% tổng nỗ lực.

---

## 3. CẤU TRÚC TÀI LIỆU ESTIMATION_AND_COST.md

Tài liệu bắt buộc gồm 5 bảng biểu chi tiết:

1. **Bảng Bóc Tách Khối Lượng (WBS & Effort Matrix)**:
   - Cột: Mã Module | Tính năng chi tiết | Độ phức tạp (S/M/L/XL) | BA (MD) | BE (MD) | FE (MD) | QC (MD) | Tổng MD | Ghi chú rủi ro.
2. **Bảng Cơ Cấu Nhân Sự Theo Tháng (Staffing Plan)**:
   - Lộ trình huy động nhân sự theo từng tháng của dự án.
3. **Bảng Dự Toán Chi Phí Phát Triển (Development Cost)**:
   - Tổng số Man-Month × Đơn giá theo vai trò.
4. **Bảng Chi Phí Hạ Tầng Cloud Hàng Tháng & Hàng Năm (Cloud Infrastructure TCO)**:
   - Compute (EC2, ECS, K8s, VM): vCPU, RAM, số lượng node.
   - Database (RDS Postgres, MongoDB Atlas): Instance size, Storage, Multi-AZ.
   - Storage & CDN (S3, CloudFront, GCS): Dung lượng lưu trữ, băng thông ra (Egress).
   - DevOps & Security (CI/CD runner, WAF, SSL, CloudWatch/Datadog).
   - Ước tính chi phí tháng đầu vs tháng cao điểm vs chi phí 3 năm (TCO).
5. **Đề Xuất Các Gói Triển Khai (Options Packaging)**:
   - Gói Tiết Kiệm (MVP Core)
   - Gói Tiêu Chuẩn (Full Functional)
   - Gói Doanh Nghiệp (High Availability, Multi-Region, 24/7 SLA).
