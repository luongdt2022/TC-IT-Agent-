---
name: bmad-qa-generate-e2e-tests
description: "Tự Động Sinh Kịch Bản Kiểm Thử Đầu Cuối E2E (Automated E2E Test Generator). Tự động phân tích Acceptance Criteria trong spec.md và hành trình người dùng User Journey để sinh mã kiểm thử Playwright TypeScript tự động bao phủ trọn vẹn 5 trạng thái UX."
metadata:
  short-description: Tự động sinh trọn bộ kịch bản kiểm thử E2E Playwright
---

# Automated E2E Test Suite Generator (`bmad-qa-generate-e2e-tests`)

Skill chuyên trách dành cho **Agent QC** để tự động hóa kiểm thử giao diện và luồng người dùng trên nền tảng Playwright Test.

## 1. NGUYÊN TẮC THIẾT KẾ TEST SUITE E2E
1. **Kiểm Thử Theo Luồng Giá Trị (User Journey Centric)**:
   - Không kiểm tra click nút đơn lẻ; kiểm tra trọn vẹn một kịch bản từ đầu đến cuối (ví dụ: Chuyên gia đăng ký qua Zalo Mini App $\rightarrow$ Hệ thống gửi thông báo $\rightarrow$ Admin duyệt trên Web Portal $\rightarrow$ Hồ sơ hiển thị trên Sàn).
2. **Bao Phủ Trọn Vẹn 5 Trạng Thái UX**:
   - `Empty State`: Khi chưa có dữ liệu $\rightarrow$ Kiểm tra có hiển thị hình minh họa và nút hành động kêu gọi không.
   - `Loading State`: Khi đang gọi API $\rightarrow$ Kiểm tra Skeleton Loader có hiển thị đúng vị trí không.
   - `Error State`: Khi ngắt mạng hoặc API trả 500 $\rightarrow$ Kiểm tra thông báo lỗi thân thiện và nút "Thử lại".
   - `Success State`: Khi tải dữ liệu thành công $\rightarrow$ Kiểm tra hiển thị đúng và đủ số bản ghi.
   - `Partial State`: Khi phân trang hoặc tải thêm $\rightarrow$ Kiểm tra infinite scroll / load more.

## 2. QUY TRÌNH TỰ ĐỘNG SINH CODE TEST
1. **Đọc Spec SSOT**: Quét `SourceCode/specs/<epic>/spec.md` lấy danh sách User Stories & Acceptance Criteria (`AC-01`, `AC-02`...).
2. **Sinh Page Object Model (POM)**:
   - Tạo file class đại diện cho trang (ví dụ: `ExpertProfilePage.ts`) chứa các bộ chọn locator chống vỡ (`data-testid`).
3. **Sinh Kịch Bản Kiểm Thử Playwright**:
   - Viết các file spec trong `SourceCode/frontend/tests/e2e/<epic>.spec.ts`.
   - Tự động chèn lệnh chụp ảnh màn hình so sánh thị giác (`await expect(page).toHaveScreenshot()`).
