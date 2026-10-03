---
name: nacen-workflow-guard
description: Người gác cổng quy trình NacenTech (Workflow & Quality Guardian). Kiểm tra, nhắc nhở và cưỡng chế toàn bộ thành viên và AI Agent tuân thủ nghiêm ngặt quy trình 2 tầng (BA 7 mục có cổng duyệt, Handoff Traceability, Spec Kit tuần tự).
metadata:
  short-description: Rà soát và cưỡng chế tuân thủ quy trình vận hành NacenTech
---

# NacenTech Workflow & Quality Guardian (`nacen-workflow-guard`)

## 1. Mục Tiêu & Trách Nhiệm Tối Cao

Skill này đóng vai trò **Người Giám Sát Tuân Thủ Tuyệt Đối** đối với mọi hoạt động của con người và AI Agent trong toàn bộ dự án NacenTech.

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

---

## 3. Giao Thức Rà Soát Khi Được Gọi (`/nacen-workflow-guard`)

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
