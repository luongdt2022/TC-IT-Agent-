---
name: ps-solution
description: "Phân tích, so sánh các phương án giải pháp kiến trúc (Trade-off Analysis), đánh giá ưu/nhược điểm (Chi phí vs Hiệu năng vs Thời gian) phục vụ báo cáo Giám đốc hoặc thuyết phục khách hàng."
---

# Kỹ Năng: ps-solution (So Sánh & Phân Tích Trade-off Giải Pháp)

> **Role Chịu Trách Nhiệm**: PS Agent (`ps`) — Presale & IT Solution Consultant.  
> **Cổng Kiểm Soát**: Pre-Project Architectural Evaluation.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Đề bài bài toán kỹ thuật hoặc yêu cầu từ Giám đốc / Khách hàng.
- **Target Output File**: `docs/00-presale-proposal/SOLUTION_COMPARISON.md`
- **NGHIÊM CẤM**: Không ghi file ra ngoài thư mục `docs/00-presale-proposal/`.

---

## 2. NỘI DUNG PHÂN TÍCH SO SÁNH GIẢI PHÁP

Tài liệu `SOLUTION_COMPARISON.md` luôn đưa ra **tối thiểu 2 đến 3 phương án kiến trúc** để người ra quyết định lựa chọn:

### Phương Án A: "Lean & Fast" (Tối Ưu Thời Gian & Chi Phí Ban Đầu)
- **Kiến trúc**: Modular Monolith, Serverless hoặc BaaS.
- **Ưu điểm**: Triển khai thần tốc (Time-to-market ngắn), chi phí vận hành ban đầu thấp, đội ngũ dev nhỏ gọn.
- **Đánh đổi (Trade-off)**: Giới hạn chịu tải cực đại, cần tái cấu trúc khi người dùng tăng đột biến.

### Phương Án B: "Scalable Enterprise" (Cân Bằng Giữa Quy Mô & Độ Ổn Định)
- **Kiến trúc**: Clean Architecture phân tầng rõ rệt, Microservices nhẹ theo Bounded Contexts, Event-Driven (Kafka/RabbitMQ), Containerization (Docker/K8s).
- **Ưu điểm**: Khả năng chịu tải cao, mở rộng độc lập từng module, độ tin cậy và an ninh chuẩn doanh nghiệp.
- **Đánh đổi (Trade-off)**: Chi phí phát triển và hạ tầng cao hơn, độ phức tạp quản trị DevOps lớn hơn.

### Phương Án C: "High-Tech / AI Native" (Nếu bài toán đòi hỏi)
- **Kiến trúc**: Tích hợp mô hình AI/ML, Vector DB, RAG pipeline, Real-time streaming.

---

## 3. MA TRẬN CHẤM ĐIỂM GIẢI PHÁP (DECISION MATRIX)

Bắt buộc có bảng ma trận chấm điểm theo thang điểm 1 - 5:

| Tiêu Chí Đánh Giá | Trọng Số (%) | Phương Án A (Lean) | Phương Án B (Enterprise) | Phương Án C |
| :--- | :---: | :---: | :---: | :---: |
| 1. Thời gian triển khai (Time to Market) | 20% | 5/5 | 3/5 | 2/5 |
| 2. Chi phí đầu tư ban đầu (CapEx) | 25% | 5/5 | 3/5 | 2/5 |
| 3. Chi phí vận hành định kỳ (OpEx) | 15% | 4/5 | 3/5 | 2/5 |
| 4. Khả năng mở rộng & Chịu tải | 20% | 2/5 | 5/5 | 5/5 |
| 5. Mức độ an toàn bảo mật & Tuân thủ | 20% | 3/5 | 5/5 | 5/5 |
| **TỔNG ĐIỂM CÓ TRỌNG SỐ** | **100%** | **Điểm A** | **Điểm B** | **Điểm C** |

---

## 4. KẾT LUẬN & ĐỀ XUẤT CỦA CHUYÊN GIA
- Đưa ra khuyến nghị dứt khoát: *Tại sao Giám đốc / Khách hàng nên chọn phương án nào ở thời điểm hiện tại và lộ trình chuyển đổi (Migration Path) khi doanh nghiệp phát triển.*
