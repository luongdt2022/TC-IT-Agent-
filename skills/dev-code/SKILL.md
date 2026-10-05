---
name: dev-code
description: "Thực thi lập trình tuần tự bám sát 1:1 theo từng task trong tasks.md. Đảm bảo clean code, không sinh code thừa, tuân thủ kỷ luật Pre-flight Grounding, chu trình nguyên tử 1 task/chu kỳ, và cập nhật checkbox [x] sau khi kiểm chứng thành công."
---

# Kỹ Năng: dev-code (Lập Trình Thực Thi Tuần Tự Bám Sát Task & Chống Ảo Giác)

> **Role Chịu Trách Nhiệm**: Dev Agent (`dev` / `tc-dev`) — Senior Full-Stack Developer.  
> **Cổng Kiểm Soát**: Implementation & Code Execution (Zero Hallucination & High Determinism).

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Danh sách task tại `specs/[epic-id]/tasks.md` và kế hoạch tại `specs/[epic-id]/plan.md`.
- **Target Output Directory**: Cấu trúc mã nguồn phân tầng chuẩn của dự án (`src/` hoặc `apps/`, `services/`).
- **NGHIÊM CẤM**: Tuyệt đối không tạo file code hoặc script chạy thử ở thư mục gốc (`root`).

---

## 2. QUY TẮC PRE-FLIGHT GROUNDING (CHỐNG ẢO GIÁC TRƯỚC KHI CODE)

Trước khi viết bất kỳ dòng mã nguồn nào, Dev Agent **BẮT BUỘC** thực hiện 2 thao tác neo dữ liệu (Grounding):
1. **Catalog / Component Grounding**:
   - Tra cứu Catalog thành phần dùng chung (như `components/ui/index.ts`, `Common/`, `Shared/`) để nắm toàn bộ component/hàm tiện ích có sẵn.
   - **Tuyệt đối không tự sáng tạo component mới** nếu trong catalog đã có sẵn hoặc có thể mở rộng. Cấm tái phát minh bánh xe.
2. **Database & Data Model Grounding**:
   - Tra cứu Schema / Data Models / Entity definitions của dự án để kiểm tra chính xác tên bảng, quan hệ và kiểu dữ liệu.
   - **Tuyệt đối không đoán mò field name** (ví dụ: `tenantId` vs `tenant_id`, `userId` vs `user_id`).

---

## 3. CHU TRÌNH THỰC THI NGUYÊN TỬ (ATOMIC EXECUTION - 1 TASK / 1 CYCLE)

Nhằm giữ độ dài context dưới 15,000 tokens và triệt tiêu hiện tượng "ngộ độc dữ liệu" dẫn đến ảo giác:
1. **Lấy 1 Task duy nhất**: Đọc đúng task tiếp theo mang trạng thái `[ ]` trong `specs/[epic-id]/tasks.md`.
2. **Viết mã tối thiểu**: Chỉ sửa hoặc tạo đúng file cần thiết cho task đó.
3. **Chốt chặn Compiler & TypeCheck (Bắt buộc chạy trước khi pass)**:
   - Chạy `./scripts/guard-rails.sh` (hoặc compiler / linter tương ứng của dự án) để máy tính tự động thẩm định:
     * 0 lỗi TypeCheck / Compilation.
     * 0 lỗi Schema validate.
     * 0 lỗi rò rỉ ranh giới kiến trúc.
4. **Đánh dấu hoàn thành**: Chỉ khi compiler và test thật sự chạy XANH mới chuyển checkbox thành `[x]`.
5. **Chuyển task**: Xóa bộ nhớ nháp, chuyển sang task kế tiếp.

---

## 4. NGUYÊN TẮC BẤT BIẾN (CORE INVARIANTS)

1. **Kỷ Luật "Red Test Bất Biến" (Test Immobility)**:
   - File test (`*.spec.*`, `*.test.*`, `tests/`) do QC (`tc-ec`) hoặc BA định nghĩa là **BẤT KHẢ XÂM PHẠM**.
   - Dev **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP** chỉnh sửa assertion hoặc nới lỏng điều kiện test để bài test pass giả tạo.
   - Mọi lỗi fail test bắt buộc phải sửa ở **mã nguồn thực thi** (Implementation Code).
2. **Bảo Vệ Ngữ Cảnh Bảo Mật & Phân Quyền (Security Invariant)**:
   - Mọi thao tác đọc/ghi CSDL bắt buộc phải kiểm tra và lọc theo phạm vi phân quyền hoặc tenant context của người dùng.
3. **Frontend Chuẩn Hóa 5 Trạng Thái UX**:
   - Màn tải dữ liệu bắt buộc thể hiện đủ các trạng thái (Đang tải · Rỗng · Lỗi · Có dữ liệu · Đang lưu) qua component chuẩn (ví dụ `<Async>`).
4. **Không Chèn Metadata Rác Vào Code**:
   - Nghiêm cấm viết comment dạng: `// Handled by Dev Agent sprint 3` hoặc `// AI generated`. Comment chỉ giải thích logic *tại sao (Why)* khi thuật toán phức tạp.
