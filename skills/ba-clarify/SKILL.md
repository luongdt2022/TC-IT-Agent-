---
name: ba-clarify
description: "Phát hiện và làm rõ các điểm mơ hồ trong đặc tả nghiệp vụ bằng cách đặt tối đa 5 câu hỏi trọng tâm sắc bén và mã hóa câu trả lời ngược lại vào spec.md."
---

# Kỹ Năng: ba-clarify (Làm Rõ Điểm Nghẽn Nghiệp Vụ)

> **Role Chịu Trách Nhiệm**: BA Agent (`ba`) — Senior Business Analyst.  
> **Cổng Kiểm Soát**: Gate 1 Clarification Gate.

---

## 1. NGUYÊN TẮC LÀM RÕ (CLARIFICATION PRINCIPLES)
1. **Không Hỏi Quá 5 Câu**: Tập trung vào tối đa 5 câu hỏi có tác động kiến trúc lớn nhất (High-impact decisions).
2. **Đưa Ra Phương Án Trắc Nghiệm Kèm Khuyến Nghị**: Không hỏi câu hỏi mở chung chung làm mất thời gian người dùng; luôn đưa ra các lựa chọn: *Phương án A (Khuyến nghị) vs Phương án B vs Khác*.
3. **Mã Hóa Kết Quả Ngược Lại Vào Tài Liệu**: Khi người dùng trả lời, ngay lập tức cập nhật câu trả lời thành các quy tắc `BR-*` hoặc `REQ-*` tương ứng trong `specs/[epic-id]/spec.md`.
