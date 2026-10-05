---
name: ec-mutation
description: "Chuyên gia Kiểm thử Đột biến (Mutation Testing Specialist): Đánh giá chất lượng thực sự của bộ Unit Test bằng cách chủ động cấy lỗi đột biến (Mutants) vào mã nguồn. Đo lường Mutation Score (tỷ lệ bài test tiêu diệt được đột biến) để loại bỏ các bài test hình thức hoặc assertion vô hiệu."
---

# Kỹ Năng: ec-mutation (Kiểm Thử Đột Biến - Thử Lửa Bộ Test)

> **Role Chịu Trách Nhiệm**: EC Agent (`ec`) — Edge-Case Hunter & QC Specialist.  
> **Cổng Kiểm Soát**: Gate 4 Test Suite Integrity Gatekeeper.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Mã nguồn nghiệp vụ trong `src/` và bộ test tương ứng trong `tests/` hoặc `__tests__/`.
- **Target Output File**: `tests/mutation/MUTATION_TEST_REPORT.md` (hoặc `docs/decisions/MUTATION_TEST_REPORT.md`)
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. NGUYÊN LÝ HOẠT ĐỘNG (TEST YOUR TESTS)

Code coverage cao (90-100%) chưa chắc bài test đã có giá trị nếu Dev viết assertion qua loa (như `expect(true).toBe(true)`). Mutation Testing sinh ra để "thử lửa" chính các bài test:

```
[ Mã Nguồn Gốc ] ---> Bơm đột biến (Mutant) ---> [ Mã Nguồn Bị Đổi ]
                                                           |
                                           Chạy Unit Test tương ứng
                                                           |
                        +----------------------------------+----------------------------------+
                        |                                                                     |
                 Test BỊ FAIL (RED)                                                    Test VẪN PASS (GREEN)
                        |                                                                     |
         [ Mutant KILLED - Xuất Sắc ]                                           [ Mutant SURVIVED - Báo Động! ]
   (Bài test đã phát hiện ra lỗi sửa đổi)                                    (Bài test viết ẩu, không bắt được lỗi!)
```

### Các Dạng Đột Biến Tiêu Chuẩn (Mutators):
1. **Toán tử Số học & So sánh**: Đổi `+` thành `-`, `*` thành `/`, `>` thành `<=`, `===` thành `!==`.
2. **Logic Boolean**: Đổi `true` thành `false`, `&&` thành `||`.
3. **Giá trị Biên**: Đổi `0` thành `1`, chuỗi rỗng `""` thành `"xyz"`, mảng rỗng `[]` thành `[null]`.
4. **Loại bỏ Lời gọi Hàm (Block/Statement Removal)**: Xoá dòng gọi hàm `save()`, `auditLog()`, `commitTransaction()`.

### Tiêu Chuẩn Nghiệm Thu Mutation Score:
$$\text{Mutation Score} = \frac{\text{Số Mutants Bị Tiêu Diệt (Killed)}}{\text{Tổng Số Mutants Được Tạo Ra}} \times 100\%$$
- **Ngưỡng Xuất Xưởng (Gate 4 Requirement)**: $\text{Mutation Score} \ge 80\%$.
- Nếu Mutant sống sót (Survived) ở các quy tắc cốt lõi `BR-*`: Bắt buộc Dev phải viết lại assertion chặt chẽ hơn.

---

## 3. CẤU TRÚC BÁO CÁO MUTATION_TEST_REPORT.MD

```markdown
# BÁO CÁO KIỂM THỬ ĐỘT BIẾN (MUTATION TEST REPORT)

- **Thời gian**: [YYYY-MM-DD HH:mm]
- **Kiểm định viên**: EC Agent

## 1. CHỈ SỐ MUTATION TỔNG THỂ
- **Tổng số Mutants sinh ra**: 120
- **Mutants bị tiêu diệt (Killed)**: 104
- **Mutants sống sót (Survived)**: 16
- **Mutation Score**: **86.7%** -> [ĐẠT TIÊU CHUẨN GATE 4]

## 2. DANH SÁCH BÀI TEST YẾU (MUTANTS SURVIVED CẦN KHẮC PHỤC)
1. `src/modules/order/order.service.ts:45`: Đổi `status = 'ACTIVE'` thành `'CANCELLED'` nhưng bài test vẫn pass -> Test case thiếu assertion kiểm tra trạng thái đơn hàng.
```
