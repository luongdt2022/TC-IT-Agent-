---
name: po-roadmap
description: "Quản trị Master Roadmap, Milestones, Epic Decomposition và đối soát tiến độ thực tế từ tasks.md để cập nhật trạng thái dự án tại backlog/ROADMAP.md."
---

# Kỹ Năng: po-roadmap (Quản Trị Master Roadmap & Tiến Độ Dự Án)

> **Role Chịu Trách Nhiệm**: PO/PM Agent (`po-pm`) — Product Owner & Project Manager.  
> **Cổng Kiểm Soát**: Gate 1 & Gate 5 Progress Tracking.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Danh sách Epic từ khâu khảo sát hoặc các tệp `specs/[epic-id]/tasks.md`.
- **Target Output File**: `backlog/ROADMAP.md`
- **Tài liệu phân rã chi tiết**: `backlog/EPICS/` và `backlog/USER_STORIES/`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. CẤU TRÚC CHUẨN CỦA BACKLOG/ROADMAP.MD

Tệp `backlog/ROADMAP.md` là bảng điều khiển tiến độ tổng thể của toàn dự án, bao gồm:

```markdown
# MASTER ROADMAP & TIẾN ĐỘ DỰ ÁN (PROJECT ROADMAP)

## 1. TỔNG QUAN TIẾN ĐỘ THEO MILESTONE
- **Milestone 1 (MVP Walking Skeleton)**: [████████░░] 80% — Hạn: [YYYY-MM-DD]
- **Milestone 2 (Core Features)**: [██░░░░░░░░] 20% — Hạn: [YYYY-MM-DD]
- **Milestone 3 (Hardening & Release)**: [░░░░░░░░░░] 0% — Hạn: [YYYY-MM-DD]

## 2. MA TRẬN THEO DÕI TỪNG EPIC (EPIC TRACKER)
| Mã Epic | Tên Epic / Tính Năng | Phân Hệ | Phụ Trách | Trạng Thái | Tiến Độ Tasks | Gate Hiện Tại |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| `EPIC-01` | Quản lý Định danh & RBAC | IAM | Dev/BA | [IN_PROGRESS] | 8/10 [x] | Gate 3 (Code) |
| `EPIC-02` | Quản lý Giỏ hàng & Thanh toán | Core | Dev/EC | [SPEC_APPROVED] | 0/12 [ ] | Gate 2 (Plan) |

## 3. CÁC QUY ƯỚC TRẠNG THÁI (STATUS CONVENTIONS)
- `[PROPOSED]`: Đang ở mức ý tưởng / Sàng lọc sơ bộ.
- `[SPEC_APPROVED]`: BA đã chốt spec.md (Gate 1 Passed).
- `[PLAN_APPROVED]`: SA đã chốt plan.md & tasks.md (Gate 2 Passed).
- `[IN_PROGRESS]`: Dev đang lập trình thực thi.
- `[VERIFYING]`: EC Agent đang kiểm thử 3 tầng (Gate 4 Pending).
- `[SHIPPED]`: PO/PM đã ký nghiệm thu hoàn tất Definition of Done (Gate 5 Passed).
```

---

## 3. CÁC THAO TÁC THỰC THI CHÍNH

1. **Khởi tạo Roadmap ban đầu (`init`)**:
   - Khi khởi động dự án (`wf-kickoff`), phân rã từ Proposal/Basic Design thành danh sách Epics và khởi tạo `backlog/ROADMAP.md`.
2. **Đăng ký Epic mới (`register`)**:
   - Thêm dòng mới vào bảng Epic Tracker, tạo thư mục tương ứng `specs/[epic-id]/`.
3. **Đối soát tự động (`sync`)**:
   - Đọc quét toàn bộ các file `specs/[epic-id]/tasks.md`.
   - Đếm số lượng task hoàn thành `[x]` trên tổng số task `[ ]` để tự động cập nhật % tiến độ trong `backlog/ROADMAP.md`.
