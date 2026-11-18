---
name: wf-pr-review
description: "Quy trình gác cổng Task DoD và Pull Request theo 6 trục kiểm soát (Gate 3 & Gate 4). Dùng khi Dev chuẩn bị mở PR hoặc SA/QA thực hiện rà soát đối kháng."
---

# Quy Trình Gác Cổng Task DoD & Pull Request (`wf-pr-review`)

## 1. Mục tiêu
Đảm bảo mọi thay đổi mã nguồn trước khi merge đều vượt qua 6 trục kiểm soát kỹ thuật và 2 cổng kiểm duyệt (Dev Self-Verify + SA Adversarial Review).

## 2. Các bước thực hiện
1. **Dev Self-Verification**:
   - Đối soát theo `templates/TEMPLATE-task-review-checklist.md`.
   - Chạy `bash scripts/guard-rails.sh` và bộ Unit Test `BR-*` (100% Pass, không sửa assertion test).
2. **Mở Pull Request chuẩn hóa**:
   - Điền đầy đủ `templates/TEMPLATE-pull-request.md` (6 trục: Clean Arch, Non-destructive Migration, Scoped RBAC, Concurrency, 5 UX States `<Async>`, Zero-Regression).
   - Đính kèm kết quả chạy lệnh thực tế và bằng chứng `audit_wireframe_fields.py`.
3. **SA Adversarial Review (`sa` via `pr-review-guard` / `sa-review`)**:
   - Kiểm toán độc lập theo 6 trục; 0 lỗi `CRITICAL` mới ký duyệt Gate 3 để chuyển sang `qc`.
