---
name: ec-e2e
description: "Tự động sinh kịch bản kiểm thử đầu cuối E2E (Playwright TypeScript) từ Acceptance Criteria trong spec.md. Bao phủ trọn vẹn hành trình người dùng và 5 trạng thái UX kèm chụp ảnh màn hình Visual QA."
---

# Kỹ Năng: ec-e2e (Tự Động Sinh Kịch Bản Playwright E2E)

> **Role Chịu Trách Nhiệm**: EC Agent (`ec`) — Edge-Case Hunter & QC Specialist.  
> **Cổng Kiểm Soát**: Gate 4 End-to-End Visual Verification.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Danh sách tiêu chí nghiệm thu (`AC-*`) trong `specs/[epic-id]/spec.md`.
- **Target Output Directory**: `tests/e2e/` (Ví dụ: `tests/e2e/auth.spec.ts`, `tests/e2e/cart.spec.ts`).
- **Thư mục ảnh chụp màn hình**: `tests/e2e/screenshots/`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. NGUYÊN TẮC THIẾT KẾ KỊCH BẢN PLAYWRIGHT E2E

1. **Tuân Thủ Mô Hình Page Object Model (POM)**:
   - Tách biệt giữa selector giao diện và logic kiểm thử hành vi.
2. **Bao Phủ 5 Trạng Thái UX**:
   - Test kiểm tra hiển thị Skeleton khi mạng chậm (`test.use({ offline: false })` + Network throttling).
   - Test kiểm tra màn hình rỗng (`Empty State`).
   - Test kiểm tra thông báo lỗi khi nhập sai (`Error State`).
   - Test kiểm tra luồng hoàn tất thành công (`Success State`).
3. **Chụp Ảnh Màn Hình Tự Động Phục Vụ Nghiệm Thu (Visual QA Screenshots)**:
   - Tại mỗi bước quan trọng, chụp ảnh màn hình và lưu vào `tests/e2e/screenshots/[epic-id]-[step].png` để con người / PO có bằng chứng nghiệm thu trực quan.

---

## 3. MẪU KỊCH BẢN PLAYWRIGHT TIÊU CHUẨN

```typescript
import { test, expect } from '@playwright/test';

test.describe('EPIC-01: Authentication Flow', () => {
  test('AC-01: Should login successfully with valid credentials and redirect to dashboard', async ({ page }) => {
    // 1. Arrange & Navigate
    await page.goto('/login');
    await expect(page.locator('h1')).toHaveText('Đăng Nhập');

    // 2. Act
    await page.fill('input[name="email"]', 'admin@example.com');
    await page.fill('input[name="password"]', 'P@ssword123!');
    await page.click('button[type="submit"]');

    // 3. Assert & Screenshot
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('.welcome-banner')).toBeVisible();
    await page.screenshot({ path: 'tests/e2e/screenshots/auth-login-success.png' });
  });

  test('AC-02: Should show error message when credentials are invalid', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'wrong@example.com');
    await page.fill('input[name="password"]', 'WrongPass!');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-toast')).toBeVisible();
    await page.screenshot({ path: 'tests/e2e/screenshots/auth-login-invalid.png' });
  });
});
```
