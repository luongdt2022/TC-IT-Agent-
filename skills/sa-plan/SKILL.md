---
name: sa-plan
description: "Lập kế hoạch kiến trúc kỹ thuật chi tiết cho một Epic/Tính năng (plan.md): Phân rã tầng Clean Architecture, ánh xạ các tệp mã nguồn sẽ tạo/sửa, cơ chế Transaction, Caching và Security."
---

# Kỹ Năng: sa-plan (Lập Kế Hoạch Kiến Trúc Kỹ Thuật Theo Epic)

> **Role Chịu Trách Nhiệm**: TL/SA Agent (`techlead-sa`) — Software Architect & Tech Lead.  
> **Cổng Kiểm Soát**: Gate 2 Architecture Plan Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Đặc tả `specs/[epic-id]/spec.md` và tài liệu thiết kế chi tiết tại `docs/02-detail-design/`.
- **Target Output File**: `specs/[epic-id]/plan.md`
- **NGHIÊM CẤM**: Không tạo các file plan lẻ tẻ ngoài thư mục `specs/[epic-id]/`.

---

## 2. CẤU TRÚC BẮT BUỘC CỦA TẬP TIN PLAN.MD

Tập tin `specs/[epic-id]/plan.md` phải tuân thủ nghiêm ngặt 5 phần chuẩn kỹ thuật:

```markdown
# KẾ HOẠCH TRIỂN KHAI KIẾN TRÚC KỸ THUẬT: [TÊN TÍNH NĂNG]

- **Mã Epic**: [EPIC-ID]
- **Kiến trúc áp dụng**: Clean Architecture / Modular Monolith
- **Kiểm soát Gate**: Gate 2 (Architecture Approved)

## 1. TỔNG QUAN KIẾN TRÚC PHÂN TẦNG (ARCHITECTURE BLUEPRINT)
- Phân bổ trách nhiệm qua 4 tầng:
  - `Domain`: Các Entity lõi, Value Objects, Domain Events, Domain Exceptions.
  - `Application`: CQRS Commands/Queries, Use Cases, DTOs, FluentValidation, Interfaces.
  - `Infrastructure`: DB Context, Repositories, Migrations, External Service Adapters.
  - `Presentation / API`: Controllers, Request/Response Mappings, Scoped RBAC Attributes.
  - `WebApp / Client`: UI Components chuẩn hóa 5 trạng thái UX qua `<Async>`.

## 2. DANH MỤC TỆP TIN DỰ KIẾN TẠO MỚI HOẶC CHỈNH SỬA (FILE MANIFEST)
- [CREATE] `src/Domain/Entities/[Entity].cs`
- [CREATE] `src/Application/Features/[Feature]/Commands/[Command].cs`
- [CREATE] `src/Application/Features/[Feature]/Commands/[CommandValidator].cs`
- [CREATE] `src/Infrastructure/Persistence/Configurations/[EntityConfiguration].cs`
- [CREATE] `src/Presentation/Controllers/[Controller].cs`
- [CREATE] `src/WebApp/components/[Component].tsx`
- [CREATE] `tests/unit/[Feature]Tests.cs`
- [CREATE] `tests/e2e/[feature].spec.ts`

## 3. CƠ SỞ DỮ LIỆU & CHIẾN LƯỢC MIGRATION
- Mã DB: `DB-[NAME]`
- Script Migration: Tên file migration, các câu lệnh DDL không gây downtime.
- Chiến lược Index và Khóa lạc quan (Concurrency Token).

## 4. CHIẾN LƯỢC TRANSACTION, CACHE & AN TOÀN DỮ LIỆU
- Transaction Scope: Unit of Work, Isolation Level (Read Committed).
- Caching: Cache key naming convention, TTL (Time-to-live), Chiến lược Cache Invalidation.
- Security: Phân quyền Scoped RBAC, mã hóa dữ liệu nhạy cảm.

## 5. RỦI RO KỸ THUẬT & PHƯƠNG ÁN PHÒNG NGỪA
- Nguy cơ N+1 Query và giải pháp (Eager Loading / Projection).
- Xử lý bất đồng bộ (Idempotent Consumer, Retry Policy).
```
