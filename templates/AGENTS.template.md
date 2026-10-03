# AGENTS.md — Quy Chuẩn Vận Hành Toàn Diện Dành Cho AI Agent (Dự Án NacenTech)

> **QUY ĐỊNH TỐI CAO**: Tập tin này là bộ luật điều hành bắt buộc cho mọi AI Agent (Antigravity, Cursor, Windsurf, Claude Code...) khi hoạt động tại bất kỳ thư mục nào trong dự án NacenTech.

---

## 0. CHỈ THỊ NHẮC NHỞ QUY TRÌNH (PROCESS REMINDER DIRECTIVE)

- **Phạm vi áp dụng BẮT BUỘC**: CHỈ hiển thị khối nhắc nhở quy trình và định vị bước khi:
  1. Đang thực hiện **soạn thảo đặc tả chi tiết (viết SRS 7 mục với `ba-srs-copilot`, viết `spec.md` kỹ thuật)**.
  2. Đang thực hiện **phân rã & triển khai task (chạy `/speckit-implement`, `/speckit-test`, `/speckit-autopilot`)**.
- **Phạm vi MIỄN TRỪ (TUYỆT ĐỐI KHÔNG CHÈN KHỐI NHẮC NHỞ)**:
  - Khi đang **trao đổi, tìm hiểu, thảo luận ý tưởng, khảo sát thông tin**.
  - Khi đang **soạn thảo và hoàn thiện Thiết Kế Cơ Sở (Basic Design - `/nacen-basic-design`)**.
  - Trong các ngữ cảnh này, AI Agent giao tiếp trực tiếp, ngắn gọn, đi thẳng vào nội dung công việc, không chèn các thông báo quy trình gây cản trở trải nghiệm người dùng.

Khi thuộc phạm vi bắt buộc, thực hiện 3 hành động:
1. Nhắc nhở tuân thủ: [`Specification/QUY_TRINH_VAN_HANH_BA_SPECKIT_NACENTECH.md`](Specification/QUY_TRINH_VAN_HANH_BA_SPECKIT_NACENTECH.md).
2. Định vị chính xác bước hiện tại trong chu trình.
3. Chỉ dẫn dứt khoát bước tiếp theo (lệnh cụ thể).

---

## 1. NGUYÊN TẮC BẤT BIẾN (NON-NEGOTIABLE CORE BEHAVIOR)

- **Tỉ mỉ và Cẩn thận (Detail-Oriented)**: Luôn kiểm tra đối chiếu dữ liệu gốc trước khi thực hiện. Tuyệt đối không làm ẩu, đốt cháy giai đoạn.
- **Hành động thay vì xin lỗi (Action over Apology)**: Không sử dụng các câu xin lỗi xã giao sáo rỗng. Khi phát hiện sai sót, chạy ngay công cụ để sửa lỗi và báo cáo kết quả đã khắc phục.
- **Tuyệt đối không đoán mò (Zero Hallucination)**: Mọi thông tin nghiệp vụ/kỹ thuật phải trích từ tài liệu gốc (`Specification/Dat-hang-phan-mem.xlsx`, `Tai lieu BA Nacentwin.xlsx`) hoặc được người dùng xác nhận rõ ràng.
- **Chất lượng hơn tốc độ (Quality over Speed)**: Ưu tiên tạo ra sản phẩm đúng, chuẩn cấu trúc và kiểm thử chặt chẽ ngay từ lần đầu tiên.
- **Lan truyền quyết định bắt buộc (Decision Propagation)**: Khi PO chốt thay đổi có thể ảnh hưởng nhiều bề mặt, lập Cross-Surface Impact Matrix trước khi code và khi nghiệm thu. Tối thiểu rà soát: Basic Design/wireframe, Detail Spec, API/DTO, domain validation, DB/migration, Web, Zalo/Mobile nếu có, public/owner/admin projection và test. Không được kết luận hoàn thành khi mới sửa một kênh; phần ngoài scope phải có quyết định PO ghi nhận rõ.

---

## 2. HỆ THỐNG 5 REPOSITORIES & KIẾN TRÚC VẬN HÀNH (MULTI-REPO ECOSYSTEM)

Dự án được phân rã thành 5 GitHub Repositories chuyên biệt thuộc tổ chức `NacenTwin`:

| TT | Repository GitHub | Thư Mục Local | Đối Tượng Phụ Trách | Mục Đích Quản Lý |
| :---: | :--- | :--- | :--- | :--- |
| **1** | [`NacenTwin/Agent`](https://github.com/NacenTwin/Agent) | [`Agent/`](Agent/) | AI Architect & Lead BA | Chứa bộ kỹ năng (Skills), Hiến pháp (`constitution.md`), Agents và scripts tự động hóa. |
| **2** | [`NacenTwin/NacenTwin-Docs`](https://github.com/NacenTwin/NacenTwin-Docs) | [`Specification/`](Specification/) | PO / BA / Stakeholders | Thiết Kế Cơ Sở (Basic Design), Master Excel SSOT, Wireframe HTML, Khảo sát nghiệp vụ. |
| **3** | [`NacenTwin/Specification`](https://github.com/NacenTwin/Specification) | [`SourceCode/`](SourceCode/) | Tech Lead & Developers | Umbrella Repo điều phối, Spec Kit Detail Design (`specs/TASK-00` $\rightarrow$ `TASK-07`), Roadmap & Traceability. |
| **4** | [`NacenTwin/NacenTwin`](https://github.com/NacenTwin/NacenTwin) | [`SourceCode/backend/`](SourceCode/backend/) | Backend Developers | Submodule Backend .NET Core Clean Architecture, Modular Monolith, Database Migrations. |
| **5** | [`NacenTwin/NacenTwinFE`](https://github.com/NacenTwin/NacenTwinFE) | [`SourceCode/frontend/`](SourceCode/frontend/) | Frontend Developers | Submodule Frontend UI Web Portal, App, Async 5 UX States. |

- **Quy tắc liên kết**: AI Agent đứng ở thư mục gốc có thể đọc chéo tài liệu giữa tất cả các repositories mà không gặp bất kỳ xung đột nào.
- **Quy tắc commit**: Mỗi repository quản lý lịch sử commit độc lập, không làm ô nhiễm mã nguồn lẫn nhau.

---

## 3. DANH MỤC KỸ NĂNG & LỆNH ĐIỀU PHỐI CHÍNH

| Lệnh / Skill | Ngữ Cảnh Hoạt Động | Mục Đích Sử Dụng |
| :--- | :--- | :--- |
| **`/nacen-workflow-guard`** | Toàn bộ dự án | Rà soát tuân thủ quy trình, phát hiện lỗ hổng/vi phạm và chỉ dẫn bước đi kế tiếp. |
| **`/nacen-basic-design`** | Folder gốc (Tầng PO/BA) | Thiết kế Cơ sở (Kihon Sekkei), định hình Khung xương sống (Backbone), C4 Context/Container, Walking Skeleton trước khi viết SRS. |
| **`ba-srs-copilot`** | Folder gốc (Tầng BA) | Thảo luận và chốt từng mục trong 7 mục SRS với cơ chế Cổng duyệt 1 chiều. |
| **`/nacen-srs-to-speckit`** | Folder gốc $\rightarrow$ SourceCode | Handoff SRS đã duyệt sang Epic kỹ thuật (`spec.md`), tự động cập nhật Roadmap & Traceability. |
| **`/speckit-plan`** | Trong `SourceCode/` | Thiết kế Clean Architecture, schema CSDL, API contracts. |
| **`/speckit-tasks`** | Trong `SourceCode/` | Phân rã đầu việc có checkbox kiểm chứng `[x]`. |
| **`/speckit-uiux`** | Trong `SourceCode/` | Thiết kế layout và chuẩn hóa 5 trạng thái UX (Empty, Loading, Error, Success, Partial). |
| **`/speckit-test`** | Trong `SourceCode/` | Kiểm thử 3 tầng: Unit (`BR-*`), DB Integration, E2E Visual QA. |
| **`/speckit-autopilot`** | Trong `SourceCode/` | Tự động hóa toàn trình thực thi một Epic (Specify $\rightarrow$ Converge). |
| **`/speckit-delta`** | Trong `SourceCode/` | Cập nhật Change Request non-destructive khi có thay đổi nghiệp vụ. |
| **`/nacen-aggregate-srs`** | Tầng BA / Báo cáo | Quét toàn bộ các `spec.md` sống để biên dịch ra file Word Master SRS bàn giao. |
| **`traceability-auditor`** | Toàn bộ dự án | Quét tự động ma trận truy vết khép kín `REQ- ↔ BR- ↔ DB- ↔ UI- ↔ API- ↔ Test`, bắt mã mồ côi. |
| **`clean-arch-guard`** | `SourceCode/` | Quét AST / namespace bảo vệ ranh giới Clean Architecture .NET & React, chặn rò rỉ DbContext. |
| **`rbac-permission-fuzzer`** | `SourceCode/` | Kiểm thử & fuzzing ma trận phân quyền 10 roles 3D Scoped RBAC, chống leo thang đặc quyền. |
| **`po-scope-triage`** | Folder gốc (Tầng PO) | Sàng lọc yêu cầu mới, phân loại P1/P2/P3 và lập Cross-Surface Impact Matrix. |
| **`bmad-party-mode`** | Toàn bộ dự án | Triệu tập Hội nghị Bàn tròn Đa Tác tử (Multi-Agent Party Mode) tranh luận giải quyết bài toán khó. |
| **`bmad-correct-course`** | Tầng PO/PM | Nắn dòng và chống trôi dạt (Drift) đưa dự án trở về đúng quỹ đạo mục tiêu. |
| **`bmad-advanced-elicitation`** | Tầng BA | Bộ 9 kỹ thuật khơi gợi nghiệp vụ chuyên sâu (5 Whys, Laddering, Devil's Advocate...). |
| **`speckit-converge`** | Tầng Dev / SA | Quét mức độ hội tụ mã nguồn so với đặc tả, tự động phát hiện mã còn thiếu để hoàn tất. |
| **`bmad-qa-generate-e2e-tests`** | Tầng QC | Tự động sinh trọn bộ kịch bản kiểm thử E2E Playwright từ Acceptance Criteria. |

---

## 4. ĐỘI NGŨ 5 AGENT CHUYÊN TRÁCH & QUY TRÌNH PHỐI HỢP (STAGE-GATE WORKFLOW)

Hệ thống vận hành theo mô hình phân công trách nhiệm (SoD) và Maker – Checker với 5 Agent chuyên trách tại `.agents/`:

| STT | Agent Chuyên Trách | Định Vị Vai Trò | Cổng Kiểm Soát (Gate) Phụ Trách |
| :---: | :--- | :--- | :--- |
| **1** | [`nacen-po-pm`](.agents/nacen-po-pm.md) | Product Owner & Project Manager | **Gate 1**: Phê duyệt SRS & Ranh giới.<br>**Gate 5**: Nghiệm thu cuối cùng & Roadmap. |
| **2** | [`nacen-ba`](.agents/nacen-ba.md) | Senior Business Analyst (BMad Specialist) | **Gate 1**: Biên soạn SRS 7 mục qua Cổng duyệt 1 chiều, chuẩn hóa `REQ-`, `BR-`, `DB-`. |
| **3** | [`nacen-techlead-sa`](.agents/nacen-techlead-sa.md) | Software Architect & Code Reviewer | **Gate 2**: Phê duyệt Kiến trúc Clean Architecture, Schema CSDL.<br>**Gate 3**: BMad Adversarial Code Review. |
| **4** | [`nacen-dev-senior`](.agents/nacen-dev-senior.md) | Senior Full-Stack Developer (.NET & React) | Thực thi lập trình 1:1 `tasks.md`, 5 UX States qua `<Async>`, Unit Test 100% `BR-*`. |
| **5** | [`nacen-qc`](.agents/nacen-qc.md) | Quality Control & Verification Specialist | **Gate 4**: Kiểm thử 3 tầng (Unit, DB, Playwright E2E), Săn lỗi biên (Edge-case Hunter). |

### Chu trình luân chuyển liên Agent:
$$\text{PO/PM} \xrightarrow{\text{Đề bài}} \text{BA} \xrightarrow{\text{SRS Converged}} \text{SA} \xrightarrow{\text{Plan/Tasks}} \text{Dev} \xrightarrow{\text{Mã nguồn}} \text{SA (Adversarial Review)} \xrightarrow{\text{Pass}} \text{QC (Test 3 Tầng)} \xrightarrow{\text{Quality Gate}} \text{PO/PM (Nghiệm thu)}$$

