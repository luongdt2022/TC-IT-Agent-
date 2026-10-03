---
name: dev-converge
description: "Đánh giá mức độ hội tụ giữa mã nguồn thực tế và spec.md/plan.md, tự động phát hiện các phần việc còn thiếu sót và sinh bổ sung thành các task mới vào tasks.md để lập trình viên hoàn tất."
---

# Kỹ Năng: dev-converge (Quét Hội Tụ Mã Nguồn & Bổ Sung Tasks)

> **Role Chịu Trách Nhiệm**: Dev Agent (`dev`) — Senior Full-Stack Developer.  
> **Cổng Kiểm Soát**: Pre-Review Convergence Gate.

---

## 1. NGUYÊN TẮC HỘI TỤ (CONVERGENCE INVARIANT)
Một tính năng chỉ được coi là "Hội tụ 100%" khi toàn bộ các tiêu chí nghiệm thu (`AC-*`) và quy tắc nghiệp vụ (`BR-*`) trong `specs/[epic-id]/spec.md` đều có code chạy thực tế và test tương ứng trong `src/` và `tests/`.

---

## 2. QUY TRÌNH THỰC THI
1. **Đối soát Mã Nguồn**: Đọc quét toàn bộ các file trong `src/` đối chiếu từng dòng tiêu chí trong `specs/[epic-id]/spec.md`.
2. **Nhận Diện Phần Việc Chưa Hoàn Tất**: Liệt kê các use cases, validation rules hoặc màn hình UI chưa được lập trình.
3. **Sinh Bổ Sung Tasks**: Tự động chèn các task còn thiếu vào cuối tệp `specs/[epic-id]/tasks.md` với định dạng `[CONVERGE-TASK-xx]` để tiếp tục thực thi qua `dev-code`.
