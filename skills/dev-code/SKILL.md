---
name: dev-code
description: "Thực thi lập trình tuần tự bám sát 1:1 theo từng task trong tasks.md. Đảm bảo clean code, không sinh code thừa, cập nhật checkbox [x] sau khi kiểm chứng thành công."
---

# Kỹ Năng: dev-code (Lập Trình Thực Thi Tuần Tự Bám Sát Task)

> **Role Chịu Trách Nhiệm**: Dev Agent (`dev`) — Senior Full-Stack Developer.  
> **Cổng Kiểm Soát**: Implementation & Code Execution.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Danh sách task tại `specs/[epic-id]/tasks.md` và kế hoạch tại `specs/[epic-id]/plan.md`.
- **Target Output Directory**: `src/` theo đúng phân tầng Clean Architecture:
  - `src/Domain/` (Entities, Value Objects, Domain Exceptions)
  - `src/Application/` (Features, Commands, Queries, DTOs, Validators)
  - `src/Infrastructure/` (Persistence, Configurations, Repositories)
  - `src/Presentation/` (Controllers, Filters, Endpoints)
  - `src/WebApp/` (Components, Pages, Hooks, Services)
- **NGHIÊM CẤM**: Tuyệt đối không tạo file code hoặc script chạy thử ở thư mục gốc (`root`).

---

## 2. NGUYÊN TẮC LẬP TRÌNH BẤT BIẾN (CODING INVARIANTS)

1. **Tuân Thủ Tuần Tự Từng Task (One Task at a Time)**:
   - Đọc task tiếp theo mang trạng thái `[ ]` trong `specs/[epic-id]/tasks.md`.
   - Viết code hoàn thiện cho duy nhất task đó.
   - Chạy lệnh kiểm chứng (build code hoặc chạy test).
   - Chỉ khi kiểm chứng thành công mới cập nhật checkbox thành `[x]`.
2. **Không Tự Ý Đoán Mò Hay Chế Tính Năng**:
   - Nếu phát hiện thiếu dữ liệu hoặc spec mơ hồ, dừng lại và kích hoạt trao đổi, tuyệt đối không tự bịa logic.
3. **Không Chèn Metadata Rác Vào Code**:
   - Nghiêm cấm viết comment dạng: `// Handled by Dev Agent sprint 3` hoặc `// AI generated`. Comment chỉ giải thích logic *tại sao (Why)* khi thuật toán phức tạp.
4. **Bảo Vệ Ranh Giới Clean Architecture**:
   - Tuân thủ nghiêm ngặt quy định: Không rò rỉ DbContext lên Controller, không import tầng ngoài vào Domain.

---

## 3. CẬP NHẬT TIẾN ĐỘ THỰC THI
Sau khi hoàn thành từng nhóm task:
- Kiểm tra tính hội tụ (Converge Check): Đối chiếu mã nguồn thực tế với `specs/[epic-id]/spec.md`.
- Báo cáo kết quả ngắn gọn cho PO/PM và bàn giao cho TL/SA rà soát đối kháng (`sa-review`).
