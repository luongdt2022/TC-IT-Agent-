---
name: dev-unit
description: "Viết mã kiểm thử đơn vị (Unit Tests) theo kỷ luật TDD cho 100% các Quy tắc Nghiệp vụ (BR-*) được định nghĩa trong spec.md. Đảm bảo chạy nhanh, độc lập và 100% pass."
---

# Kỹ Năng: dev-unit (Kiểm Thử Đơn Vị TDD Cho Quy Tắc Nghiệp Vụ)

> **Role Chịu Trách Nhiệm**: Dev Agent (`dev`) — Senior Full-Stack Developer.  
> **Cổng Kiểm Soát**: Pre-Commit Quality Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Danh sách Business Rules (`BR-*`) trong `specs/[epic-id]/spec.md`.
- **Target Output Directory**: `tests/unit/` (Đặt tên theo chuẩn `[Feature]Tests.cs` hoặc `[feature].test.ts`).
- **NGHIÊM CẤM**: Không tạo các file test bên trong `src/` hoặc ở thư mục gốc (`root`).

---

## 2. KỶ LUẬT TDD BẤT BIẾN (RED ➔ GREEN ➔ REFACTOR)

1. **Chuẩn Đặt Tên Test Case**:
   - `[TênHàm/NghiệpVụ]_[ĐiềuKiệnĐầuVào]_[KếtQuảKỳVọng]`
   - Ví dụ: `ValidateOrder_WhenTotalAmountIsZero_ShouldThrowDomainException()`
2. **Quy Tắc AAA (Arrange - Act - Assert)**:
   - **Arrange**: Chuẩn bị dữ liệu mẫu và mock dependencies.
   - **Act**: Thực thi hàm nghiệp vụ cần kiểm thử.
   - **Assert**: Kiểm tra kết quả trả về khớp chính xác với `BR-*`.
3. **Độ Bao Phủ Bắt Buộc (100% BR Coverage)**:
   - Từng quy tắc nghiệp vụ `BR-*` trong `spec.md` bắt buộc phải có ít nhất:
     - 1 test case cho luồng hợp lệ (Happy Path).
     - 1 test case cho điều kiện biên (Boundary Path).
     - 1 test case cho trường hợp không hợp lệ và ném exception mong muốn (Negative Path).

---

## 3. THỰC THI & BÁO CÁO
- Chạy lệnh test đơn vị trong terminal.
- Đảm bảo toàn bộ test case chạy hoàn tất trong vòng dưới vài giây (Fast execution).
- Chỉ khi 100% Unit test xanh mới được đánh dấu hoàn tất task tương ứng trong `tasks.md`.
