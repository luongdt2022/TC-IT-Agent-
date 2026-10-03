---
name: ec-test
description: "Chuyên gia Thiết kế & Thực thi Kiểm thử Toàn diện (Testing Specialist): Tự động điều phối trọn bộ kiểm thử 3 tầng (Unit Test, Database Integration Test, Playwright E2E) đạt chuẩn Quality Gate 4 (100% Green)."
---

# Kỹ Năng: ec-test (Điều Phối Kiểm Thử 3 Tầng - Quality Gate 4)

> **Role Chịu Trách Nhiệm**: EC Agent (`ec`) — Edge-Case Hunter & QC Specialist.  
> **Cổng Kiểm Soát**: Quality Gate 4 Verification Gatekeeper.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Toàn bộ mã nguồn `src/` và bộ test cases tại `tests/` (`tests/unit/`, `tests/integration/`, `tests/e2e/`).
- **Target Output File**: `docs/decisions/GATE4_VERIFICATION.md`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. CHU TRÌNH KIỂM THỬ 3 TẦNG BẮT BUỘC (3-TIER TESTING PYRAMID)

```
             / \
            /   \      TẦNG 3: Playwright E2E (Hành trình người dùng & 5 UX States)
           / E2E \     - tests/e2e/*.spec.ts (Có ảnh chụp màn hình kiểm chứng)
          /-------\
         / Integr- \   TẦNG 2: Integration Tests (API Endpoints & Database Transaction)
        /   ation   \  - tests/integration/*
       /-------------\
      /     Unit      \ TẦNG 1: Unit Tests (100% Quy tắc nghiệp vụ BR-*)
     /     Tests       \- tests/unit/*
    /-------------------\
```

1. **Tầng 1 - Unit Tests**:
   - Chạy toàn bộ test nghiệp vụ trong `tests/unit/`.
   - Tiêu chuẩn: 100% test case pass, thời gian chạy dưới 10 giây.
2. **Tầng 2 - Database Integration Tests**:
   - Chạy test tương tác CSDL thực tế (sử dụng Docker Postgres / Testcontainers).
   - Kiểm tra commit/rollback transaction, khóa lạc quan concurrency token.
3. **Tầng 3 - Playwright E2E Visual QA**:
   - Khởi động web dev server, chạy headless browser kịch bản `tests/e2e/`.
   - Kiểm tra hiển thị đủ 5 trạng thái UX, chụp ảnh màn hình lưu vào `tests/e2e/screenshots/`.

---

## 3. CẤU TRÚC BIÊN BẢN GATE4_VERIFICATION.MD

```markdown
# BIÊN BẢN KIỂM ĐỊNH CHẤT LƯỢNG KỸ THUẬT (GATE 4 VERIFICATION)

- **Mã Epic**: [EPIC-ID]
- **Thời gian thẩm định**: [YYYY-MM-DD HH:mm]
- **Người thẩm định**: EC Agent (QC Specialist)

## 1. BẢNG TỔNG HỢP KẾT QUẢ KIỂM THỬ 3 TẦNG
| Tầng Kiểm Thử | Tổng Số Tests | Passed | Failed | Thời Gian Chạy | Đánh Giá |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tầng 1: Unit Test** | 35 | 35 | 0 | 1.8s | [PASS 100%] |
| **Tầng 2: Integration** | 12 | 12 | 0 | 4.2s | [PASS 100%] |
| **Tầng 3: Playwright E2E**| 6 | 6 | 0 | 11.5s | [PASS 100%] |

## 2. KẾT QUẢ SĂN LỖI BIÊN & BẢO MẬT
- Săn lỗi biên (`ec-hunt`): 0 lỗi Blocker/Critical/Major chưa khắc phục.
- Fuzzing bảo mật (`ec-fuzz`): [RBAC COMPLIANT].

## 3. PHÁN QUYẾT GATE 4
- **KẾT QUẢ**: [CHÍNH THỨC PHÊ DUYỆT QUALITY GATE 4 - PASS]
- **Bàn giao**: Chuyển giao toàn bộ hồ sơ kiểm định sang PO/PM Agent để tiến hành ký nghiệm thu xuất xưởng (Gate 5).
```
