---
name: qa-shadow-sentinel
description: "Bóng ma kiểm toán độc lập (Shadow QA Sentinel): Quét Git Diff, phát hiện vi phạm Gate 2 (code khi chưa có plan), săn tìm mock ngầm (Zero-Mock), đo lường dung lượng Token Context (ngưỡng 60%-80%) và kích hoạt quy trình giải phóng ngữ cảnh an toàn."
---

# Kỹ Năng: Shadow QA Sentinel (Bóng Ma Giám Sát Độc Lập)

## Mục Đích
Kỹ năng này cho phép Agent QA hoạt động trên một luồng riêng biệt (Context Isolation) để "soi" hành vi làm việc của Agent Dev và QC, ngăn chặn hiện tượng làm ẩu do tràn context hoặc đốt cháy giai đoạn.

## Các Chốt Chặn Kiểm Tra Tự Động
Kích hoạt kịch bản kiểm toán toán học:
```bash
./scripts/qa-shadow-sentinel.sh
```

---

### 1. Đo lường Token Context (Context Telemetry)
- Trích xuất trực tiếp số lượng tokens từ transcript log phiên làm việc.
- **Ngưỡng Vàng (>= 60% / >= 80k tokens)**: Cảnh báo sớm. Khuyến nghị dứt điểm task hiện tại, không kéo thêm file rác vào chat.
- **Ngưỡng Đỏ (>= 80% / >= 120k tokens)**: Báo động khẩn cấp, khóa nhận task mới, yêu cầu kích hoạt **Quy trình 3 bước giải phóng an toàn (Safe Context Evacuation)**:
  1. Ghi điểm lưu trạng thái: `specs/[epic-id]/.session_checkpoint.md`.
  2. Commit Git toàn bộ code đã làm để bảo toàn công sức.
  3. Kích hoạt `/compact` hoặc mở Clean Session mới để chạy tiếp sạch sẽ.

---

### 2. Kiểm toán Gate 2 (Chống Code Chay)
- Kiểm tra trạng thái Git (`git status --porcelain`).
- Nếu phát hiện file mã nguồn (`.cs`, `.tsx`, `.ts`, `.py`, `.go`, `.java`...) bị sửa đổi hoặc tạo mới **MÀ** thư mục `specs/[epic-id]/` chưa tồn tại file `plan.md` hoặc `tasks.md` chưa được sinh:
  - $\rightarrow$ **CẮT LUỒNG DEV NGAY LẬP TỨC**. Bắt buộc hoàn tất `sa-plan` và `dev-tasks` trước khi gõ code.

---

### 3. Săn Lùng Mock Ngầm (Zero-Mock Detector)
- Quét các regex pattern trong diff mã nguồn: `fakeItem`, `fakeCode`, `fakeUser`, `mockData`, `dummyData`, fallback tự sinh dữ liệu giả trong khối `catch` hoặc nhánh `else`:
  - $\rightarrow$ **ĐÁNH FAIL GATE 3/4 NGAY VÒNG 1**. Yêu cầu kết nối API/DB thật.

---

### 4. Thẩm Định Bài Test QC (Deep DB Assertion & No Page Route)
- Kiểm tra bài test E2E / Integration trong `tests/`:
  - Tuyệt đối cấm sử dụng `page.route()` hoặc `route.fulfill()` để mớm dữ liệu giả cho UI.
  - Tuyệt đối cấm inject mock auth token vào localStorage.
  - Mọi thao tác submit / lưu dữ liệu bắt buộc phải có câu lệnh truy vấn CSDL thật (`SELECT ... FROM ... WHERE ...` hoặc query DB client) để đối soát dòng dữ liệu thực tế.
  - Cấm Shallow Assertions (`is_visible()`, `toBeInTheDocument()`) mà không có assertion dữ liệu thật hoặc hành vi tương tác thật.
