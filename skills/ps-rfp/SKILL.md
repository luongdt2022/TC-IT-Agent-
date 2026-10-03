---
name: ps-rfp
description: "Thẩm định hồ sơ yêu cầu thầu (RFP/RFI), đánh giá tính khả thi kỹ thuật, rủi ro pháp lý và an toàn thông tin trước khi quyết định nhận dự án."
---

# Kỹ Năng: ps-rfp (Thẩm Định Hồ Sơ Mời Thầu & Tính Khả Thi)

> **Role Chịu Trách Nhiệm**: PS Agent (`ps`) — Presale & IT Solution Consultant.  
> **Cổng Kiểm Soát**: Pre-Project Go/No-Go Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Hồ sơ mời thầu (RFP/RFI) dạng tệp văn bản hoặc mô tả bài toán từ khách hàng.
- **Target Output File**: `docs/00-presale-proposal/FEASIBILITY_REPORT.md`
- **NGHIÊM CẤM**: Không ghi file ra ngoài thư mục `docs/00-presale-proposal/`.

---

## 2. NỘI DUNG THẨM ĐỊNH TÍNH KHẢ THI (FEASIBILITY CHECKLIST)

Báo cáo `FEASIBILITY_REPORT.md` bao gồm 5 khía cạnh thẩm định bắt buộc:

1. **Thẩm Định Khả Thi Kỹ Thuật (Technical Feasibility)**:
   - Các công nghệ yêu cầu trong RFP có nằm trong năng lực cốt lõi của team không?
   - Có yêu cầu tích hợp với hệ thống cũ (Legacy) hoặc thiết bị ngoại vi không có tài liệu API chuẩn không?
   - Yêu cầu về hiệu năng (SLA, Response time, Uptime 99.99%) có khả thi với ngân sách dự kiến không?
2. **Thẩm Định Khả Thi Thời Gian (Schedule Feasibility)**:
   - Thời hạn bàn giao khách hàng yêu cầu có phi thực tế không?
   - Cần tối thiểu bao nhiêu sprint để hoàn thiện phiên bản tối thiểu (MVP)?
3. **Thẩm Định Rủi Ro & Ràng Buộc Pháp Lý / Bảo Mật (Compliance & Security)**:
   - Các tiêu chuẩn tuân thủ bắt buộc: PCI-DSS, GDPR, HIPAA, Luật An ninh mạng Việt Nam...
   - Yêu cầu lưu trữ dữ liệu tại chỗ (On-Premise / Local Datacenter) hay được dùng Cloud quốc tế?
4. **Đánh Giá Khoảng Trống Yêu Cầu (RFP Gap Analysis)**:
   - Liệt kê tối thiểu 5 - 10 câu hỏi làm rõ (Clarification Questions) cần gửi lại cho bên mời thầu trước khi nộp hồ sơ.
5. **Quyết Định Kiến Nghị (Go / No-Go Decision)**:
   - `[GO]`: Đạt điều kiện triển khai, chuyển sang `ps-proposal` và `ps-estimate`.
   - `[GO WITH CONDITIONS]`: Cần đàm phán lại về phạm vi hoặc thời gian trước khi ký.
   - `[NO-GO]`: Từ chối thầu do rủi ro vượt quá mức kiểm soát hoặc phi khả thi kỹ thuật.
