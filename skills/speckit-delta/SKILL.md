---
name: "speckit-delta"
description: "Quy trình điều phối cập nhật & nâng cấp (Delta / Change Request) cho một Task/Epic trong hệ sinh thái NacenTech: từ Impact Analysis, bổ sung spec, cập nhật plan non-destructive, phân rã task mới [BE]/[FE], EF Core migration, kiểm thử hồi quy đến nghiệm thu hội tụ."
metadata:
  author: "NacenTwin Architecture Team"
  source: "custom/speckit-delta-nacentech"
  version: "2.2.0"
---

## User Input

```text
$ARGUMENTS
```

Tham số đầu vào bao gồm:
1. **Task cần cập nhật**: Mã Task chuẩn 1:1 (ví dụ: `TASK-00`, `TASK-04_HO_SO_CHAO_BAN_SELLER_VA_BO_LOC`, `TASK-06`).
2. **Nội dung thay đổi / Yêu cầu mới**: Mô tả yêu cầu sửa đổi, tài liệu bổ sung từ PO/Basic Design, hoặc yêu cầu kỹ thuật phát sinh (ví dụ: `Bổ sung 3D Scoped RBAC với 10 roles và ScopeType/ScopeId`, `Thêm 15 tiêu chí lọc ngành viễn thông`).

Nếu người dùng chưa cung cấp đủ thông tin, hãy hỏi người dùng:
1. Cần cập nhật Delta cho Task nào trong danh mục từ `TASK-00` đến `TASK-07`?
2. Chi tiết yêu cầu thay đổi nghiệp vụ hoặc kỹ thuật cần bổ sung là gì?

---

## Triết Lý Vận Hành Của Spec Kit Delta NacenTech (Core Principles)

Khác với việc xây dựng một Task mới từ con số 0, việc **sửa đổi/bổ sung một Task đang thi công hoặc đã hoàn thiện** đòi hỏi sự chặt chẽ tối đa để không làm gãy hệ thống đang chạy:

1. **Bất Biến Lịch Sử & Non-destructive Migration**:
   - **Tuyệt đối KHÔNG** sửa đè hoặc xóa các file EF Core / SQL migration cũ đã áp dụng vào CSDL PostgreSQL.
   - Luôn tạo file migration mới với tên mô tả rõ ràng (ví dụ: `Add3DScopedRbacToPersons`).
2. **Tương Thích Ngược Tuyệt Đối (Backward Compatibility)**:
   - Các cột mới bổ sung vào bảng đã có dữ liệu bắt buộc phải là `Nullable` (dấu `?`) hoặc có giá trị mặc định (`DEFAULT`).
   - Tuyệt đối không xóa cột hoặc đổi kiểu dữ liệu gây mất dữ liệu (data loss) nếu không có kế hoạch chuyển đổi tường minh.
3. **Bảo Toàn Danh Sách Việc Cũ (Append-only Tasks)**:
   - Giữ nguyên vẹn toàn bộ các task cũ đã đánh dấu `[x]` hoặc `[ ]`.
   - Phân rã phần việc mới thành một Giai đoạn bổ sung ở cuối file `tasks.md` (ví dụ: `## Giai đoạn N: Delta v2 — [Tên Nội Dung]`).
4. **Không Gây Hồi Quy (Zero Regression)**:
   - 100% test suites cũ của Backend (`dotnet test`) và Frontend phải tiếp tục pass.
   - Bổ sung test suites mới kiểm chứng chuyên biệt cho các trường/tính năng vừa nâng cấp.
5. **Đồng Bộ Hai Chiều Với Basic Design (Bidirectional Sync)**:
   - Nếu Delta xuất phát từ PO/Khách hàng: Cập nhật `Specification/02_BASIC_DESIGN/` $\rightarrow$ kéo sang `SourceCode/specs/`.
   - Nếu Delta xuất phát từ giải pháp kỹ thuật (như 3D Scoped RBAC): Ghi nhận rõ ràng để cập nhật tài liệu kiến trúc.
6. **Hội Tụ Đa Bề Mặt (Cross-Surface Convergence)**:
   - Một thay đổi nghiệp vụ không được coi là hoàn tất chỉ vì một kênh đã sửa. Trước khi code và trước khi converge, phải đối chiếu đủ: Basic Design/wireframe, Detail Spec, API/DTO, domain validation, DB/migration, Web, Zalo/Mobile (nếu tồn tại), public/owner/admin và test.

---

## Quy Trình Nâng Cấp Delta 5 Giai Đoạn Chi Tiết

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        NACENTECH SPECKIT DELTA PIPELINE                                │
└────────────────────────────────────────────────────────────────────────────────────────┘
  [1] Impact Analysis ──> Đánh giá bề mặt tác động & Viết Spec Delta vào spec.md
           │
           ▼
  [1.1] Clarify Check ──> 🛑 CHECKPOINT 1: DỪNG LẠI HỎI nếu mâu thuẫn/thiếu dữ kiện
           │               (Nếu yêu cầu rõ ràng -> Tự động đi tiếp)
           ▼
  [2] Plan Delta      ──> 🏛️ GATE 2 (SA Review): Cập nhật plan.md & schema CSDL EF Core
           │               🛑 CHECKPOINT 2: SA thẩm định Non-destructive Migration & DTOs
           ▼
  [2.1] speckit-uiux  ──> (Nếu Delta có đổi UI) Wireframe HTML mapping, 5 trạng thái UX
           │
           ▼
  [3] Tasks Delta     ──> Append Phase mới vào cuối tasks.md (Gắn tag [BE], [FE], [INT])
           │
           ▼
  [3.1] speckit-analyze──> 🏛️ GATE 2 (SA Consistency): Rà soát chéo Coverage Matrix Delta 100%
           │
           ▼
  [4] Implement Delta ──> Viết EF Core migration/code mới, cập nhật types, viết test delta
           │                🛑 CHECKPOINT 3: DỪNG LẠI HỎI nếu gặp lỗi môi trường/DB lock
           ▼
  [4.1] sa-gate3-delta ──> 🛑 GATE 3 BẮT BUỘC (SA Adversarial Review & Zero Regression Gate):
           │                - SA chạy pr-review-guard & guard-rails.sh rà soát 6 trục kiểm soát
           │                - SA phản hồi PO & Dev; Dev fix triệt để mọi lỗi trước khi sang QC
           ▼
  [5] Converge Delta  ──> 🛡️ GATE 4 (QC 4 Tầng Verification) & GATE 5 (PO DoD Sign-off):
                           Kiểm thử hồi quy 100%, đối soát DB/Code, cập nhật ROADMAP & TRACEABILITY
```

---

### Giai Đoạn 1: Đánh Giá Tác Động & Viết Spec Delta (`spec.md`)

1. **Bước 1.0 (BẮT BUỘC): Quét Mã Nguồn Toàn Cục (Grep-First Surface Discovery)**:
   - Trước khi viết bất kỳ chữ nào vào `spec.md`, BA/SA **bắt buộc phải chạy lệnh Grep toàn diện** trên toàn bộ codebase (`SourceCode/frontend/src/` và `SourceCode/backend/`) để tìm tất cả các vị trí tiêu thụ từ khóa/mã liên quan.
   - Tránh tuyệt đối cái bẫy "Mù cục bộ" (chỉ nhìn file spec của 1 Task mà bỏ sót Trang chủ, Login, Dashboard, Navigation...).
2. **Xác định Task mục tiêu & Lập Bảng Ma Trận Bề Mặt**:
   - Định vị thư mục Task tương ứng trong `specs/` (ví dụ: `specs/TASK-00_...` hoặc `specs/TASK-06_...`).
   - Lập **Cross-Surface Impact Matrix** gồm 4 cột: Bề mặt/Màn hình | File Path | Hiện trạng | Thay đổi cần làm.
3. **🛑 CHECKPOINT 1.1: CỔNG DUYỆT PHẠM VI ẢNH HƯỞNG (USER SCOPE GATE)**:
   - **BẮT BUỘC DỪNG LẠI**: Xuất trình Bảng Ma trận Bề mặt Ảnh hưởng cho User/PO và đặt câu hỏi xác nhận:
     > *"Yêu cầu này ảnh hưởng đến N màn hình sau: [Danh sách]. Xin User/PO xác nhận phạm vi trước khi đội ngũ tiến hành phân rã kỹ thuật."*
   - **Chỉ tiếp tục sang Giai đoạn 2 khi User gõ rõ `XÁC NHẬN SCOPE` hoặc đồng thuận phạm vi.** Tuyệt đối cấm tự suy diễn ngầm để đi tiếp!
4. **Cập nhật `spec.md` (Append-only)**:
   - Giữ nguyên toàn bộ nội dung của các User Stories cũ.
   - Thêm mục mới vào cuối file `spec.md`:
     ```markdown
     ## Spec Delta v2: [Tên Nội Dung Bổ Sung/Thay Đổi]
     - **Bối cảnh & Căn cứ thay đổi**: [Lý do phát sinh từ Basic Design hoặc Kỹ thuật].
     - **Yêu cầu chức năng mới**: [FR-NEW-###].
     - **Quy tắc nghiệp vụ bổ sung**: [BR-NEW-###].
     - **Tiêu chuẩn chấp thuận (Acceptance Criteria)**: [Given-When-Then].
     ```
5. **Cập nhật Master Roadmap (`specs/ROADMAP.md`)**:
   - Chuyển trạng thái Task trong Bảng Master Registry sang `🔄 Nâng cấp Delta (In Progress)`.
   - Ghi nhận yêu cầu thay đổi (Impact Analysis / Delta Request) vào Bảng Lịch sử thay đổi (Mục 4 của Roadmap).

---

### Giai Đoạn 1.1: Làm Rõ Điểm Mơ Hồ (Clarify Check) — 🛑 CHECKPOINT 1

1. **Rà soát tính nhất quán**:
   - Yêu cầu mới có xung đột với Basic Design nguồn (`Specification/02_BASIC_DESIGN/`) hay Hiến pháp (`.specify/memory/constitution.md`) không?
    - Có trường dữ liệu nào chưa rõ kiểu dữ liệu C# / PostgreSQL, hoặc chưa rõ điều kiện bắt buộc (Nullable/Required)?
   - Cross-Surface Impact Matrix đã có mọi bề mặt liên quan và xác định rõ phần nào là `ngoài phạm vi` chưa?
2. **Ra quyết định rẽ nhánh**:
   - **NẾU CÓ ĐIỂM MƠ HỒ HOẶC MÂU THUẪN**:
     - **DỪNG LẠI NGAY LẬP TỨC (STOP)**.
     - Trình bày tối đa 3 câu hỏi kèm phương án giải quyết đề xuất cho người dùng chọn.
     - Sau khi người dùng trả lời, ghi nhận vào `spec.md` và tự động chuyển sang **Giai đoạn 2**.
   - **NẾU ĐÃ ĐỦ RÕ RÀNG 100%**:
     - Thông báo: *"Đã phân tích xong phạm vi tác động của Delta. Yêu cầu rõ ràng, tự động chuyển tiếp sang Giai đoạn 2: Cập nhật Kế hoạch Kỹ thuật."*
     - Tự động tiếp tục sang **Giai đoạn 2**.

---

### Giai Đoạn 2: Cập Nhật Kế Hoạch Kỹ Thuật (Plan Delta) — 🏛️ GATE 2 (SA CHECKPOINT)

1. **Cập nhật `plan.md`**:
   - Thêm Section `## Plan Delta vX: [Tên Nội Dung]` vào cuối file `plan.md`.
   - Nêu rõ:
     - **Database Schema Delta**: Câu lệnh SQL / Migration EF Core non-destructive (ví dụ: `scope_type VARCHAR(20) DEFAULT 'GLOBAL'`).
     - **Domain & Contract Delta**: Interface `ICurrentActor`, DTOs mở rộng.
     - **API & Policy Delta**: Quy tắc phân quyền mới trong `authorization-rules.v1.json`.
2. **🏛️ MẶC ĐỊNH GỌI SA (`nacen-techlead-sa`) THẨM ĐỊNH MIGRATION & PLAN DELTA (GATE 2)**:
   - SA thẩm định nghiêm ngặt:
     - **Tính phi phá hủy (Non-destructive)**: CẤM xóa cột (`DropColumn`) hoặc xóa bảng đang chạy; cột mới bắt buộc phải là `Nullable` hoặc có `DEFAULT VALUE`.
     - Không làm hỏng dữ liệu hiện tại trong PostgreSQL.
     - Nếu có Breaking Change hoặc tái cấu trúc bảng dùng chung, SA trực tiếp thiết kế giải pháp Migration 2 bước kèm script chuyển đổi an toàn.
   - **SA phản hồi trực tiếp cho PO & Dev**: Đưa ra kết luận hoặc yêu cầu hiệu chỉnh trước khi chuyển sang phân rã việc.

---

### Giai Đoạn 2.1: Thiết Kế UI/UX Delta (`speckit-uiux`) — (Áp Dụng Cho Delta Có Đổi Giao Diện)

1. **Kiểm tra tác động UI của Delta**:
   - Nếu Delta thuần backend (DB, Auth, Migration): Tự động bỏ qua và chuyển sang **Giai đoạn 3**.
   - Nếu Delta có bổ sung trường, sửa form hoặc thêm widget:
2. **Khảo sát Bố cục & Component**:
   - Đảm bảo các input/button mới không làm vỡ layout Desktop (1440px) và Mobile (390px).
   - Ánh xạ component: `<FormField>`, `<TRLBadge>`, `<SectorTag>`, `<LoadingButton>`.
   - Đảm bảo đầy đủ 5 trạng thái UX qua `<Async>`.

---

### Giai Đoạn 3 & 3.1: Phân Rã Việc Delta & Rà Soát Phủ (`tasks.md` & `speckit-analyze`)

1. **Quy tắc Append-only cho `tasks.md`**:
   - Tìm mã task lớn nhất hiện tại (ví dụ `T-00.16`).
   - Thêm một Giai đoạn mới vào cuối `tasks.md` (ví dụ `## Giai đoạn 6: Delta v2 — [Tên Delta]` từ `T-00.17` trở đi).
   - Gắn tag rõ ràng: `[KERNEL]`, `[IDENTITY]`, `[PERSISTENCE]`, `[API]`, `[FE]`, `[TEST]`.
2. **🏛️ SA Rà Soát Ma Trận Phủ Delta (`speckit-analyze`)**:
   - 100% yêu cầu chức năng mới trong Spec Delta đều có task tương ứng.
   - 100% thay đổi schema và code đều có Unit/Integration Test kiểm chứng.
   - SA xác nhận không có bề mặt nào trong Cross-Surface Impact Matrix bị bỏ quên trước khi Dev bắt đầu lập trình.

---

### Giai Đoạn 4: Thi Công Thực Tế Delta (`Implement Delta`) — 🛑 CHECKPOINT 3

1. **Thực thi trong đúng Submodule tương ứng**:
   - Khi làm task Backend: Thao tác tại `SourceCode/backend/`.
     - Cập nhật Domain Entity và EF Core Configurations.
     - Tạo và chạy migration:
       ```bash
       dotnet ef migrations add <TênMigrationDelta> --project modules/<TênModule>
       dotnet ef database update
       ```
     - Cập nhật Handler, DTOs, Policy authorization rules.
     - Viết Unit / Integration Test mới kiểm chứng dữ liệu và quyền hạn Delta.
   - Khi làm task Frontend: Thao tác tại `SourceCode/frontend/`.
     - Bổ sung trường input, update UI component, xử lý state.
2. **Kỷ Luật Zero-Mock & Single Source of Truth trên Client**:
   - Cấm code màn hình CRUD/Quản trị chỉ bằng mock static state trong RAM. Bắt buộc màn hình phải có kết nối API thật và xử lý đủ các trạng thái UX qua `<Async>`.
   - Cấm hardcode mảng danh mục dữ liệu dùng chung tại từng component view lẻ. Mọi dữ liệu Master Data bắt buộc phải qua Hook/SDK tập trung.
3. **Kỷ Luật Quét Sạch Toàn Cục (Global Refactor Sweep)**:
   - Khi đổi mã định danh hoặc enum (ví dụ: `SEC-*` sang `LV`), Dev bắt buộc chạy lệnh grep toàn diện:
     ```bash
     grep -rn "<MA_CU>" SourceCode/frontend/src/ SourceCode/backend/
     ```
   - **Chỉ được đánh dấu `[x]` vào task khi kết quả quét trả về 0.**
4. **Kiểm tra hồi quy liên tục (Regression Test)**:
   - Backend: `dotnet build` và `dotnet test` (bắt buộc 100% test cũ và mới đều pass).
   - Frontend: Build sạch 0 lỗi (`npx tsc --noEmit` và `npm test`).
5. **Xử lý Blocker**: Nếu gặp lỗi xung đột migration hoặc deadlock DB, **DỪNG LẠI TRAO ĐỔI VỚI NGƯỜI DÙNG**.

---

### Giai Đoạn 4.1: Kiểm Toán Đối Kháng SA Cho Delta (Gate 3 Delta Bắt Buộc) — 🛑 CHECKPOINT 3.5

> [!IMPORTANT]
> **QUY ĐỊNH BẮT BUỘC TRƯỚC KHI BÀN GIAO SANG QC**:
> Mặc định sau khi Dev hoàn thành Implement Delta, workflow **BẮT BUỘC KÉO SA (`nacen-techlead-sa`) VÀO KIỂM TRA**. Tuyệt đối CẤM chuyển thẳng sang QC (`nacen-qc` / `tc-ec`) khi chưa có kết luận thẩm định Gate 3 của SA!

1. **SA Kích hoạt Chốt chặn Tĩnh & Review Delta**:
   - Chạy `./Agent/scripts/guard-rails.sh` kiểm tra biên dịch .NET, TypeScript và ranh giới Clean Architecture.
   - Kích hoạt `/pr-review-guard` rà soát theo **6 trục kiểm soát**:
     - **Trục 1 (Clean Architecture)**: Không vi phạm ranh giới tầng, không tiêm `DbContext` lên API, CQRS phân tách rõ ràng.
     - **Trục 2 (CSDL & EF Core Migration)**: Đảm bảo migration thực tế là non-destructive, không khóa chết DB, có index cho các trường tìm kiếm mới.
     - **Trục 3 (3D Scoped RBAC)**: Phân quyền Delta không bị rò rỉ hoặc bỏ sót permission check.
     - **Trục 4 (Concurrency & Idempotency)**: Luồng ghi có token bảo vệ chống ghi đè đồng thời.
     - **Trục 5 (Frontend 5 UX States)**: Component Delta bọc `<Async>`, giao diện responsive không vỡ layout.
     - **Trục 6 (Zero Regression)**: 100% Unit Test cũ và mới đều pass, `BR-*` mới có test bao phủ 100%.
2. **SA Phản hồi và Chỉ đạo Sửa chữa (Feedback Loop)**:
   - SA lập bảng đánh giá phân loại:
     - `🔴 CRITICAL`: Vi phạm kiến trúc, rò rỉ migration, lỗi hồi quy, thiếu test $\rightarrow$ **Chặn xuất xưởng**.
     - `🟡 WARNING`: Điểm cần tối ưu hóa mã nguồn.
   - **SA phản hồi trực tiếp cho PO và Dev**: Chỉ rõ sai lệch và yêu cầu sửa chữa.
   - **Dev BẮT BUỘC fix triệt để 100% lỗi `CRITICAL`**.
   - SA thực hiện Re-check. **CHỈ KHI SA KÝ DUYỆT "GATE 3 DELTA APPROVED"**, mới chính thức chuyển sang Giai đoạn 5 để bàn giao cho QC!

---

### Giai Đoạn 5: Đánh Giá Hội Tụ & Nghiệm Thu QC/PO (`Converge Delta`) — 🛡️ GATE 4 & GATE 5

1. **Bàn giao QC 4 Tầng Bắt Buộc (Gate 4 Verification)**:
   - QC (`nacen-qc` / `tc-ec`) tiếp nhận mã nguồn đã được SA phê duyệt ở Gate 3.
   - QC lập Test Matrix dựa trên Cross-Surface Impact Matrix của Bước 1.0 (bao phủ 100% các màn hình bị ảnh hưởng).
   - QC bắt buộc thực thi 4 tầng:
     - Tầng 1: Unit & Invariants Test.
     - Tầng 2: Contract Test (API DTO compatibility).
     - Tầng 3: Database Integration Test trên PostgreSQL container thật.
     - Tầng 4: Playwright E2E Visual QA & Scoped RBAC Fuzzing.
   - Cấm ký duyệt Gate 4 nếu chỉ test Backend hoặc bỏ qua màn hình UI liên quan.
2. **Nghiệm thu Cuối cùng (Gate 5 Sign-off - PO DoD)**:
   - PO/PM (`nacen-po-pm`) đối soát tiêu chuẩn hoàn thành Definition of Done (`xong`).
   - Cập nhật Ma trận Truy vết trong [`specs/TRACEABILITY.md`](file:///Users/luongdt/Library/CloudStorage/GoogleDrive-luongdt.wi@gmail.com/My Drive/NacenTechProject/SourceCode/specs/TRACEABILITY.md).
   - Đổi trạng thái Task trong [`specs/ROADMAP.md`](file:///Users/luongdt/Library/CloudStorage/GoogleDrive-luongdt.wi@gmail.com/My Drive/NacenTechProject/SourceCode/specs/ROADMAP.md) sang `✅ Hoàn thành (Delta vX)`.
   - Ghi nhận chi tiết kết quả vào Lịch sử thay đổi (Mục 4 của Roadmap).
3. **Hướng dẫn Commit Đa Tầng Submodules**:
   - Hướng dẫn commit code Backend vào `NacenTwin.git`.
   - Hướng dẫn commit code Frontend vào `NacenTwinFE.git`.
   - Tự động commit cập nhật spec và con trỏ submodule tại `Specification.git`.
4. **Báo Cáo Nghiệm Thu Hoàn Tất Delta**:
   - Báo cáo danh sách các trường/tính năng mới đã bổ sung.
   - Báo cáo số lượng test cases mới và kết quả kiểm thử hồi quy 100% pass.
   - Sẵn sàng kích hoạt bước tiếp theo.
