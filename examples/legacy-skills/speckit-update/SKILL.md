---
name: speckit-update
description: "Cập nhật, sửa đổi và mở rộng nghiệp vụ cho một Epic đã hoàn thiện theo chuẩn Spec Kit Delta (Impact Analysis -> Clarify Check -> Plan Delta -> UI/UX Delta -> Tasks Delta -> Analyze Delta -> Implement Delta -> Converge Delta)."
compatibility: "Requires spec-kit project structure with .specify/ directory"
metadata:
  author: "github-spec-kit"
  source: "custom/speckit-update"
---
## User Input

```text
$ARGUMENTS
```

## Chỉ Dẫn Thực Thi

Đây là bí danh (alias) của skill `speckit-delta`.
Hãy đọc và tuân thủ toàn bộ quy trình cập nhật delta 7 giai đoạn chi tiết tại:
[`../speckit-delta/SKILL.md`](../speckit-delta/SKILL.md)

1. **[1] Impact Analysis**: Phân tích bề mặt tác động (Multi-tenant, CSDL, Domain, API, UI/UX Layout), bổ sung mục Spec Delta vào `spec.md`, và cập nhật trạng thái `🔄 Nâng cấp Delta (In Progress)` trong `specs/ROADMAP.md`.
2. **[1.1] Clarify Check**: 🛑 **CHECKPOINT 1 — DỪNG LẠI HỎI** nếu tài liệu mới mâu thuẫn hoặc thiếu dữ kiện. Nếu đã rõ -> Tự động đi tiếp.
3. **[2] Plan Delta**: Cập nhật `plan.md`, `data-model.md`, và API contracts theo chiến lược non-destructive. 🛑 **CHECKPOINT 2 — DỪNG LẠI HỎI** nếu có breaking change.
4. **[2.1] speckit-uiux**: (Nếu Delta có đổi UI) Đối soát wireframe, áp dụng 5 Luật Code Frontend (ADR 0009), 4-5 trạng thái UX qua `<Async>`, tái sử dụng primitives từ `components/ui/index.ts`.
5. **[3] Tasks Delta**: Append Phase mới vào cuối `tasks.md`, bảo toàn các task cũ đã làm `[x]`.
6. **[3.1] speckit-analyze**: Rà soát chéo ma trận phủ Delta (`spec.md` ⟷ `plan.md` ⟷ `tasks.md`), tự động vá (self-correct) task còn thiếu trước khi code.
7. **[4] Implement Delta**: Chạy migration mới (v2, v3...), viết code, viết unit test mới, chạy `pnpm typecheck` / `pnpm test`. 🛑 **CHECKPOINT 3 — DỪNG LẠI HỎI** nếu gặp lỗi blocker.
8. **[5] Converge Delta**: Kiểm tra hội tụ 100%, cập nhật living docs `docs/system/`, cập nhật trạng thái `✅ 100% Hoàn thành (Delta vX)` cùng số tasks và kết quả test vào `specs/ROADMAP.md`, xuất báo cáo nghiệm thu trọn vẹn.
