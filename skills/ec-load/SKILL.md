---
name: ec-load
description: "Chuyên gia Kiểm thử Tải & Hiệu năng (Load & Performance Testing Specialist): Thiết kế và thực thi kịch bản đo lường chịu tải (k6 / autocannon / wrk), tính toán throughput (RPS), độ trễ p95/p99, phát hiện rò rỉ tài nguyên và xác định điểm sập (Break Point) của hệ thống."
---

# Kỹ Năng: ec-load (Kiểm Thử Tải, Sức Chịu Đựng & Hiệu Năng)

> **Role Chịu Trách Nhiệm**: EC Agent (`ec`) — Edge-Case Hunter & QC Specialist.  
> **Cổng Kiểm Soát**: Gate 4 Performance & Scalability Gatekeeper.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: 
  - Kịch bản tải mục tiêu: `tests/load/scenarios/` (k6, autocannon, hoặc công cụ tương đương).
  - Ngưỡng SLA yêu cầu: Latency p95 < 200ms, p99 < 500ms, Error rate < 1%, RPS tối thiểu theo thiết kế.
- **Target Output File**: `tests/load/LOAD_TEST_REPORT.md` (hoặc `docs/decisions/LOAD_TEST_REPORT.md`)
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. 4 MÔ HÌNH KIỂM THỬ TẢI TIÊU CHUẨN

```
Tải (RPS)
 ^
 |          /-------------\ (Stress)
 |         /               \
 |  /-----\ (Load Test)     \            /---\ (Spike)
 | /       \                 \          /     \
 +-----------------------------------------------> Thời gian
```

1. **Load Test (Tải Tiêu Chuẩn)**:
   - Duy trì tải tương đương 100% dung lượng thiết kế trong 10–30 phút.
   - Mục tiêu: Kiểm tra hệ thống duy trì ổn định không rò rỉ RAM/CPU, p95 latency đạt chuẩn SLA.
2. **Stress Test (Tải Cực Hạn & Tìm Break Point)**:
   - Tăng dần traffic (Ramping VUs) lên 200% -> 300% -> 500% cho đến khi hệ thống bắt đầu nghẽn, sập kết nối hoặc trả lỗi 5xx.
   - Mục tiêu: Xác định chính xác "Điểm sập" (Break Point) và kiểm tra hệ thống có tự hồi phục khi giảm tải không.
3. **Spike Test (Tải Tăng Đột Biến)**:
   - Giả lập traffic tăng vọt đột ngột gấp 5–10 lần trong vài giây (ví dụ: mở bán vé / flash sale / push thông báo hàng loạt).
   - Mục tiêu: Kiểm tra cơ chế Rate Limiting, Autoscaling và khả năng đệm hàng đợi (Queue buffering).
4. **Soak Test (Kiểm Tra Độ Bền / Tải Kéo Dài)**:
   - Duy trì tải vừa phải liên tục trong thời gian dài (vài giờ đến 24h).
   - Mục tiêu: Phát hiện rò rỉ bộ nhớ (Memory Leaks), tràn kết nối DB Connection Pool, hoặc phân mảnh cache.

---

## 3. CẤU TRÚC BÁO CÁO LOAD_TEST_REPORT.MD

```markdown
# BÁO CÁO KIỂM THỬ TẢI & HIỆU NĂNG (PERFORMANCE & LOAD REPORT)

- **Thời gian thực hiện**: [YYYY-MM-DD HH:mm]
- **Kịch bản**: [Smoke / Load / Stress / Spike]
- **Target Endpoints**: [Danh sách APIs]

## 1. BẢNG CHỈ SỐ TẢI CHÍNH (METRICS SUMMARY)
| Chỉ Số | Mục Tiêu (SLA) | Kết Quả Đạt Được | Đánh Giá |
| :--- | :---: | :---: | :---: |
| **Max Concurrent Users (VUs)** | 500 | 500 | [PASS] |
| **Throughput (Requests/sec)** | > 1,000 RPS | 1,240 RPS | [PASS] |
| **Latency p50 (Median)** | < 50ms | 28ms | [PASS] |
| **Latency p95** | < 200ms | 115ms | [PASS] |
| **Latency p99** | < 500ms | 240ms | [PASS] |
| **Error Rate (HTTP 5xx / Timeouts)** | < 0.5% | 0.02% | [PASS] |

## 2. PHÁT HIỆN NGHẼN CỔ CHAI (BOTTLENECK ANALYSIS)
- CSDL Connection Pool: Max 50 connections, đạt đỉnh 38/50.
- Cache Hit Ratio: Đạt > 90%.
- CPU/RAM Service: Ổn định, không có hiện tượng rò rỉ bộ nhớ.
```
