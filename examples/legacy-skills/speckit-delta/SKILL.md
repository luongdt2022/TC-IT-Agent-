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
  [2] Plan Delta      ──> Cập nhật plan.md & schema CSDL (Chiến lược Non-destructive EF Core)
           │               🛑 CHECKPOINT 2: DỪNG LẠI HỎI nếu có Breaking Change
           ▼
  [2.1] speckit-uiux  ──> (Nếu Delta có đổi UI) Wireframe HTML mapping, 5 trạng thái UX
           │
           ▼
  [3] Tasks Delta     ──> Append Phase mới vào cuối tasks.md (Gắn tag [BE], [FE], [INT])
           │
           ▼
  [3.1] speckit-analyze──> Rà soát chéo ma trận phủ Delta (Coverage Matrix 100%)
           │
           ▼
  [4] Implement Delta ──> Viết EF Core migration/code mới, cập nhật types, viết test delta
           │               🛑 CHECKPOINT 3: DỪNG LẠI HỎI nếu gặp lỗi môi trường/DB lock
           ▼
  [5] Converge Delta  ──> Kiểm thử hồi quy 100%, đối soát DB/Code, cập nhật ROADMAP & TRACEABILITY
                           🛑 CHECKPOINT 4: Báo cáo nghiệm thu hoàn tất Delta
```

---

### Giai Đoạn 1: Đánh Giá Tác Động & Viết Spec Delta (`spec.md`)

1. **Xác định Task mục tiêu**:
   - Định vị thư mục Task tương ứng trong `specs/` (ví dụ: `specs/TASK-00_PLATFORM_FOUNDATION_VA_COMMON` hoặc `specs/TASK-04_...`).
   - Đọc kỹ `spec.md`, `plan.md`, `tasks.md` và mã nguồn hiện tại của Task đó trong `backend/` và `frontend/`.
2. **Phân tích bề mặt tác động (Impact Surface Analysis)**:
   - **Database Layer (PostgreSQL)**: Bảng nào bị thêm/sửa cột? Enums/Constraints nào cần mở rộng? Khóa ngoại tới Master Data có đổi không?
   - **Domain & Application**: UseCases nào bị ảnh hưởng? Logic validate `BR-XX-*` nào cần rẽ nhánh mới?
   - **3D Scoped RBAC**: Có thay đổi quyền hạn của 10 PlatformRoles hay 4 ScopeTypes không?
   - **API / Contracts**: Request/Response DTOs nào cần nhận thêm trường? Mã lỗi mới?
   - **UI/UX Layer**: Màn hình nào bị thêm/sửa input? Có ảnh hưởng 5 trạng thái UX không?
   - **Backward Compatibility**: Dữ liệu hiện có trong CSDL PostgreSQL có bị ảnh hưởng không?
   - **Kênh và projection khác**: Web Portal, Zalo/Mobile, background/AI intake, public/owner/admin projection nào cùng dùng quy tắc hoặc field này?
3. **Lập Cross-Surface Impact Matrix bắt buộc**:
   - Ghi vào `plan.md` hoặc `spec.md` một bảng gồm: bề mặt, trạng thái hiện tại, thay đổi cần làm, test/kiểm chứng và trạng thái `đã rà soát`.
   - Nếu thay đổi liên quan field/PII, bổ sung Field Lifecycle: lưu trữ, nhập, hiển thị, quyền đọc, mục đích xử lý và retention/ngoại lệ.
   - Không được mặc định một thay đổi ở Zalo/Web chỉ áp dụng cho chính kênh đó. Nếu phạm vi chưa rõ hoặc mâu thuẫn giữa tài liệu/kênh, dừng tại Checkpoint 1.1 để PO quyết định.
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

### Giai Đoạn 2: Cập Nhật Kế Hoạch Kỹ Thuật (Plan Delta) — 🛑 CHECKPOINT 2

1. **Cập nhật `plan.md`**:
   - Thêm Section `## Plan Delta vX: [Tên Nội Dung]` vào cuối file `plan.md`.
   - Nêu rõ:
     - **Database Schema Delta**: Câu lệnh SQL / Migration EF Core non-destructive (ví dụ: `scope_type VARCHAR(20) DEFAULT 'GLOBAL'`).
     - **Domain & Contract Delta**: Interface `ICurrentActor`, DTOs mở rộng.
     - **API & Policy Delta**: Quy tắc phân quyền mới trong `authorization-rules.v1.json`.
2. **Ra quyết định rẽ nhánh**:
   - **NẾU PHÁT HIỆN BREAKING CHANGE LỚN**: **DỪNG LẠI HỎI Ý KIẾN NGƯỜI DÙNG** về chiến lược migration trước khi thực thi.
   - **NẾU THAY ĐỔI AN TOÀN & NON-DESTRUCTIVE**: Tự động chuyển tiếp sang **Giai đoạn 2.1 (nếu có đổi UI)** hoặc **Giai đoạn 3 (nếu thuần backend)**.

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
2. **Rà soát ma trận phủ**:
   - 100% yêu cầu chức năng mới trong Spec Delta đều có task tương ứng.
   - 100% thay đổi schema và code đều có Unit/Integration Test kiểm chứng.

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
2. **Kiểm tra hồi quy liên tục (Regression Test)**:
   - Backend: `dotnet build` và `dotnet test` (bắt buộc 100% test cũ và mới đều pass).
   - Frontend: Build sạch 0 lỗi.
3. **Cập nhật tiến độ**: Tự động đánh dấu `[x]` vào từng task hoàn thành trong `tasks.md`.
4. **Xử lý Blocker**: Nếu gặp lỗi xung đột migration hoặc deadlock DB, **DỪNG LẠI TRAO ĐỔI VỚI NGƯỜI DÙNG**.

---

### Giai Đoạn 5: Đánh Giá Hội Tụ & Nghiệm Thu Delta (`Converge Delta`) — 🛑 CHECKPOINT 4

1. **Kiểm tra độ hội tụ thực tế**:
   - Xác nhận CSDL PostgreSQL container thật đã có các cột/bảng mới và dữ liệu cũ không bị lỗi.
    - 100% test suites của dự án pass (Zero Regression).
   - Cross-Surface Impact Matrix không còn hàng `chưa rà soát`; mọi hàng `cần sửa` có implementation/test hoặc được PO chấp thuận để pending ngoài scope.
2. **Cập nhật Ma trận Truy vết & Roadmap**:
   - Bổ sung các mã `REQ-NEW-*`, `BR-NEW-*`, file triển khai và test mới vào [`specs/TRACEABILITY.md`](file:///Users/luongdt/Library/CloudStorage/GoogleDrive-luongdt.wi@gmail.com/My Drive/NacenTechProject/SourceCode/specs/TRACEABILITY.md).
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
