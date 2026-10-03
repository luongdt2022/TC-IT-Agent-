# QUY TRÌNH KHỞI ĐỘNG DỰ ÁN: wf-kickoff (TỪ BÀN GIAO ĐẾN BASIC DESIGN & ROADMAP)

> **Mã Quy Trình**: `wf-kickoff`  
> **Tác Tử Chủ Trì**: **PO/PM Agent (`po-pm`)** — Product Owner & Project Manager  
> **Tác Tử Phối Hợp**: **BA Agent (`ba`)**, **TL/SA Agent (`techlead-sa`)**  
> **Cổng Kết Thúc**: Gate 1 Backbone Architecture & Master Roadmap Sign-off

---

## 1. MỤC TIÊU CỐT LÕI
Chuyển giao ngữ cảnh từ khâu tiền dự án sang bộ máy thực thi:
1. Xác lập tầm nhìn sản phẩm, User Personas và Story Mapping.
2. Xây dựng tài liệu **Thiết Kế Cơ Sở (Basic Design - Kihon Sekkei)** làm khung xương sống định hướng.
3. Thiết lập sơ đồ kiến trúc tổng thể (C4 Level 1 & Level 2) và định hình khung xương mỏng (**Walking Skeleton**).
4. Khởi tạo **Master Roadmap (`backlog/ROADMAP.md`)** và phân rã các Milestone.

---

## 2. BẢNG ĐIỀU HƯỚNG TỆP TIN ĐẦU RA (ENFORCED DIRECTORY CONTRACT)
Tất cả các tài liệu trong quy trình này BẮT BUỘC lưu tại:
- `docs/01-basic-design/BD-00-overview.md` (Tầm nhìn, Story Mapping, Walking Skeleton)
- `docs/01-basic-design/BD-01-c4-context.md` (Sơ đồ C4 Context & Container)
- `docs/01-basic-design/BD-02-domain-model.md` (Domain Entities & Bounded Contexts)
- `backlog/ROADMAP.md` (Master Roadmap theo dõi tiến độ)
- `constitution.md` (Hiến pháp kỹ thuật dự án)

---

## 3. CÁC BƯỚC THỰC THI TUẦN TỰ (STAGE-GATE FLOW)

### Bước 1: Tiếp Nhận Bàn Giao & Thiết Lập Hiến Pháp Kỹ Thuật [PO/PM + TL/SA]
- **Kỹ năng sử dụng**: `po-scope` & `sa-design`
- **Hành động**: Tiếp nhận hồ sơ từ `docs/00-presale-proposal/PROPOSAL.md`. Sàng lọc phạm vi ban đầu và khởi tạo tệp hiến pháp kỹ thuật `constitution.md` quy định Tech Stack, Clean Architecture boundaries và quy tắc chống rác.

### Bước 2: Khơi Gợi Nghiệp Vụ Chuyên Sâu [BA Agent]
- **Kỹ năng sử dụng**: `ba-elicit`
- **Hành động**: Áp dụng 9 kỹ thuật khơi gợi nghiệp vụ (5 Whys, Laddering...) để làm rõ các điểm mơ hồ, bóc tách hành trình người dùng (User Journeys).

### Bước 3: Soạn Thảo Thiết Kế Cơ Sở (Kihon Sekkei) & Xuất Bản Hồ Sơ [BA Agent + TL/SA Agent]
- **Kỹ năng sử dụng**: `ba-design`, `sa-design` & `ba-docx`
- **Hành động**: 
  - BA soạn thảo `BD-00-overview.md` (Story Mapping, Walking Skeleton).
  - SA hỗ trợ dựng `BD-01-c4-context.md` (C4 Diagrams Mermaid).
  - BA + SA đồng thuận xây dựng `BD-02-domain-model.md` (Domain Entities & Bounded Contexts).
  - Tùy chọn: Dùng `ba-docx` đóng gói bộ tài liệu Basic Design thành hồ sơ hoàn chỉnh bàn giao cho khách hàng hoặc Giám đốc.

### Bước 4: Khởi Tạo Master Roadmap & Hội Ý Đa Tác Tử [PO/PM Agent]
- **Kỹ năng sử dụng**: `po-roadmap` & `po-party` (khi cần đối kháng)
- **Hành động**: 
  - Bóc tách Basic Design thành danh mục các Epics lớn, phân bổ vào các Milestone và khởi tạo bảng điều khiển `backlog/ROADMAP.md`.
  - Nếu xuất hiện xung đột lớn về công nghệ hoặc ranh giới phạm vi, PO triệu tập `po-party` để cả 5 tác tử (PO, BA, SA, Dev, EC) phản biện đa chiều và chốt quyết định ADR.

### Bước 5: Thẩm Định & Ký Duyệt Gate 1 [PO/PM Agent]
- **Kỹ năng sử dụng**: `po-gate`
- **Hành động**: PO/PM kiểm tra tính đầy đủ của bộ 3 tài liệu Basic Design. Ký biên bản `[GATE 1 PASS]` cho phép bắt đầu phân rã các Epic để chạy `wf-autopilot`.
