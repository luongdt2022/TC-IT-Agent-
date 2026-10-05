# AGENTS.md — Quy Chuẩn Vận Hành Toàn Diện Dành Cho AI Agent (Dự Án {{PROJECT_NAME}})

> **QUY ĐỊNH TỐI CAO**: Tập tin này là bộ luật điều hành bắt buộc cho mọi AI Agent (Google Antigravity, Cursor, Windsurf, Claude Code, Codex, DeepSeek...) khi hoạt động tại bất kỳ thư mục nào trong dự án {{PROJECT_NAME}}.  
> Tích hợp tinh hoa của **GitHub Spec Kit** (Đặc tả chính xác) và **BMad Method** (Tranh biện đối kháng đa tác tử & kiểm thử đa tầng).

---

## 1. NGUYÊN TẮC BẤT BIẾN & PHONG CÁCH LÀM VIỆC (MANDATORY BEHAVIOR)

- **Tỉ mỉ và Cẩn thận (Detail-Oriented)**: Luôn phân tích kỹ yêu cầu nghiệp vụ và cấu trúc hệ thống trước khi bắt tay vào làm. Tuyệt đối không làm ẩu, đốt cháy giai đoạn. Phải lường trước các rủi ro trước khi thực thi.
- **Hành động thay vì xin lỗi (Action over Apology)**: Khi gặp lỗi hoặc được user nhắc nhở, **TUYỆT ĐỐI KHÔNG** phản hồi bằng những câu sáo rỗng như "Tôi xin lỗi", "Bạn nói hoàn toàn đúng". Thay vào đó, phải **NGAY LẬP TỨC HÀNH ĐỘNG**: chạy công cụ sửa lỗi, kiểm tra lại logic và đưa ra kết quả đã khắc phục xong.
- **Tính chính xác tuyệt đối (Zero Hallucination)**: Không bao giờ đoán mò. Mọi thông tin nghiệp vụ/kỹ thuật phải trích từ tài liệu gốc, mã nguồn hiện có hoặc được người dùng xác nhận rõ ràng.
- **Chất lượng hơn tốc độ (Quality over Speed)**: Ưu tiên tạo ra sản phẩm đúng, chuẩn kiến trúc, an toàn và tối ưu ngay từ lần đầu tiên.
- **Kỷ Luật Chống Ảo Giác Tuyệt Đối (Anti-Hallucination Protocol)**:
  1. **Pre-flight Grounding**: Trước khi code UI phải đọc UI Component Catalog dùng chung; trước khi viết query CSDL phải đọc Data Schema / Models. Cấm phỏng đoán tên field hay reinvent the wheel.
  2. **Thực Thi Nguyên Tử (Atomic Chunking)**: 1 task / 1 chu kỳ kiểm tra, giữ context window < 15,000 tokens.
  3. **Chốt Chặn Toán Học Tự Động**: Bắt buộc chạy `./scripts/guard-rails.sh` kiểm chứng TypeCheck / Compiler trước khi tick `[x]`.
  4. **Red Test Bất Biến (Test Immobility)**: Dev tuyệt đối không được sửa assertion trong file test để pass giả tạo; chỉ sửa mã nguồn nghiệp vụ.

---

## 2. NGUỒN SỰ THẬT DUY NHẤT (SINGLE SOURCES OF TRUTH)

| Cần Biết | Đọc Tại |
|---|---|
| Luật bất di bất dịch | `constitution.md` |
| Hệ thống **hiện tại** làm gì | `docs/system/<vùng>.md` (hoặc `docs/01-basic-design/`) |
| Tiến độ tổng thể & Master Roadmap | `specs/ROADMAP.md` (hoặc `backlog/ROADMAP.md`) |
| Đặc tả chi tiết từng tính năng | `specs/[epic-id]/` (`spec.md`, `plan.md`, `tasks.md`) |
| Quyết định kiến trúc & Kỹ thuật | `docs/decisions/` (ADR) |
| Câu hỏi kỹ thuật đang treo | `docs/open-questions.md` |

*Lưu ý: `specs/` mô tả ý định tại thời điểm xây dựng; `docs/system/` mô tả hiện trạng thực tế đang chạy. Khi nghiệm thu xuất xưởng (`/xong`), bắt buộc cập nhật `docs/system/`.*

---

## 3. KỶ LUẬT THƯ MỤC CHỐNG RÁC (ZERO-TOLERANCE ROOT DUMPING)

Mọi tệp tin sinh ra BẮT BUỘC phải lưu đúng địa chỉ theo Bảng Điều Hướng Thư Mục:
- **Hồ sơ giải pháp & Báo giá**: `docs/00-presale-proposal/` (PROPOSAL.md, ESTIMATION_AND_COST.md)
- **Thiết kế cơ sở (Kihon Sekkei)**: `docs/01-basic-design/` (BD-*.md)
- **Thiết kế chi tiết (Shousai Sekkei)**: `docs/02-detail-design/` (DD-*.md: ERD, API contracts, Sequences)
- **Tiến độ & Roadmap**: `specs/` (hoặc `backlog/ROADMAP.md`)
- **Đặc tả tính năng (Spec Kit)**: `specs/[epic-id]/` (`spec.md`, `plan.md`, `tasks.md`)
- **Mã nguồn phần mềm**: `src/` (theo phân tầng Clean Architecture / Monorepo)
- **Hệ thống kiểm thử**: `tests/` (`tests/unit/`, `tests/integration/`, `tests/e2e/`, `tests/load/`, `tests/chaos/`)
- **Quyết định kiến trúc & Thay đổi**: `docs/decisions/` (ADR) và `docs/change-requests/`

> [!CAUTION]
> **NGHIÊM CẤM**: Không tạo bất kỳ file nháp `.md`, file code `.js/.ts/.py`, log hoặc script tạm vứt ở thư mục gốc (`root`). Vi phạm sẽ bị vệ binh `sa-guard` chặn Quality Gate!

---

## 4. ĐỘI NGŨ 6 AGENT CHUYÊN TRÁCH & QUY TRÌNH PHỐI HỢP

| STT | Agent Chuyên Trách | Định Vị Vai Trò | Cổng Kiểm Soát (Gate) Phụ Trách |
| :---: | :--- | :--- | :--- |
| **0** | [`ps`](.agents/ps.md) | Presale & IT Solution Consultant | **Pre-Project Gate**: Thẩm định RFP, Lập IT Proposal, Báo giá Man-Month, TCO. |
| **1** | [`po-pm`](.agents/po-pm.md) | Product Owner & Project Manager | **Gate 1**: Phê duyệt Basic Design & Scope.<br>**Gate 5**: Nghiệm thu DoD & Xuất xưởng (`xong`). |
| **2** | [`ba`](.agents/ba.md) | Senior Business Analyst | **Gate 1**: Khơi gợi 9D (`ba-elicit`), Basic Design, SRS 7 mục (`ba-srs`), làm rõ (`ba-clarify`), xuất Word (`ba-docx`). |
| **3** | [`techlead-sa`](.agents/techlead-sa.md) | Software Architect & Tech Lead | **Gate 2**: sa-analyze (Nhất quán chéo).<br>**Gate 3**: Adversarial Review, sa-guard, chốt ADR (`chot`). |
| **4** | [`dev`](.agents/dev.md) | Senior Full-Stack Developer | Thực thi tuần tự 1:1 `tasks.md`, 5 UX States qua `<Async>`, Unit Test 100% `BR-*`, hội tụ (`dev-converge`). |
| **5** | [`ec`](.agents/ec.md) | Edge-Case Hunter & QC Specialist | **Gate 4**: Săn lỗi biên (`ec-hunt`), Fuzzing Security (`ec-fuzz`), E2E Playwright (`ec-e2e`), Tải (`ec-load`), Hợp đồng (`ec-contract`), Hỗn loạn (`ec-chaos`), Đột biến (`ec-mutation`). |

---

## 5. DANH MỤC QUY TRÌNH CHUẨN (STANDARD WORKFLOWS)

| Lệnh / Workflow | Tác Tử Chủ Trì | Chức Năng Thực Thi |
| :--- | :--- | :--- |
| **`/wf-presale`** | **`ps`** | Biến đề bài thô / RFP thành IT Proposal và bảng tính Man-Month chi tiết. |
| **`/wf-kickoff`** | **`po-pm`** | Khởi động dự án, thiết lập Basic Design (Walking Skeleton) và Master Roadmap. |
| **`/wf-autopilot [epic-id]`** | **`po-pm`** | Điều phối toàn trình tự động một Epic từ Đặc tả đến Mã nguồn hoàn thiện (7 chặng khép kín). |
| **`/wf-delta [cr-id]`** | **`sa` + `ba`** | Xử lý yêu cầu thay đổi (CR) theo nguyên tắc: Tài liệu đi trước, Code theo sau. |
| **`/wf-uiux [epic-id]`** | **`dev`** | Chuẩn hóa giao diện 5 trạng thái UX và tự động chụp ảnh Playwright Visual QA. |
| **`/wf-audit`** | **`sa`** | Kiểm toán toàn diện: Clean Architecture, Traceability khép kín, và dọn rác thư mục. |
| **`/chot`** | **`sa`** | Sau khi chốt một quyết định kỹ thuật: Ghi nhận ADR trong `docs/decisions/` và cập nhật `open-questions.md`. |
| **`/xong [epic-id]`** | **`po-pm`** | Kiểm tra Definition of Done -> Cập nhật Living Docs `docs/system/` -> Chuyển Shipped. |
