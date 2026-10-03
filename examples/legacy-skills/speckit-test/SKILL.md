---
name: "speckit-test"
description: "Chuyên gia Thiết kế & Thực thi Kiểm thử Toàn Diện (Testing Specialist): Tự động xây dựng Unit Test (Vitest), Database Integration Test, và End-to-End Visual QA (Playwright) đạt chuẩn Quality Gate 100% pass."
compatibility: "Requires Node.js, Vitest/Jest, and Playwright in project"
metadata:
  author: "github-spec-kit"
  source: "custom/speckit-test"
---

## User Input

```text
$ARGUMENTS
```

Tham số đầu vào là tên module, tính năng, hoặc Epic cần viết/chạy test (Ví dụ: `Auth Module`, `VietQR Payment`, `Admin CMS`, `Visual QA`).

---

## 1. Triết Lý Kiểm Thử (Testing Philosophy)

Hệ thống tuân thủ mô hình **Testing Pyramid** 3 tầng nghiêm ngặt:

```text
          ▲
         / \     Tầng 3: Playwright E2E & Visual QA (Giao diện, luồng người dùng, ảnh chụp)
        /───\
       /     \   Tầng 2: Database Integration Test (Transaction ACID, Outbox, API routes)
      /───────\
     /         \ Tầng 1: Unit Test (Vitest) - Business Logic, Formatter, Validator, Security
    ─────────────
```

- **Zero Assumption (Không giả định)**: Mọi logic nghiệp vụ cốt lõi (tính tiền, phân quyền, mã hóa) phải có test kiểm chứng.
- **Real Database over Fake Mocks**: Với tầng Integration Test, ưu tiên kết nối database test thật (chạy trong transaction hoặc dọn dẹp sạch sau `afterAll`) thay vì mock mọi thứ dẫn tới lỗi ngầm khi deploy.
- **Visual Proof**: Với giao diện, bắt buộc có ảnh chụp màn hình Playwright đối chiếu trực quan (Visual QA).

---

## 2. Quy Chuẩn 3 Tầng Test Chi Tiết

### Tầng 1: Unit Test (`*.spec.ts` cạnh module)
- **Công cụ**: Vitest / Jest.
- **Phạm vi**:
  - State machine, transitions, validators (Zod schemas).
  - Utility functions, formatters (tiền tệ, ngày tháng, phone).
  - Thuật toán mã hóa / giải mã (AES-256-GCM, SHA-256).
- **Nguyên tắc**: Chạy cực nhanh (< 10ms/test), không phụ thuộc network ngoài.

### Tầng 2: Database Integration Test (`src/server/db/*.spec.ts`)
- **Phạm vi**:
  - Giao tác cơ sở dữ liệu ACID đa bảng (Database Transaction).
  - Transactional Outbox Pattern (đảm bảo ghi event đồng bộ).
  - Các ràng buộc duy nhất (Unique constraints, Foreign keys).
- **Vòng đời**:
  - `beforeAll`: Chuẩn bị dữ liệu mẫu cô lập.
  - `afterAll`: Dọn dẹp sạch sẽ (cleanup) và đóng kết nối pool.

### Tầng 3: Playwright E2E & Visual QA (`tests/e2e/*.spec.ts`)
- **Phạm vi**:
  - Luồng thao tác của người dùng từ đầu đến cuối (User Journeys).
  - Đa ngôn ngữ (Language Switcher Parity).
  - Đa kích thước màn hình (Desktop 1440px, Mobile 390px PWA, Tablet).
  - Chụp ảnh Visual QA độ phân giải cao Retina (lưu vào `docs/screenshots/<epic>/`).

---

## 3. Các Lệnh Thực Thi Tiêu Chuẩn

```bash
# 1. Chạy toàn bộ Unit & Integration test
pnpm test

# 2. Chạy test cho một file cụ thể
pnpm test path/to/file.spec.ts

# 3. Chạy Playwright E2E / Visual QA
pnpm exec playwright test tests/e2e/<test-file>.spec.ts

# 4. Kiểm tra TypeScript toàn dự án
pnpm typecheck
```

---

## 4. Quality Gate Bắt Buộc Trước Khi Nghiệm Thu

Một tính năng chỉ được đánh dấu hoàn thành khi thỏa mãn:
1. `pnpm typecheck` trả về 0 errors (Exit code 0).
2. `pnpm test` đạt 100% test suites passed (0 failures).
3. Playwright Visual QA chụp ảnh màn hình lưu vào thư mục tài liệu để người dùng nghiệm thu.
