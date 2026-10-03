---
name: nacen-srs-to-speckit
description: Cầu nối chuyển giao (Handoff Bridge) tự động bóc tách tài liệu SRS 7 mục đã phê duyệt sang Epic kỹ thuật (spec.md, plan, tasks) chuẩn Spec Kit Framework trong SourceCode/specs/.
metadata:
  short-description: Chuyển giao SRS nghiệp vụ sang Epic kỹ thuật trong SourceCode/specs/
---

# NacenTech SRS to Spec Kit Handoff Skill

## 1. Mục Tiêu & Sứ Mệnh Cốt Lõi

Skill này đóng vai trò **Cầu Nối Huyết Mạch (The Handoff Bridge)** giữa tầng Nghiệp vụ (`Specification/SRS/`) và tầng Kỹ thuật (`SourceCode/specs/`).

Sau khi một tài liệu SRS 7 mục hoàn thành biên soạn và đạt trạng thái **HỘI TỤ (CONVERGED)** theo quy trình của `ba-srs-copilot`, skill này thực hiện nhiệm vụ:
1. Đọc và phân tích toàn văn tài liệu SRS nguồn.
2. Trích xuất toàn bộ các thực thể định danh: `REQ-`, `BR-`, `DB-`, `UI-`, `API-`, `NFR-`.
3. Khởi tạo cấu trúc Epic kỹ thuật tại `SourceCode/specs/<epic-code>-<slug>/`.
4. Soạn thảo `spec.md` kỹ thuật bám chuẩn `SourceCode/.specify/templates/spec-template.md`, chuyển đổi Functional Requirements thành User Stories (P1, P2, P3), Acceptance Scenarios (Gherkin Given-When-Then) và Edge Cases.
5. Tự động đồng bộ và đăng ký vào:
   - **`SourceCode/specs/ROADMAP.md`**: Cập nhật Master Registry và Change Log.
   - **`SourceCode/specs/TRACEABILITY.md`**: Thiết lập liên kết truy vết 2 chiều khép kín.
   - **`SourceCode/.specify/feature.json`**: Trỏ feature hiện hành vào Epic mới tạo.

---

## 2. Tiêu Chuẩn Đầu Vào (Pre-conditions)

Chỉ được thực thi chuyển giao khi thỏa mãn các điều kiện:
1. File SRS nằm tại `Specification/SRS/` (hoặc đường dẫn do người dùng chỉ định).
2. Tài liệu đã có đầy đủ **7 mục chuẩn hóa** và vượt qua kiểm tra hội tụ theo `BA Agent/references/convergence-checklist.md`.
3. Không còn nhãn `[PROPOSAL]` nào chưa được duyệt (tất cả phải là `[VERIFIED]` hoặc `[CONFIRMED]`).

---

## 3. Quy Trình Chuyển Giao 5 Bước Chi Tiết

### Bước 1: Đối soát & Trích xuất Dữ kiện (Extraction Phase)
- Đọc nội dung file SRS nguồn.
- Lập bảng danh mục các mã truy vết:
  - Danh sách `REQ-*`: Tên chức năng, vai trò người dùng, tiêu chí nghiệm thu.
  - Danh sách `BR-*`: Quy tắc nghiệp vụ, điều kiện biên, quy tắc TRL 1–9.
  - Danh sách `DB-*`: Cấu trúc thực thể và quan hệ bảng.
  - Danh sách `UI-*`: Màn hình và trạng thái UX cần có.
  - Danh sách `API-*`: Điểm cuối giao tiếp dữ liệu.
  - Danh sách `NFR-*`: Chỉ số hiệu năng, tải, bảo mật định lượng.

### Bước 2: Xác định Thư mục Epic & Cập nhật Context
- Xác định mã thứ tự Epic tiếp theo dựa trên `SourceCode/specs/ROADMAP.md` (ví dụ: `002-core-platform-iam`, `003-tech-product-catalog`...).
- Tạo thư mục đích: `SourceCode/specs/<epic-folder>/`.
- Cập nhật `.specify/feature.json`:
  ```json
  {
    "feature_directory": "specs/<epic-folder>"
  }
  ```

### Bước 3: Soạn thảo `spec.md` Kỹ Thuật
- Tạo file `SourceCode/specs/<epic-folder>/spec.md` theo cấu trúc:
  - **Header**: Tên Epic, tham chiếu nguồn `../Specification/SRS/<tên-file-srs>.md`, phiên bản, ngày handoff.
  - **User Stories & Acceptance Scenarios**: Phân cấp ưu tiên P1 (Core Happy Path), P2 (Advanced/Filter), P3 (Polish/Nice-to-have). Mỗi story có kịch bản Given-When-Then đối soát trực tiếp mã `REQ-` và `BR-`.
  - **Functional Requirements**: Ánh xạ chi tiết bảng `REQ-*` và quy tắc `BR-*`.
  - **Edge Cases & Failure Modes**: Kịch bản lỗi, mất mạng, dữ liệu không hợp lệ trích xuất từ Mục 5 của SRS.
  - **Traceability Mapping**: Bảng tổng hợp đối soát 1:1 giữa mã SRS và spec kỹ thuật.

### Bước 4: Đồng bộ Master Roadmap & Ma Trận Truy Vết
- Mở `SourceCode/specs/ROADMAP.md`:
  - Thêm dòng Epic mới vào Bảng 1 với trạng thái `⚪ Dự Kiến`.
  - Thêm dòng vào Bảng 3 (Lịch sử thay đổi) ghi nhận ngày handoff từ SRS sang Spec Kit.
- Mở `SourceCode/specs/TRACEABILITY.md`:
  - Cập nhật ánh xạ giữa mã SRS và thư mục Epic tương ứng.

### Bước 5: Báo cáo Nghiệm thu Chuyển giao (Handoff Summary)
- Xuất bản báo cáo ngắn gọn cho người dùng gồm:
  1. Đường dẫn thư mục Epic đã tạo: `SourceCode/specs/<epic-folder>/spec.md`.
  2. Số lượng `REQ-`, `BR-`, `DB-`, `API-` đã được chuyển đổi trọn vẹn.
  3. Lệnh gợi ý tiếp theo để lập trình viên hoặc AI thực thi tầng kỹ thuật:
     ```text
     cd SourceCode
     /speckit-plan          (để thiết kế architecture, DB schema, API contracts)
     /speckit-tasks         (để phân rã đầu việc tasks.md)
     /speckit-autopilot     (để chạy toàn trình từ plan đến code và test)
     ```
