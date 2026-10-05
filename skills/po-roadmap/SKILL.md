---
name: po-roadmap
description: "Quản trị Master Roadmap, Milestones, Epic Decomposition và đối soát tiến độ thực tế từ tasks.md để cập nhật trạng thái dự án tại specs/ROADMAP.md (hoặc backlog/ROADMAP.md)."
---

# Kỹ Năng: po-roadmap (Quản Trị Master Roadmap & Tiến Độ Dự Án)

> **Role Chịu Trách Nhiệm**: PO/PM Agent (`po-pm`) — Product Owner & Project Manager.  
> **Cổng Kiểm Soát**: Scope, Planning & Milestones Tracking.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Danh sách Epic từ khâu khảo sát hoặc các tệp `specs/[epic-id]/tasks.md`.
- **Target Output File**: `specs/ROADMAP.md` (hoặc `backlog/ROADMAP.md`)
- **Tài liệu phân rã chi tiết**: `specs/[epic-id]/` hoặc `backlog/EPICS/`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. CẤU TRÚC CHUẨN CỦA ROADMAP.MD

Tệp `specs/ROADMAP.md` (hoặc `backlog/ROADMAP.md`) là bảng điều khiển tiến độ tổng thể của toàn dự án, bao gồm:

```markdown
# MASTER ROADMAP & TIẾN ĐỘ DỰ ÁN (PROJECT ROADMAP)

- **Cập nhật lần cuối**: [YYYY-MM-DD]
- **Người quản trị**: PO/PM Agent

## 1. BẢNG THEO DÕI TIẾN ĐỘ EPICS
| Mã Epic | Tên Phân Hệ / Tính Năng | Ưu Tiên | Trạng Thái | Tiến Độ (%) | Ghi Chú |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `EPIC-01` | Xác Thực & Phân Quyền | P0 | [SHIPPED] | 100% | Đã nghiệm thu Gate 5 |
| `EPIC-02` | Quản Lý Khách Hàng | P1 | [IN-PROGRESS] | 65% | Đang làm Chặng 5 |
| `EPIC-03` | Báo Cáo & Thống Kê | P2 | [PLANNED] | 0% | Chờ Sprint sau |

## 2. KẾ HOẠCH BÀN GIAO THEO GIAI ĐOẠN (MILESTONES)
### Milestone 1: Minimum Viable Product (MVP) — [Ngày dự kiến]
- [x] EPIC-01: Authentication & RBAC
- [ ] EPIC-02: Customer Management

### Milestone 2: Enterprise Enhancements — [Ngày dự kiến]
- [ ] EPIC-03: Advanced Analytics
```

---

## 3. CÁC THAO TÁC THỰC THI CHÍNH

1. **Khởi tạo Roadmap ban đầu (`init`)**:
   - Khi khởi động dự án (`wf-kickoff`), phân rã từ Proposal/Basic Design thành danh sách Epics và khởi tạo Roadmap.
2. **Đăng ký Epic mới (`register`)**:
   - Thêm dòng mới vào bảng Epic Tracker, tạo thư mục tương ứng `specs/[epic-id]/`.
3. **Đối soát tự động (`sync`)**:
   - Đọc quét toàn bộ các file `specs/[epic-id]/tasks.md`.
   - Đếm số lượng task hoàn thành `[x]` trên tổng số task `[ ]` để tự động cập nhật % tiến độ trong Roadmap.
