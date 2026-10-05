---
name: sa-guard
description: "Vệ binh Kiến trúc & Cấu trúc Thư mục (Architecture & Directory Sentinel). Quét phát hiện vi phạm ranh giới Clean Architecture/Phân tầng, rò rỉ CSDL lên API/UI, rò rỉ phân quyền/đa tổ chức, vi phạm thư viện dùng chung và kiểm tra kỷ luật thư mục chống rác (Zero-Tolerance Root Dumping)."
---

# Kỹ Năng: sa-guard (Vệ Binh Ranh Giới Kiến Trúc & Cấu Trúc Thư Mục)

> **Role Chịu Trách Nhiệm**: TL/SA Agent (`techlead-sa` / `tc-sa`) — Software Architect & Tech Lead.  
> **Cổng Kiểm Soát**: Gate 2, Gate 3, Gate 4 Lint & Sentinel Gatekeeper.

---

## 1. NGUYÊN TẮC KIỂM TRA RANH GIỚI KIẾN TRÚC (ARCHITECTURE INVARIANTS)

Vệ binh `sa-guard` quét toàn bộ mã nguồn của dự án để phát hiện các vi phạm cấu trúc cốt lõi:

1. **Rò Rỉ Hạ Tầng Lên Tầng Trên (Infrastructure Leaks)**:
   - Nghiêm cấm tầng `Presentation/API` hoặc `Application` gọi trực tiếp `DbContext`, Raw SQL hoặc các SDK Third-party cụ thể. Mọi tương tác phải qua Interface / Repository / Service layer.
2. **Phụ Thuộc Ngược Từ Domain (Domain Inversion Violation)**:
   - Tầng `Domain` tuyệt đối KHÔNG ĐƯỢC chứa dependencies từ `Application`, `Infrastructure`, hay `Presentation`. `Domain` là tầng độc lập tuyệt đối.
3. **Thao Tác CSDL Trực Tiếp Trên Controller / Route Handler**:
   - Nghiêm cấm viết câu lệnh SQL thô, query ORM trực tiếp hoặc gọi HTTP client bên ngoài trong Controller/Page. Controller chỉ nhận request, chuyển qua Use Case / Service và trả về response.
4. **Cô Lập Đa Tổ Chức & Ngữ Cảnh Bảo Mật (Tenant & Security Boundary Isolation)**:
   - Trong các hệ thống Multi-tenant, mọi thao tác đọc/ghi bảng nghiệp vụ bắt buộc phải gắn điều kiện lọc Tenant Context (`tenant_id` / `org_id`).
5. **Kỷ Luật Tái Sử Dụng Thành Phần Dùng Chung (Component / Module Grounding)**:
   - Trước khi tạo component hoặc hàm tiện ích mới, bắt buộc tra cứu Catalog dùng chung (như `components/ui/index.ts`, `Common/`, `Shared/`). Cấm tạo bản sao thứ hai hoặc tái phát minh bánh xe.

---

## 2. NGUYÊN TẮC KIỂM TRA THƯ MỤC CHỐNG RÁC (ANTI-CLUTTER DIRECTORY LINTER)

`sa-guard` thực hiện kiểm tra kỷ luật cấu trúc thư mục dự án:

1. **Quét Thư Mục Gốc (`root`)**:
   - Nếu phát hiện file `.md` lẻ tẻ (ngoài `README.md`, `AGENTS.md`, `constitution.md`), file `.js/.ts/.py` chạy thử, hoặc file log vứt ở root $\rightarrow$ **CẢNH BÁO VI PHẠM & TỰ ĐỘNG DỌN DẸP**.
2. **Kiểm Tra Vị Trí File Test**:
   - Mọi file test (`*Test.cs`, `*.spec.ts`, `*.test.js`, `test_*.py`) phải nằm trong thư mục kiểm thử quy định (`tests/` hoặc thư mục `__tests__/` của module). Cấm để file test lạc ở root.
3. **Kiểm Tra Vị Trí File Đặc Tả & Thiết Kế**:
   - Master Roadmap ➔ Bắt buộc nằm tại `specs/ROADMAP.md` (hoặc `backlog/ROADMAP.md`).
   - Spec Kit theo Epic ➔ Bắt buộc nằm tại `specs/[epic-id]/` (`spec.md`, `plan.md`, `tasks.md`).
   - Living Documents ➔ Bắt buộc nằm tại `docs/system/<vùng>.md` (hoặc `docs/01-basic-design/`).
   - Architecture Decisions ➔ Bắt buộc nằm tại `docs/decisions/NNNN-ten-quyet-dinh.md`.
4. **Kiểm Tra Vị Trí Mã Nguồn**:
   - Toàn bộ mã nguồn phải nằm trong cấu trúc phân tầng (`src/` hoặc `apps/`, `services/`). Cấm tạo các thư mục mã nguồn ngoài lề ở root.

---

## 3. CÁCH THỨC THỰC THI (AUTOMATED GUARDRAILS EXECUTION)

Chạy kịch bản gác cổng tự động chống ảo giác & kiến trúc:
```bash
./scripts/guard-rails.sh
```
Kịch bản tự động kiểm tra:
1. Compiler & TypeCheck tĩnh (`tsc --noEmit`, `mypy`, `dotnet build`... tùy stack dự án).
2. Schema & Model validation (CSDL migrations, ORM model check).
3. Quét vi phạm gọi API thô / rò rỉ kiến trúc.
4. Grounding Check: Xác thực sự tồn tại của Shared Components & Database Models.

**Quy tắc Chặn**: Nếu `./scripts/guard-rails.sh` trả về mã lỗi (`exit 1`), TL/SA Agent kiên quyết **TỪ CHỐI THÔNG QUA GATE 2 / GATE 3** cho đến khi Dev sửa triệt để.
