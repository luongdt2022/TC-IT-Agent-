---
name: sa-guard
description: "Vệ binh Kiến trúc & Cấu trúc Thư mục (Architecture & Directory Sentinel). Quét phát hiện vi phạm ranh giới Clean Architecture, rò rỉ CSDL lên API và kiểm tra kỷ luật thư mục chống rác (Zero-Tolerance Root Dumping)."
---

# Kỹ Năng: sa-guard (Vệ Binh Ranh Giới Kiến Trúc & Cấu Trúc Thư Mục)

> **Role Chịu Trách Nhiệm**: TL/SA Agent (`techlead-sa`) — Software Architect & Tech Lead.  
> **Cổng Kiểm Soát**: Gate 2, Gate 3, Gate 4 Lint & Sentinel Gatekeeper.

---

## 1. NGUYÊN TẮC KIỂM TRA RANH GIỚI KIẾN TRÚC (CLEAN ARCHITECTURE RULES)

Vệ binh `sa-guard` quét toàn bộ mã nguồn `src/` để phát hiện 4 nhóm vi phạm cấu trúc kinh điển:

1. **Rò Rỉ Hạ Tầng Lên Tầng Trên (Infrastructure Leaks)**:
   - Nghiêm cấm tầng `Presentation/API` hoặc `Application` gọi trực tiếp `DbContext` hay các thư viện Third-party cụ thể. Mọi tương tác phải qua Interface / Repository.
2. **Phụ Thuộc Ngược Từ Domain (Domain Inversion Violation)**:
   - Tầng `Domain` tuyệt đối KHÔNG ĐƯỢC chứa `using/import` bất kỳ namespace nào của `Application`, `Infrastructure`, hay `Presentation`. `Domain` là tầng độc lập tuyệt đối.
3. **Thao Tác CSDL Trực Tiếp Trên Controller**:
   - Nghiêm cấm viết câu lệnh SQL thô, query LINQ trực tiếp hoặc gọi HTTP client bên ngoài trong Controller. Controller chỉ nhận request, chuyển qua MediatR/Use Case và trả về response.
4. **Bypass Business Rules Validation**:
   - Mọi Command ghi dữ liệu bắt buộc phải đi qua lớp kiểm tra tính hợp lệ (FluentValidation / Business Rule Validator) trước khi chạm tới Entity.

---

## 2. NGUYÊN TẮC KIỂM TRA THƯ MỤC CHỐNG RÁC (ANTI-CLUTTER DIRECTORY LINTER)

`sa-guard` thực hiện kiểm tra kỷ luật cấu trúc thư mục dự án:

1. **Quét Thư Mục Gốc (`root`)**:
   - Nếu phát hiện file `.md` lẻ tẻ (ngoài `README.md`, `AGENTS.md`, `constitution.md`), file `.js/.ts/.py` chạy thử, hoặc file log vứt ở root $\rightarrow$ **CẢNH BÁO VI PHẠM & TỰ ĐỘNG DỌN DẸP**.
2. **Kiểm Tra Vị Trí File Test**:
   - Mọi file `*Test.cs`, `*.spec.ts`, `*.test.js` phải nằm trong `tests/` (`tests/unit/`, `tests/integration/`, `tests/e2e/`). Nếu nằm lạc trong `src/` $\rightarrow$ Đánh dấu lỗi cấu trúc.
3. **Kiểm Tra Vị Trí File Đặc Tả & Thiết Kế**:
   - Hồ sơ đề xuất giải pháp ➔ Bắt buộc nằm trong `docs/00-presale-proposal/`.
   - Thiết kế cơ sở ➔ Bắt buộc nằm trong `docs/01-basic-design/`.
   - Thiết kế chi tiết ➔ Bắt buộc nằm trong `docs/02-detail-design/`.
   - Spec Kit theo Epic ➔ Bắt buộc nằm trong `specs/[epic-id]/`.

---

## 3. CÁCH THỨC THỰC THI
Chạy lệnh kiểm tra tĩnh:
- Kiểm tra namespace dependencies qua AST/Grep.
- Kiểm tra cây thư mục dự án đối chiếu với cấu trúc chuẩn.
- Nếu có vi phạm: Xuất danh sách lỗi chi tiết kèm file, dòng, và **CHẶN KHÔNG CHO PASS QUALITY GATE**.
