---
name: "speckit-autopilot"
description: "Điều phối và thực thi tự động toàn diện một Epic qua các bước Spec Kit từ Specify đến Converge cho hệ sinh thái NacenTech."
metadata:
  author: "NacenTwin Architecture Team"
  source: "custom/speckit-autopilot-nacentech"
  version: "2.2.0"
---

## User Input

```text
$ARGUMENTS
```

Tham số đầu vào là mã Task hoặc tên Epic (Ví dụ: `TASK-00`, `TASK-04_HO_SO_CHAO_BAN_SELLER_VA_BO_LOC`, `TASK-06`, hoặc một yêu cầu nghiệp vụ cụ thể).
Nếu người dùng chưa cung cấp tham số, hãy tra cứu [`specs/ROADMAP.md`](file:///Users/luongdt/Library/CloudStorage/GoogleDrive-luongdt.wi@gmail.com/My Drive/NacenTechProject/SourceCode/specs/ROADMAP.md) và hỏi người dùng muốn thực thi Epic nào trong danh mục từ `TASK-00` đến `TASK-07`.

---

## Mục Tiêu & Triết Lý Vận Hành (Philosophy)

Skill **`speckit-autopilot`** giải quyết bài toán: **"Gọi 1 lần — Hoàn thành cả Epic"**. 
Thay vì người dùng phải gõ thủ công 7 câu lệnh nối tiếp nhau, skill này tự động điều phối toàn bộ chu trình phát triển phần mềm theo chuẩn Spec Kit của dự án NacenTech:

1. **Tự Động Hóa Liền Mạch (Seamless Automation)**: Tự động chuyển giao kết quả từ bước này sang bước tiếp theo mà không làm gián đoạn tiến độ.
2. **Điểm Dừng Tương Tác Có Trọng Tâm (Interactive Checkpoints)**: Chỉ dừng lại khi và chỉ khi:
   - Phát hiện điểm mơ hồ, mâu thuẫn hoặc chưa rõ ràng trong yêu cầu nghiệp vụ (**Checkpoint 1.1**).
   - Cần chốt quyết định kiến trúc quan trọng có nhiều phương án đánh đổi (**Checkpoint 2**).
   - Gặp lỗi blocking bên ngoài cần chỉ đạo của người dùng (**Checkpoint 4**).
   - Nghiệm thu tính năng khi hoàn tất 100% (**Checkpoint 5**).
3. **Tuân Thủ Hiến Pháp Dự Án (`.specify/memory/constitution.md`)**:
   - **Ánh xạ 1:1 với Thiết Kế Cơ Sở**: Mọi Task nghiệp vụ phải có nguồn gốc từ `Specification/02_BASIC_DESIGN/TASK-XX` và Master Excel SSOT.
   - **Kiến trúc Modular Monolith & Clean Architecture**: Tách biệt rõ ràng tầng Domain, Application, Infrastructure và Presentation trong `SourceCode/backend/`.
   - **Bảo mật & Phân quyền Đa tầng (3D Scoped RBAC)**: 10 vai trò hạt nhân (`PlatformRoles`), 4 cấp phạm vi (`ScopeTypes`: Global, Province, Sector, OrgUnit), kiểm soát quyền truy cập chặt chẽ (PDPD NĐ 13/2023/NĐ-CP).
   - **Chuẩn Hóa Ngành & Thang Đo TRL**: Tuân thủ 18 ngành kinh tế TT17, 109 cặp quan hệ Lĩnh vực - Công nghệ và thang đo mức độ sẵn sàng công nghệ TRL 1–9.
   - **Contract-First & Result Pattern**: Chốt DTOs và lỗi chuẩn RFC 7807 ProblemDetails trước khi code; mọi UseCase trả về `Result<T>`.
   - **Cô Lập Submodules (Submodule Isolation)**: Code BE commit vào `NacenTwin.git`, code FE commit vào `NacenTwinFE.git`, chỉ lưu con trỏ và Spec tại Umbrella repo `Specification.git`.

---

## Quy Trình 7 Giai Đoạn Chi Tiết

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        NACENTECH SPECKIT AUTOPILOT PIPELINE                            │
└────────────────────────────────────────────────────────────────────────────────────────┘
  [1] speckit-specify   ──> Đọc Basic Design (TASK-XX/README.md), sinh specs/TASK-XX/spec.md
           │
           ▼
  [1.1] speckit-clarify ──> 🛑 CHECKPOINT 1: DỪNG LẠI nếu mơ hồ quy tắc/nghiệp vụ; Tự động nếu rõ
           │
           ▼
  [2] speckit-plan      ──> Thiết kế Clean Architecture, DB schema, 3D Scoped RBAC;
           │                ⭐ CONTRACT-FIRST: Chốt DTOs/OpenAPI trước cho cả BE và FE
           │                🛑 CHECKPOINT 2: Phê duyệt quyết định kiến trúc lớn (Trade-offs)
           │
           ▼
  [2.1] speckit-uiux    ──> (Nếu Task có UI) Wireframe HTML mapping, chuẩn hóa 5 UX States (<Async>)
           │
           ▼
  [3] speckit-tasks     ──> Phân rã tasks.md gắn tag [CONTRACT], [BE], [FE], [INT]
           │
           ▼
  [3.1] speckit-analyze ──> Rà soát chéo Coverage Matrix (100% REQ-*, BR-* có task tương ứng)
           │
           ▼
  [4] speckit-implement ──> Thi công song song: BE (SourceCode/backend/) & FE (SourceCode/frontend/)
           │                🛑 CHECKPOINT 3: DỪNG LẠI nếu gặp blocker môi trường/DB/SDK
           ▼
  [5] speckit-converge  ──> Chạy Unit Test BR-*, DB Integration, Visual QA, cập nhật ROADMAP.md
                            🛑 CHECKPOINT 4: Nghiệm thu toàn trình và push commit các submodules
```

---

### Cổng 0: Kiểm tra lan truyền quyết định (Cross-Surface Preflight)

Trước Giai đoạn 1, Autopilot phải tìm các Decision Record mới hoặc quy tắc bị thay thế trong Basic Design/spec hiện hữu. Với mỗi quyết định có thể chạm nhiều kênh, lập Cross-Surface Impact Matrix gồm: Basic Design/wireframe, Detail Spec, API/DTO, domain validation, DB/migration, Web, Zalo/Mobile, public/owner/admin và test. Nêu rõ bề mặt nào không tồn tại hoặc ngoài scope.

Nếu matrix phát hiện mâu thuẫn, chưa rõ phạm vi, hoặc có PII mà chưa rõ vòng đời (lưu, nhập, hiển thị, quyền đọc, mục đích), dừng ở Checkpoint 1 để hỏi PO; không tự triển khai ở một kênh rồi suy diễn cho phần còn lại.

### Giai Đoạn 1: Khởi Tạo Yêu Cầu Từ Basic Design (`speckit-specify`)

1. **Xác định Feature Scope & Nguồn Dữ Liệu**:
   - Phân tích mã Task từ `$ARGUMENTS` (ví dụ `TASK-04_HO_SO_CHAO_BAN_SELLER_VA_BO_LOC` hoặc `TASK-00`).
   - Nếu là Task nghiệp vụ (`TASK-01` $\rightarrow$ `TASK-07`): Tự động đọc tài liệu nguồn tại [`../../Specification/02_BASIC_DESIGN/TASK-XX/README.md`](file:///Users/luongdt/Library/CloudStorage/GoogleDrive-luongdt.wi@gmail.com/My Drive/NacenTechProject/Specification/02_BASIC_DESIGN), các biểu mẫu HTML mô phỏng và Sheet Excel tương ứng trong `DỮ_LIỆU_GỐC_MASTER/`.
   - Nếu là Task kỹ thuật (`TASK-00`): Đọc yêu cầu hạ tầng Clean Architecture, Docker PostgreSQL, Shared Kernel.
2. **Khởi tạo Feature Directory Khớp 1:1**:
   - Tạo thư mục: `specs/TASK-XX_<TEN_GIONG_BASIC_DESIGN>/` (Khớp 100% với tên thư mục Basic Design).
   - Cập nhật `.specify/feature.json`:
     ```json
     {
       "feature_directory": "specs/TASK-XX_<TEN_GIONG_BASIC_DESIGN>"
     }
     ```
3. **Sinh tài liệu `spec.md` chuẩn hóa**:
   - Xây dựng User Stories phân theo thứ tự ưu tiên (P1, P2...). Mỗi User Story phải có:
     - **Why this priority** (Giá trị nghiệp vụ).
     - **Independent Test** (Kịch bản kiểm thử độc lập).
     - **Acceptance Scenarios** (Chuẩn Given-When-Then).
   - Functional Requirements (`REQ-XX-###`) đánh số tuần tự.
   - Business Rules (`BR-XX-###`): Bóc tách toàn bộ quy tắc nghiệp vụ (ví dụ: quy tắc lọc 18 ngành, điều kiện TRL 1-9 khi chuyển giao, quy tắc định danh MST).
   - Success Criteria (`SC-###`): Tiêu chí định lượng đo lường được.
4. **Đồng bộ Master Roadmap (`specs/ROADMAP.md`)**:
   - Cập nhật trạng thái của Task trong Bảng Master Registry sang `🔵 Đang thi công`.

---

### Giai Đoạn 1.1: Làm Rõ Nghiệp Vụ (`speckit-clarify`) — 🛑 CHECKPOINT 1

1. **Phân tích độ hoàn thiện của `spec.md`**:
   - Rà soát các quy tắc nghiệp vụ: Có logic nào bị mập mờ, thiếu điều kiện rẽ nhánh hoặc xung đột giữa các Sheet dữ liệu?
   - Rà soát tích hợp và quyền hạn: 3D Scoped RBAC (ai được duyệt, ở phạm vi tỉnh hay toàn quốc), quy chuẩn file đính kèm.
2. **Ra quyết định rẽ nhánh**:
   - **TRƯỜNG HỢP CÓ ĐIỂM MƠ HỒ (Ambiguous / Underspecified)**:
     - **DỪNG LẠI NGAY LẬP TỨC (STOP)**.
     - Trình bày tối đa 3 câu hỏi trọng tâm dạng bảng trắc nghiệm A/B/C kèm phân tích tác động kỹ thuật.
     - Đợi phản hồi trực tiếp từ người dùng.
     - Khi người dùng trả lời: Ghi nhận câu trả lời vào mục `Clarifications & Key Technical Decisions` trong `spec.md`, sau đó tự động chuyển sang **Giai đoạn 2**.
   - **TRƯỜNG HỢP YÊU CẦU ĐÃ ĐỦ RÕ RÀNG (100% Clarity)**:
     - Xuất thông báo: *"Yêu cầu nghiệp vụ của Task đã rõ ràng 100% từ tài liệu Basic Design. Tự động chuyển tiếp sang Giai đoạn 2: Lập kế hoạch kỹ thuật."*
     - Tự động tiếp tục sang **Giai đoạn 2**.

---

### Giai Đoạn 2: Lập Kế Hoạch Kỹ Thuật (`speckit-plan`) — 🛑 CHECKPOINT 2

1. **Thiết Kế Contract-First (Bản Hợp Đồng Giao Tiếp Bắt Buộc)**:
   - Sinh file `plan.md` trong thư mục Task.
   - Định nghĩa trước toàn bộ:
     - Request / Response DTOs.
     - API Endpoints (`API-XX-###`).
     - Mã lỗi chuẩn RFC 7807 ProblemDetails (`ErrorCodes`).
   - *Lợi ích*: Cung cấp ngay bản hợp đồng để Frontend và Backend có thể thi công song song.
2. **Backend Architecture Plan (`backend/`)**:
   - Xác định module thụ hưởng trong `backend/modules/<module-name>/`.
   - Thiết kế Entity Framework Core Schema, Data Annotations, Foreign Keys tới Master Data (Ngành, Lĩnh vực).
   - Tích hợp **3D Scoped RBAC**: Gán `ScopeType` và `ScopeId` vào bảng dữ liệu tương ứng.
   - Thiết lập UseCase Handler (MediatR/FastEndpoints) áp dụng `Result<T>` và `AuditableEntity`.
3. **Frontend Architecture Plan (`frontend/`)**:
   - Cấu trúc trang/views, routing, state management.
4. **Quy tắc Kiểm tra Hiến pháp (Constitution Check Gate)**:
   - Nghiêm cấm dùng raw SQL không an toàn; bắt buộc dùng EF Core / LINQ parameterized queries.
   - Bắt buộc kiểm tra quyền qua `ICurrentActor` (không hardcode role chuỗi trần).
   - Bắt buộc dùng PostgreSQL container thật trong môi trường phát triển (không mock database cốt lõi).
5. **Ra quyết định rẽ nhánh**:
   - **NẾU có quyết định kiến trúc lớn có trade-offs**: **DỪNG LẠI HỎI Ý KIẾN NGƯỜI DÙNG** kèm bảng so sánh.
   - **NẾU kế hoạch đã chuẩn mực**: Tự động chuyển tiếp sang **Giai đoạn 2.1 (nếu có UI)** hoặc **Giai đoạn 3 (nếu thuần backend)**.

---

### Giai Đoạn 2.1: Thiết Kế UI/UX & Wireframe Mapping (`speckit-uiux`)

1. **Kiểm tra loại Task**:
   - Nếu Task thuần backend (như `TASK-00`, Cron worker, Migration): Tự động bỏ qua và chuyển sang **Giai đoạn 3**.
   - Nếu Task có giao diện người dùng (ví dụ: `TASK-01` Portal, `TASK-02` Form DN, `TASK-04` Bộ Lọc):
2. **Khảo sát Wireframe từ Basic Design**:
   - Đọc trực tiếp các file HTML review (ví dụ `bo_loc_cban_view.html`, `form_dn_dmst.html`).
   - Quy hoạch layout Desktop (Dashboard/Grid lọc nâng cao) và Mobile (Responsive filter modal).
3. **Chuẩn hóa 5 Trạng Thái UX Bắt Buộc (`<Async>`)**:
   - `Loading`: Hiển thị Skeleton loaders tương ứng với form/bảng.
   - `Empty`: Trạng thái rỗng kèm hướng dẫn và nút thêm mới/tra cứu lại.
   - `Error`: Thông báo lỗi thân thiện kèm nút Thử lại (Retry).
   - `Success`: Hiển thị dữ liệu chuẩn xác.
   - `Partial`: Tải dữ liệu từng phần (Infinite scroll / phân trang PagedList).
4. **Ghi nhận vào `plan.md`**: Bổ sung mục `UI/UX Component & Layout Specification` vào `plan.md`.

---

### Giai Đoạn 3 & 3.1: Phân Rã Task & Rà Soát Ma Trận Phủ (`speckit-tasks` & `speckit-analyze`)

1. **Sinh file `tasks.md` đa chiều có gắn Tag Submodule**:
   ```markdown
   ### Phase 1: API Contract & Mocking [CONTRACT]
   - [ ] T-XX.1 [CONTRACT] Định nghĩa DTOs và API Schema giao tiếp giữa BE và FE

   ### Phase 2: Triển Khai Backend [BE] (Thực thi tại `SourceCode/backend/`)
   - [ ] T-XX.2 [BE] Tạo EF Core Migration và Entity mapping có 3D Scoped RBAC
   - [ ] T-XX.3 [BE] Cài đặt Domain Logic và Business Rules `BR-XX-*`
   - [ ] T-XX.4 [BE] Viết Unit Tests bao phủ 100% các Business Rules

   ### Phase 3: Triển Khai Frontend [FE] (Thực thi tại `SourceCode/frontend/`)
   - [ ] T-XX.5 [FE] Xây dựng UI Screen theo wireframe Basic Design
   - [ ] T-XX.6 [FE] Tích hợp gọi API client với 5 UX states

   ### Phase 4: Tích Hợp & Nghiệm Thu [INT]
   - [ ] T-XX.7 [INT] Chạy kiểm thử tích hợp E2E kết nối UI -> API -> DB
   ```
2. **Rà soát chéo Ma trận Phủ (Coverage Matrix)**:
   - 100% User Stories đã có ít nhất một task thực thi.
   - 100% Business Rules (`BR-XX-*`) có Unit Test tương ứng.
   - Tự động bổ sung các task bị sót vào `tasks.md` trước khi tiến hành viết code.
   - Cross-Surface Impact Matrix phải được chuyển thành task `[BE]`, `[FE]`, `[ZALO]`, `[INT]` và `[TEST]` tương ứng; mỗi hàng chỉ được đóng khi có bằng chứng implementation hoặc quyết định PO pending.

---

### Giai Đoạn 4: Thi Công Thực Tế Song Song (`speckit-implement`) — 🛑 CHECKPOINT 3

1. **Thi công đúng ngữ cảnh Submodule**:
   - Khi làm task `[BE]`: AI tự động thao tác trong thư mục `SourceCode/backend/`, sinh mã nguồn .NET Clean Architecture, chạy kiểm thử:
     ```bash
     dotnet build NacenTech.slnx
     dotnet test tests/NacenTech.UnitTests/
     ```
   - Khi làm task `[FE]`: Thao tác trong thư mục `SourceCode/frontend/`, dựng component, test các trạng thái UX.
2. **Cập nhật tiến độ**: Tự động đánh dấu `[x]` vào từng task hoàn thành trong `tasks.md`.
3. **Xử lý tình huống Blocker**:
   - Nếu gặp lỗi biên dịch không thể tự sửa, thiếu biến môi trường hoặc connection string CSDL -> **DỪNG LẠI BÁO CÁO NGƯỜI DÙNG** kèm phương án xử lý ngay lập tức.

---

### Giai Đoạn 5: Đánh Giá Hội Tụ & Nghiệm Thu (`speckit-converge`) — 🛑 CHECKPOINT 4

1. **Kiểm tra Tiêu Chuẩn Hoàn Thành (Definition of Done)**:
   - Backend: `dotnet test` đạt 100% pass toàn bộ test suites.
   - Frontend: Build sạch, không có lỗi runtime/type.
   - CSDL: Migration chạy thành công trên PostgreSQL container thật.
   - Ma trận truy vết: Đối soát khép kín trong [`specs/TRACEABILITY.md`](file:///Users/luongdt/Library/CloudStorage/GoogleDrive-luongdt.wi@gmail.com/My Drive/NacenTechProject/SourceCode/specs/TRACEABILITY.md).
   - Cross-Surface Impact Matrix: không còn bề mặt chưa rà soát; mỗi thay đổi field/quy tắc có regression test trên các kênh còn trong phạm vi.
2. **Đồng bộ Master Roadmap (`specs/ROADMAP.md`)**:
   - Cập nhật trạng thái của Task sang `✅ Hoàn thành`.
   - Cập nhật số task thực tế, kết quả test và ghi nhận vào Lịch sử thay đổi (Mục 4 của Roadmap).
3. **Hướng dẫn Commit Đa Tầng Submodules**:
   - Xuất lệnh git gợi ý để người dùng commit và push mã nguồn của từng repo:
     ```bash
     # 1. Commit Backend (nếu có sửa code BE):
     cd backend && git add . && git commit -m "feat(module): implement TASK-XX" && git push origin main && cd ..
     # 2. Commit Frontend (nếu có sửa code FE):
     cd frontend && git add . && git commit -m "feat(ui): implement TASK-XX screens" && git push origin main && cd ..
     # 3. Commit Umbrella Repo (lưu spec và con trỏ submodules):
     git add . && git commit -m "feat(spec): converge and complete TASK-XX" && git push origin main
     ```
4. **Báo Cáo Nghiệm Thu Trọn Vẹn**:
   - Tổng kết các tính năng đã hoàn thiện.
   - Báo cáo số lượng Unit/Integration test pass.
   - Sẵn sàng kích hoạt Task tiếp theo theo lộ trình Master Roadmap.
