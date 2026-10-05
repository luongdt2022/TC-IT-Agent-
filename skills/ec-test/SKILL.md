---
name: ec-test
description: "Chuyên gia Thiết kế & Thực thi Kiểm thử Toàn diện (Testing Specialist): Tự động điều phối trọn bộ kiểm thử 4 tầng (Unit Test, API Contract Test, Database Integration Test, Playwright E2E & Scoped RBAC Fuzzing) đạt chuẩn Quality Gate 4 (100% Green)."
---

# Kỹ Năng: ec-test (Điều Phối Kiểm Thử 4 Tầng — Quality Gate 4)

> **Role Chịu Trách Nhiệm**: EC Agent (`ec`) — Edge-Case Hunter & QC Specialist.  
> **Cổng Kiểm Soát**: Quality Gate 4 Verification Gatekeeper.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input Bắt Buộc**:
  1. Toàn bộ mã nguồn `src/` và bộ test cases tại `tests/` (`tests/unit/`, `tests/contracts/`, `tests/integration/`, `tests/e2e/`).
  2. **Cross-Surface Impact Matrix** từ Step 0 của BA (danh sách tất cả các màn hình UI, API, DB bị tác động).
- **Target Output File**: `docs/decisions/GATE4_VERIFICATION.md`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`). Cấm ký duyệt Gate 4 nếu Test Matrix chưa bao phủ đủ 100% các màn hình trong Surface Impact Matrix.

---

## 2. CHU TRÌNH KIỂM THỬ 4 TẦNG BẮT BUỘC (4-TIER TESTING PYRAMID)

```
             / \
            /   \      TẦNG 4: Playwright E2E & Scoped RBAC Fuzzing (ec-hunt / ec-fuzz)
           / E2E \     - Hành trình người dùng & 5 UX States (<Async>)
          /-------\    - Fuzzing ma trận phân quyền, giả lập xâm nhập ngoài phạm vi
         / Integr- \   TẦNG 3: Database Integration Tests (PostgreSQL Container thật)
        /   ation   \  - EF Core Migrations, Unique constraints, Transaction rollback
       /-------------\ TẦNG 2: API Contracts & Architecture Boundary
      /   Contract    \ - DTO Shape, Error status code (400, 403), Clean Arch sentinel
     /-----------------\ TẦNG 1: Unit & Invariants Tests (BR-*)
    /    Unit Tests     \- 100% Quy tắc nghiệp vụ BR-*, AggregateRoot life-cycle
   /---------------------\
```

1. **Tầng 1 - Unit & Invariants Tests**:
   - Chạy toàn bộ test nghiệp vụ trong `tests/unit/` và `tests/invariants/`.
   - Tiêu chuẩn: 100% test case pass, kiểm chứng toàn bộ các hàm domain model, validation logic và enum chuẩn.
2. **Tầng 2 - API Contract Tests**:
   - Chạy test kiểm tra hợp đồng API (`tests/contracts/`): Format DTO, ranh giới phân tầng, cấu trúc phản hồi lỗi `ValidationException`.
3. **Tầng 3 - Database Integration Tests**:
   - Chạy test tương tác CSDL thực tế (sử dụng Docker Postgres / Testcontainers).
   - Kiểm tra nạp seed dữ liệu, kích hoạt unique constraints, bảo toàn khóa ngoại không bị mồ côi (orphan records).
4. **Tầng 4 - Playwright E2E Visual QA & Scoped RBAC Fuzzing**:
   - Khởi động web dev server, chạy headless browser kịch bản `tests/e2e/` bao phủ trọn vẹn các màn hình từ Surface Impact Matrix.
   - Săn lỗi biên (`ec-hunt`): Bơm payload cũ/lỗi thời, ký tự đặc biệt, chuỗi rỗng.
   - Fuzzing phân quyền (`ec-fuzz`): Kiểm tra từ chối `403 Forbidden` khi người dùng không đủ quyền.

---

## 3. QUY TẮC ĐỐI SOÁT ĐẦU VÀO INPUT STUDY (SCREEN COVERAGE GUARD)

**CẢNH BÁO CHỐNG LỖI MÙ CỤC BỘ (SCOPE TUNNEL VISION)**:
- QC tuyệt đối **KHÔNG ĐƯỢC CHỈ ĐỌC MỖI FILE SPEC HẸP** của Epic để lập test.
- Khi tiếp nhận Handoff, QC bắt buộc phải chạy lệnh kiểm tra chéo:
  ```bash
  # Quét tìm tất cả các file UI có tiêu thụ thực thể hoặc danh mục đang test:
  grep -rn "<KEYWORD>" src/
  ```
- **Điều kiện tiên quyết để mở Gate 4**: Mọi màn hình xuất hiện trong kết quả quét (Trang chủ, Portal, Dashboard, Layout, Login...) đều phải có ít nhất 1 test case hoặc visual assertion kiểm tra tính nhất quán dữ liệu.

---

## 4. CẤU TRÚC BIÊN BẢN GATE4_VERIFICATION.MD

```markdown
# BIÊN BẢN KIỂM ĐỊNH CHẤT LƯỢNG KỸ THUẬT (GATE 4 VERIFICATION)

- **Mã Epic**: [EPIC-ID]
- **Thời gian thẩm định**: [YYYY-MM-DD HH:mm]
- **Người thẩm định**: EC Agent (QC Specialist)

## 1. BẢNG TỔNG HỢP KẾT QUẢ KIỂM THỬ 4 TẦNG
| Tầng Kiểm Thử | Tổng Số Tests | Passed | Failed | Thời Gian Chạy | Đánh Giá |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tầng 1: Unit & Invariants** | 80 | 80 | 0 | 120ms | [PASS 100%] |
| **Tầng 2: API Contracts** | 37 | 37 | 0 | 5.2s | [PASS 100%] |
| **Tầng 3: DB Integration** | 7 | 7 | 0 | 500ms | [PASS 100%] |
| **Tầng 4: Playwright E2E & RBAC**| 12 | 12 | 0 | 14.5s | [PASS 100%] |

## 2. MA TRẬN ĐỘ PHỦ MÀN HÌNH (SCREEN COVERAGE MATRIX)
- Số màn hình phát hiện qua Surface Scan: [N màn hình]
- Số màn hình đã kiểm chứng thực tế: [N / N] (100% Khớp)

## 3. KẾT QUẢ SĂN LỖI BIÊN & BẢO MẬT
- Săn lỗi biên (`ec-hunt`): 0 lỗi Blocker/Critical/Major chưa khắc phục.
- Fuzzing bảo mật (`ec-fuzz`): [RBAC & SCOPE COMPLIANT].

## 4. PHÁN QUYẾT GATE 4
- **KẾT QUẢ**: [CHÍNH THỨC PHÊ DUYỆT QUALITY GATE 4 - PASS]
- **Bàn giao**: Chuyển giao toàn bộ hồ sơ kiểm định sang PO/PM Agent để tiến hành ký nghiệm thu xuất xưởng (Gate 5).
```
