---
name: po-issues
description: "Chuyển đổi danh sách công việc trong tasks.md thành các GitHub Issues theo thứ tự phụ thuộc (Dependency-ordered GitHub Issues) để quản lý tiến độ trên GitHub Project Board."
---

# Kỹ Năng: po-issues (Đồng Bộ Tasks Thành GitHub Issues)

> **Role Chịu Trách Nhiệm**: PO/PM Agent (`po-pm`) — Product Owner & Project Manager.  
> **Cổng Kiểm Soát**: Issue Tracking & Project Board Sync.

---

## 1. NGUYÊN TẮC ĐỒNG BỘ
- Đọc tệp `specs/[epic-id]/tasks.md`.
- Chuyển từng task thành 1 GitHub Issue có đầy đủ nhãn (Labels: `backend`, `frontend`, `test`, `epic-[id]`), người phụ trách (Assignee), và mô tả tiêu chí kiểm chứng hoàn thành.
- Giúp team theo dõi tiến độ trực quan trên GitHub Projects / Kanban Board.
