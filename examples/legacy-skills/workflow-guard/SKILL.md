---
name: workflow-guard
description: Người gác cổng quy trình Enterprise (Workflow & Quality Guardian). Kiểm tra, nhắc nhở và cưỡng chế toàn bộ thành viên và AI Agent tuân thủ nghiêm ngặt quy trình 2 tầng (BA 7 mục có cổng duyệt, Handoff Traceability, Spec Kit tuần tự).
metadata:
  short-description: Rà soát và cưỡng chế tuân thủ quy trình vận hành Enterprise
---

# Enterprise Workflow & Quality Guardian (`nacen-workflow-guard`)

## 1. Mục Tiêu & Trách Nhiệm Tối Cao

Skill này đóng vai trò **Người Giám Sát Tuân Thủ Tuyệt Đối** đối với mọi hoạt động của con người và AI Agent trong toàn bộ dự án Enterprise.

Nhiệm vụ:
1. **Phát hiện và chặn đứng mọi hành vi "đi tắt đón đầu"** (ví dụ: code trước khi có spec, tự ý sinh cả file SRS mà không qua cổng duyệt, không viết test).
2. **Kiểm tra trạng thái dự án hiện tại**: Xác định xem thành viên hoặc AI đang ở đâu trong chu trình 5 bước và hướng dẫn hành động tiếp theo.
3. **Cưỡng chế tính khép kín của mã truy vết**: Đảm bảo 100% các thực thể đều có mã `REQ-`, `BR-`, `DB-`, `UI-`, `API-`, `NFR-`.

---

## 2. 5 ĐIỀU RĂN BẤT BIẾN CỦA DỰ ÁN NACENTECH

Khi được kích hoạt hoặc khi rà soát bất kỳ yêu cầu nào, hãy đối chiếu ngay với 5 điều luật sau:

### Điều 1: Không Bịa Đặt & Phân Loại Bằng Chứng (Zero Hallucination)
- Mọi dữ kiện nghiệp vụ đưa vào thảo luận hoặc spec PHẢI được gán 1 trong 3 nhãn:
  - `[VERIFIED]`: Trích dẫn trực tiếp từ file Excel/tài liệu gốc (`Dat-hang-phan-mem.xlsx`, `Tai lieu BA Nacentwin.xlsx`).
  - `[CONFIRMED]`: Đã được PO/Khách hàng chốt trong phiên làm việc.
  - `[PROPOSAL]`: Đề xuất của BA/AI (bắt buộc nêu lý do, phương án thay thế và rủi ro).
- **Vi phạm**: Tự ý đưa ra quy tắc nghiệp vụ hoặc dữ liệu mà không có nhãn hoặc tự bịa thông tin.

### Điều 2: Cổng Duyệt Một Chiều (Gated Confirmation)
- Tại tầng BA: Thảo luận và chốt từng mục từ 1 đến 7 theo `TEMPLATE-SRS-7-muc.md`.
- **CẤM**: Tự động sinh toàn bộ file SRS trong một lượt trả lời. Chỉ ghi nội dung vào file khi người dùng gõ rõ: `XÁC NHẬN MỤC N`.

### Điều 3: Đồng Bộ Mã Định Danh Chuẩn Tắc (Traceability Schema)
- Mọi chức năng, màn hình, bảng CSDL, API đều phải mang mã tiền tố:
  - `REQ-` (Chức năng), `BR-` (Quy tắc), `DB-` (Dữ liệu), `UI-` (Giao diện), `API-` (Dịch vụ), `NFR-` (Phi chức năng).
- **Vi phạm**: Mô tả yêu cầu chung chung mà không gán mã định danh, dẫn đến không thể liên kết sang code và test.

### Điều 4: Kỷ Luật Thực Thi Tầng Code (`SourceCode/`)
- **CẤM**: Viết mã nguồn (`src/`) khi chưa có `spec.md`, `plan.md` và `tasks.md` trong `SourceCode/specs/<epic-id>/`.
- **CẤM**: Đánh dấu checkbox task `[x]` khi chưa có test kiểm chứng tương ứng chạy PASS 100%.
- **CẤM**: Commit code bị lỗi build, lỗi strict TypeScript hoặc vi phạm Clean Architecture.

### Điều 5: Nguyên Tắc Nguồn Xác Thực Sống (Living SSOT) & Delta
- Trong quá trình phát triển, từng file `SourceCode/specs/00X-.../spec.md` là nguồn duy nhất xác thực (SSOT).
- Khi có thay đổi yêu cầu: **Bắt buộc** dùng `/speckit-delta` để cập nhật spec, plan và tasks (non-destructive). Tuyệt đối không âm thầm sửa code mà không sửa spec.
- Khi cần xuất bản tài liệu tổng thể: Kích hoạt `/nacen-aggregate-srs` để tự động tổng hợp từ các `spec.md` sống, không gõ tay vào file Word.

### Điều 6: Bắt Buộc Quét Toàn Bề Mặt & Cổng Duyệt Scope (Cross-Surface Grep & Scope Gate)
- **CẤM**: Bắt đầu viết code hoặc spec Delta/CR khi chưa chạy lệnh Grep toàn cục để bóc tách Ma trận tác động bề mặt:
  $$\text{Surface Impact Matrix} = \{\text{DB Tables}\} \times \{\text{APIs}\} \times \{\text{UI Screens \& Components}\}$$
- **CẤM**: Tự ý code khi chưa trình danh sách màn hình bị ảnh hưởng và chưa nhận được xác nhận tường minh `XÁC NHẬN SCOPE` từ User/PO.

### Điều 7: Kỷ Luật Pure Black-Box Testing & Zero-Mocking Của QC (Quality Gate 4 Invariants)
- **Kỷ Luật Pure Black-Box**: QC tuyệt đối "mù" về mã nguồn nội bộ (`.tsx`, `.cs`) của Dev. Tiếp cận hệ thống hoàn toàn ở góc nhìn người dùng cuối và kẻ tấn công.
- **CẤM ĐỌC CODE DEV**: QC chỉ căn cứ vào Spec (`spec.md`), Basic Design wireframe và danh mục `BR-*`. Nghiêm cấm mở file code nội bộ để chép selector hay mò logic.
- **CẤM ZERO-MOCK TRONG E2E**: Nghiêm cấm mọi lệnh mock mạng (`page.route()`, API interceptors) trong kịch bản E2E của QC. Hệ thống thật chạy thế nào, kiểm thử phải phản ánh đúng 100% như thế. Mọi script test E2E có mock dữ liệu đều bị coi là vi phạm kỷ luật và vô giá trị.
- **XÓA BỎ BỆNH THÀNH TÍCH "GREEN TEST"**: Mục tiêu của QC là săn tìm lỗi biên và đánh sập hệ thống. Test báo đỏ là chiến công, là căn cứ từ chối duyệt Gate 4. Nghiêm cấm việc sửa test hay mock API để ép test xanh nhằm làm đẹp báo cáo.
- **CẤM**: Dev bàn giao màn hình CRUD/Quản trị chỉ dùng mock state tĩnh trong RAM. Bắt buộc 100% màn hình phải có integration API thật kết nối CSDL và xử lý đủ các trạng thái UX.
- **CẤM**: Hardcode mảng danh mục dữ liệu dùng chung tại từng component view lẻ. Bắt buộc gọi qua Client Hook/SDK tập trung.
- **CẤM**: QC ký Gate 4 khi bộ Test Matrix chưa bao phủ 100% các màn hình trong Surface Impact Matrix của BA. Kiểm thử bắt buộc tuân thủ 4 tầng: (1) Unit & Invariants $\rightarrow$ (2) API Contracts $\rightarrow$ (3) DB Integration trên Postgres thật $\rightarrow$ (4) E2E Playwright & Scoped RBAC Fuzzing.

### Điều 8: Kỷ Luật Gác Cổng Task & Pull Request (Stage-Gate Review Discipline)
- **CẤM**: Tích `[x]` vào `tasks.md` khi chưa tự rà soát theo `TEMPLATE-task-review-checklist.md` và chưa có Unit Test cho 100% `BR-*`.
- **CẤM**: Tạo PR mà không sử dụng template `.github/pull_request_template.md` hoặc để trống/tick hình thức mà không có bằng chứng test (Test Evidence).
- **CẤM**: Merge bất kỳ PR nào vào nhánh chính khi chưa có **Gate 3 (TechLead / SA Approve qua `pr-review-guard`)** và **Gate 4 (QC Verification PASS)**.

---

## 3. Giao Thức Rà Soát Khi Được Gọi (`/workflow-guard`)

Khi nhận lệnh, Agent thực hiện rà soát nhanh qua 4 bước:

### Bước 1: Xác định Ngữ cảnh Hoạt động
- Đang ở thư mục gốc (Tầng Nghiệp vụ) hay trong `SourceCode/` (Tầng Kỹ thuật)?
- Kiểm tra file đang mở hoặc nội dung vừa thảo luận.

### Bước 2: Kiểm tra Vi phạm Quy trình
- Có tài liệu nào đang bị thiếu mã truy vết không?
- Có Epic nào có code mà chưa có `spec.md` / `tasks.md` không?
- Có task nào đánh dấu `[x]` mà chưa có test tương ứng không?
- Bảng `Specification/BA_PROGRESS_TRACKER.md` và `SourceCode/specs/ROADMAP.md` có được đồng bộ không?

### Bước 3: Xuất Bản Kết Quả Rà Soát (Verdict)
Phản hồi theo định dạng chuẩn:
```markdown
### 🛡️ KẾT QUẢ RÀ SOÁT QUY TRÌNH NACENTECH
- **Ngữ cảnh hiện tại**: [Tầng Nghiệp vụ / Tầng Kỹ thuật]
- **Trạng thái tuân thủ**: [✅ ĐẠT CHUẨN / ⚠️ PHÁT HIỆN LỖ HỔNG / ❌ VI PHẠM QUY TRÌNH]

#### 1. Các điểm đã tuân thủ tốt:
- ...

#### 2. Các điểm cần khắc phục ngay (nếu có):
- ...

#### 3. Lệnh / Hành động tiếp theo bắt buộc:
- Gõ: `...` (ví dụ: `/speckit-plan`, `/nacen-srs-to-speckit`, `XÁC NHẬN MỤC 3`...)
```
