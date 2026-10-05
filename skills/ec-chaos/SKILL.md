---
name: ec-chaos
description: "Chuyên gia Kiểm thử Hỗn loạn & Khả năng Phục hồi (Chaos & Resilience Specialist): Cố tình bơm lỗi vào hệ thống (gián đoạn Redis/Cache, drop connection CSDL, ngắt mạng background worker, inject độ trễ cao) để chứng minh tính năng tự hồi phục (Self-healing), Circuit Breaker và Graceful Degradation."
---

# Kỹ Năng: ec-chaos (Kiểm Thử Hỗn Loạn & Khả Năng Phục Hồi)

> **Role Chịu Trách Nhiệm**: EC Agent (`ec`) — Edge-Case Hunter & QC Specialist.  
> **Cổng Kiểm Soát**: Gate 4 Resilience & Fault-Tolerance Gatekeeper.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Hệ thống phân tán hoặc dịch vụ hạ tầng (CSDL, Cache/Queue, Background Workers, External APIs).
- **Target Output File**: `tests/chaos/CHAOS_EXPERIMENT_REPORT.md` (hoặc `docs/decisions/CHAOS_EXPERIMENT_REPORT.md`)
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. 5 KỊCH BẢN BƠM LỖI HỖN LOẠN (CHAOS FAULT INJECTION SCENARIOS)

```
[ Client / WebApp ] ---> [ Backend API ] --x (Cắt đứt CSDL / Cache / Queue) x--> [ Hạ Tầng Phụ Thuộc ]
                               |
                               +---> [ Cơ chế Fallback / Circuit Breaker / Graceful UX ]
```

1. **Rớt Kết Nối CSDL (Database Cutoff / Reconnect Test)**:
   - Tạm ngắt kết nối CSDL (PostgreSQL, MySQL, SQL Server...) trong 15 giây khi hệ thống đang xử lý request.
   - Kỳ vọng: API không bị crash process; trả mã lỗi 503 kèm thông báo thân thiện; tự động kết nối lại khi CSDL hoạt động trở lại mà không cần khởi động lại container/service.
2. **Sập Bộ Đệm Cache / Queue (Redis & Message Broker Failure)**:
   - Đột ngột ngắt kết nối Cache/Queue (Redis, RabbitMQ, Kafka...).
   - Kỳ vọng: Hệ thống chuyển sang chế độ Graceful Degradation (đọc trực tiếp CSDL với rate limit, hoặc lưu tạm job vào fallback file/queue), không làm chết tiến trình chính.
3. **Dịch Vụ Bên Ngoài / Worker Bị Treo Hoặc Quá Tải (Third-party / Worker Timeout)**:
   - Mô phỏng dịch vụ bên ngoài (Payment Gateway, AI LLM, SMTP, SMS...) phản hồi chậm > 30 giây hoặc trả về lỗi 5xx.
   - Kỳ vọng: Backend kích hoạt Circuit Breaker, timeout quy định, giải phóng thread/connection pool và trả thông báo lỗi phù hợp cho client.
4. **Độ Trễ Mạng Cực Cao (High Network Latency Injection)**:
   - Bơm độ trễ ngẫu nhiên 3,000ms – 8,000ms vào kết nối mạng giữa Frontend và Backend.
   - Kỳ vọng: Frontend không bị đơ trình duyệt; hiển thị spinner/skeleton hoặc trạng thái Updating đúng chuẩn UI UX.
5. **Đột Ngột Tắt Tiến Trình (Process Kill & Orphan Transaction)**:
   - Giả lập crash tiến trình worker đang xử lý transaction/job dang dở.
   - Kỳ vọng: Không sinh ra dữ liệu rác mồ côi (Orphan Records), transaction trong CSDL được rollback hoàn toàn, job được retry theo idempotent policy.

---

## 3. CẤU TRÚC BÁO CÁO CHAOS_EXPERIMENT_REPORT.MD

```markdown
# BÁO CÁO THỰC NGHIỆM HỖN LOẠN (CHAOS EXPERIMENT REPORT)

- **Thời gian**: [YYYY-MM-DD HH:mm]
- **Kiểm định viên**: EC Agent

## 1. KẾT QUẢ THỰC NGHIỆM
| Thí Nghiệm Lỗi | Đối Tượng Tác Động | Hành Vi Thực Tế | Tự Hồi Phục | Đánh Giá |
| :--- | :--- | :--- | :---: | :---: |
| **Drop DB Connection** | Primary Database | Trả 503, tự reconnect sau 3s | Có | [PASS] |
| **Kill Worker** | Background Job Worker | Job được re-queue và thực thi lại | Có | [PASS] |
| **Downstream Timeout** | External Provider | Circuit Breaker trip, trả fallback | Có | [PASS] |

## 2. PHÁT HIỆN RỦI RO & KHẮC PHỤC
- Ghi nhận thời gian hồi phục (MTTR - Mean Time To Recovery).
- Đề xuất tăng timeout hoặc cấu hình fallback nếu service bị treo process.
```
