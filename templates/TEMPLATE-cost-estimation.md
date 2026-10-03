# DỰ TOÁN KHỐI LƯỢNG & CHI PHÍ DỰ ÁN (PROJECT ESTIMATION & COSTING)

*Dự án: `{{PROJECT_NAME}}` | Khách hàng: `{{CLIENT_NAME}}` | Ngày lập: `{{DATE}}`*  
*Quy đổi chuẩn: `1 Man-Month (MM) = 22 Man-Days (MD) = 176 Giờ làm việc`*

---

## 1. BẢNG BÓC TÁCH KHỐI LƯỢNG THEO PHÂN HỆ (WBS EFFORT BREAKDOWN)

| Mã Module | Tính Năng / Công Việc Cụ Thể | Độ Phức Tạp | BA (MD) | SA (MD) | BE (MD) | FE (MD) | QC (MD) | Tổng MD | Ghi Chú Rủi Ro |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **MOD-01** | Quản trị Định danh, Phân quyền RBAC | M | 2 | 2 | 5 | 4 | 3 | **16** | Tích hợp OAuth2/JWT |
| **MOD-02** | [Tên phân hệ nghiệp vụ chính 1] | L | 4 | 3 | 10 | 8 | 5 | **30** | Luồng nghiệp vụ cốt lõi |
| **MOD-03** | [Tên phân hệ nghiệp vụ chính 2] | M | 3 | 2 | 7 | 6 | 4 | **22** | Xử lý dữ liệu bảng lớn |
| **MOD-04** | Bảng điều khiển & Báo cáo thống kê | M | 2 | 1 | 4 | 5 | 3 | **15** | Tối ưu truy vấn đọc |
| **MOD-05** | Tích hợp Cổng thanh toán & Notification| M | 2 | 2 | 5 | 3 | 3 | **15** | Phụ thuộc bên thứ ba |
| **HỆ THỐNG** | CI/CD, Docker, Setup Kiến trúc ban đầu | M | 0 | 4 | 3 | 2 | 2 | **11** | Triển khai hạ tầng |
| **TỔNG NỖ LỰC CHƯA BUFFER** | | | **13** | **14** | **34** | **28** | **20** | **109 MD** | (~ 5.0 Man-Month) |
| **BUFFER DỰ PHÒNG RỦI RO (+20%)** | | | 2.5 | 2.5 | 7 | 5.5 | 4 | **21.5 MD** | (~ 1.0 Man-Month) |
| **TỔNG CỘNG TOÀN DỰ ÁN** | | | **15.5**| **16.5**| **41** | **33.5**| **24** | **130.5 MD**| **~ 6.0 Man-Month** |

---

## 2. DỰ TOÁN CHI PHÍ PHÁT TRIỂN THEO VAI TRÒ (DEVELOPMENT COST)

| Vai Trò Chuyên Môn | Nỗ Lực (Man-Month) | Đơn Giá / Tháng (VND) | Thành Tiền (VND) | Tỷ Trọng (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Senior BA** | 0.70 MM | [Đơn giá BA] | [Thành tiền] | 12% |
| **Software Architect / Tech Lead** | 0.75 MM | [Đơn giá SA] | [Thành tiền] | 13% |
| **Senior Backend Developer** | 1.85 MM | [Đơn giá BE] | [Thành tiền] | 31% |
| **Senior Frontend / Mobile Dev** | 1.50 MM | [Đơn giá FE] | [Thành tiền] | 26% |
| **EC / QC Automation Specialist** | 1.10 MM | [Đơn giá QC] | [Thành tiền] | 18% |
| **TỔNG CHI PHÍ PHÁT TRIỂN (Chưa VAT)**| **5.90 MM** | | **[TỔNG TIỀN PHÁT TRIỂN]** | **100%** |

---

## 3. DỰ TOÁN CHI PHÍ HẠ TẦNG CLOUD & VẬN HÀNH (CLOUD INFRASTRUCTURE TCO)

| Dịch Vụ / Tài Nguyên | Cấu Hình Kỹ Thuật Dự Kiến | Đơn Vị | Chi Phí / Tháng (USD) | Chi Phí / Năm (USD) |
| :--- | :--- | :---: | :---: | :---: |
| **Compute (App Server)** | 2x Node (4 vCPU, 16GB RAM) Auto-scaling | 2 nodes | ~$120 | ~$1,440 |
| **Database (Managed Postgres)** | Primary + Standby Multi-AZ (2 vCPU, 8GB RAM, 100GB SSD) | 1 cluster | ~$150 | ~$1,800 |
| **Cache (Redis Cluster)** | 1 Node (2 vCPU, 4GB RAM) | 1 node | ~$45 | ~$540 |
| **Storage & CDN** | S3 200GB Storage + CloudFront 500GB Egress | Dung lượng | ~$25 | ~$300 |
| **DevOps, Security & Backup** | WAF, Automated Snapshot, SSL, CI/CD runner | Dịch vụ | ~$60 | ~$720 |
| **TỔNG CHI PHÍ HẠ TẦNG (Ước tính)** | | | **~$400 / tháng** | **~$4,800 / năm** |

---

## 4. CÁC GÓI ĐẦU TƯ ĐỀ XUẤT (PACKAGING OPTIONS)

1. **Gói MVP Tối Thiểu (Phát triển 2 tháng)**:
   - Phạm vi: MOD-01 + MOD-02 cốt lõi.
   - Nỗ lực: ~3.0 Man-Month.
   - Phù hợp: Thử nghiệm thị trường nhanh, chi phí tiết kiệm.
2. **Gói Tiêu Chuẩn Doanh Nghiệp (Phát triển 3.5 tháng - KHUYÊN DÙNG)**:
   - Phạm vi: Toàn bộ 5 Modules + Kiểm thử 3 tầng đầy đủ.
   - Nỗ lực: ~6.0 Man-Month.
   - Phù hợp: Hệ thống vận hành chính thức, sẵn sàng chịu tải lớn.
3. **Gói Mở Rộng Cao Cấp (Phát triển 5 tháng)**:
   - Phạm vi: Toàn bộ hệ thống + AI tích hợp + Multi-region High Availability.
   - Nỗ lực: ~9.0 Man-Month.
