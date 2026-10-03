# QUY TRÌNH TIỀN DỰ ÁN: wf-presale (TỪ ĐỀ BÀI ĐẾN IT PROPOSAL & BÁO GIÁ)

> **Mã Quy Trình**: `wf-presale`  
> **Tác Tử Chủ Trì**: **PS Agent (`ps`)** — Presale & IT Solution Consultant  
> **Tác Tử Phối Hợp**: **TL/SA Agent (`techlead-sa`)**  
> **Cổng Kết Thúc**: Pre-Project Go/No-Go Gate & Hợp Đồng Ký Duyệt

---

## 1. MỤC TIÊU CỐT LÕI
Chuyển hóa đề bài sơ bộ, ý tưởng kinh doanh hoặc hồ sơ mời thầu (RFP/RFI) của khách hàng thành:
1. Hồ sơ đề xuất giải pháp kỹ thuật tổng thể (**IT Technical Proposal**).
2. Bảng bóc tách khối lượng công việc (**WBS**) và dự toán chi phí theo **Man-Month**.
3. Bảng dự toán chi phí vận hành hạ tầng Cloud hàng tháng & 3 năm (**TCO**).
4. Bản tóm lược giải pháp dành cho Giám đốc / C-Level (**Executive Summary**).

---

## 2. BẢNG ĐIỀU HƯỚNG TỆP TIN ĐẦU RA (ENFORCED DIRECTORY CONTRACT)
Tất cả các tài liệu trong quy trình này BẮT BUỘC lưu tại:
- `docs/00-presale-proposal/PROPOSAL.md` (Hồ sơ đề xuất giải pháp kỹ thuật)
- `docs/00-presale-proposal/ESTIMATION_AND_COST.md` (Dự toán chi phí & Man-Month)
- `docs/00-presale-proposal/SOLUTION_COMPARISON.md` (Bảng so sánh Trade-off)
- `docs/00-presale-proposal/EXECUTIVE_SUMMARY.md` (Tóm lược cho C-Level)
- `docs/00-presale-proposal/FEASIBILITY_REPORT.md` (Báo cáo thẩm định tính khả thi)

---

## 3. CÁC BƯỚC THỰC THI TUẦN TỰ (STAGE-GATE FLOW)

### Bước 1: Tiếp Nhận & Thẩm Định Tính Khả Thi [PS Agent]
- **Kỹ năng sử dụng**: `ps-rfp`
- **Hành động**: Đọc hiểu đề bài, rà soát 5 yếu tố khả thi (Công nghệ, Thời gian, Bảo mật, Ngân sách, Tuân thủ).
- **Đầu ra**: `docs/00-presale-proposal/FEASIBILITY_REPORT.md` với phán quyết `[GO]` hoặc `[NO-GO]`.

### Bước 2: So Sánh Phương Án Kiến Trúc [PS Agent + TL/SA Agent]
- **Kỹ năng sử dụng**: `ps-solution`
- **Hành động**: Đưa ra tối thiểu 2 phương án: Phương án Lean (Tối ưu chi phí/thời gian) vs Phương án Enterprise (Khả năng mở rộng cao). SA Agent hỗ trợ đánh giá Trade-off kỹ thuật.
- **Đầu ra**: `docs/00-presale-proposal/SOLUTION_COMPARISON.md`.

### Bước 3: Bóc Tách Khối Lượng & Dự Toán Chi Phí [PS Agent]
- **Kỹ năng sử dụng**: `ps-estimate`
- **Hành động**: Lập ma trận WBS phân bổ theo Man-Month cho từng vai trò (BA, SA, BE, FE, QC). Tính toán chi phí Cloud AWS/GCP/Azure.
- **Đầu ra**: `docs/00-presale-proposal/ESTIMATION_AND_COST.md`.

### Bước 4: Soạn Thảo IT Technical Proposal [PS Agent]
- **Kỹ năng sử dụng**: `ps-proposal`
- **Hành động**: Tổng hợp hoàn chỉnh hồ sơ giải pháp 7 phần chuẩn mực.
- **Đầu ra**: `docs/00-presale-proposal/PROPOSAL.md` và `docs/00-presale-proposal/EXECUTIVE_SUMMARY.md`.

### Bước 5: Thuyết Trình & Bàn Giao Hợp Đồng [PS Agent ➔ PO/PM Agent]
- **Hành động**: Trình bày cho Giám đốc/Khách hàng phê duyệt. Khi hợp đồng được chốt, PS Agent bàn giao toàn bộ hồ sơ cho PO/PM Agent để kích hoạt quy trình khởi động dự án chính thức (`wf-kickoff`).
