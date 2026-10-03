---
name: ps-proposal
description: "Soạn thảo hồ sơ đề xuất giải pháp kỹ thuật tổng thể (IT Technical Proposal) chuyên nghiệp cho C-Level / Khách hàng từ đề bài thô hoặc hồ sơ mời thầu (RFP)."
---

# Kỹ Năng: ps-proposal (Soạn Thảo IT Technical Proposal)

> **Role Chịu Trách Nhiệm**: PS Agent (`ps`) — Presale & IT Solution Consultant.  
> **Cổng Kiểm Soát**: Pre-Project Gate (Trước khi ký duyệt hợp đồng/dự án).

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Đề bài thô của khách hàng, biên bản trao đổi sơ bộ, hoặc hồ sơ mời thầu RFP/RFI.
- **Target Output File**: `docs/00-presale-proposal/PROPOSAL.md`
- **Tài liệu bổ trợ đính kèm**:
  - `docs/00-presale-proposal/EXECUTIVE_SUMMARY.md` (Dành riêng cho Giám đốc / C-Level)
- **NGHIÊM CẤM**: Tuyệt đối không ghi file ra thư mục gốc (`root`) hay các thư mục khác ngoài `docs/00-presale-proposal/`.

---

## 2. CẤU TRÚC CHUẨN CỦA TÀI LIỆU PROPOSAL.md

Tài liệu `docs/00-presale-proposal/PROPOSAL.md` phải tuân thủ nghiêm ngặt 7 phần chuẩn doanh nghiệp:

1. **Executive Summary (Tóm lược điều hành)**:
   - Bài toán cốt lõi của khách hàng & Bối cảnh thị trường.
   - Tuyên ngôn giá trị (Value Proposition) & Kết quả định lượng kỳ vọng (KPI/ROI).
2. **System Architecture Blueprint (Bản vẽ kiến trúc đề xuất)**:
   - Sơ đồ kiến trúc tổng thể cấp cao (High-Level C4 Context Diagram bằng Mermaid).
   - Danh sách công nghệ (Tech Stack) đề xuất & Lý do lựa chọn (Performance, Scale, Cost, Security).
3. **Core Functional Modules (Phân rã các phân hệ chức năng chính)**:
   - Danh mục module chức năng (WBS cấp 1 và cấp 2).
   - Trải nghiệm người dùng cốt lõi (User Journey Flow).
4. **Non-Functional Requirements & Security (Yêu cầu phi chức năng & Bảo mật)**:
   - Tiêu chuẩn chịu tải (Concurrent Users, TPS, Response Time < 200ms).
   - An toàn thông tin: Chuẩn mã hóa dữ liệu (AES-256, TLS 1.3), phân quyền Scoped RBAC, Audit Logging.
5. **Implementation Timeline & Roadmap (Lộ trình triển khai)**:
   - Phân kỳ dự án: MVP (Giai đoạn 1) ➔ V1.0 (Giai đoạn 2) ➔ Mở rộng (Giai đoạn 3).
   - Các mốc Milestone nghiệm thu bàn giao chính.
6. **Cost & Investment Summary (Tổng quan chi phí & Báo giá sơ bộ)**:
   - Dẫn chiếu sang `ESTIMATION_AND_COST.md` (Chi phí phát triển theo Man-Month + Chi phí hạ tầng Cloud hàng tháng).
7. **Risk Assessment & Mitigation (Đánh giá rủi ro kỹ thuật & Giải pháp phòng ngừa)**:
   - Nhận diện các điểm rủi ro nghẽn cổ chai và cam kết SLA hệ thống.

---

## 3. CÁC BƯỚC THỰC THI (STEP-BY-STEP WORKFLOW)

1. **Khảo sát & Phân tích Đề bài**:
   - Đọc kỹ thông tin đề bài từ người dùng hoặc tệp RFP.
   - Nhận diện 3 yếu tố cốt lõi: Ngân sách ước lượng, Thời hạn bàn giao mong muốn, và Khối lượng tính năng then chốt.
2. **Lựa chọn Phương án Kiến trúc**:
   - Tham khảo và kích hoạt `ps-solution` để cân nhắc các phương án kiến trúc phù hợp.
3. **Khởi tạo Thư mục & Soạn thảo**:
   - Đảm bảo thư mục `docs/00-presale-proposal/` đã tồn tại.
   - Viết tệp `docs/00-presale-proposal/PROPOSAL.md` theo cấu trúc 7 phần trên.
   - Tóm lược bản rút gọn `docs/00-presale-proposal/EXECUTIVE_SUMMARY.md` (tối đa 2 trang A4) làm tài liệu thuyết trình nhanh.
4. **Bàn giao**:
   - Trình bày cho người dùng hoặc Ban Giám đốc xem xét trước khi chuyển sang khâu tính toán chi phí chi tiết (`ps-estimate`).
