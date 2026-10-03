---
name: po-gate
description: "Bộ tiêu chuẩn nghiệm thu sản phẩm (Definition of Done - DoD), thẩm định chất lượng cuối cùng và ký biên bản xuất xưởng (Quality Gate 5 Sign-off) để đóng Epic/Release."
---

# Kỹ Năng: po-gate (Tiêu Chuẩn Nghiệm Thu & Ký Duyệt Gate 5)

> **Role Chịu Trách Nhiệm**: PO/PM Agent (`po-pm`) — Product Owner & Project Manager.  
> **Cổng Kiểm Soát**: Gate 5 Final Acceptance & Release Gatekeeper.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Báo cáo kiểm thử đạt chuẩn từ EC Agent (`docs/decisions/GATE4_VERIFICATION.md`) và mã nguồn hoàn thiện.
- **Target Output File**: `docs/decisions/GATE5_ACCEPTANCE.md`
- **Cập nhật trạng thái**: Đổi trạng thái Epic trong `backlog/ROADMAP.md` sang `[SHIPPED]`.
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. CHECKLIST DEFINITION OF DONE (DoD) BẮT BUỘC TRƯỚC KHI KÝ DUYỆT

PO/PM Agent chỉ được phép ký biên bản nghiệm thu khi **100% các tiêu chí sau đây đạt chuẩn**:

1. **Khớp Nghiệp Vụ 100% (Spec Compliance)**:
   - Toàn bộ các tiêu chí nghiệm thu (`AC-*`) trong `specs/[epic-id]/spec.md` đều có mã nguồn thực thi tương ứng.
2. **Kiểm Thử 3 Tầng Đạt Chuẩn (Green Tests)**:
   - Tầng 1: Unit Test cho 100% Business Rules (`BR-*`) chạy PASS.
   - Tầng 2: Database Integration Test cho API endpoints chạy PASS.
   - Tầng 3: Playwright E2E visual journeys chạy PASS, có kèm ảnh chụp màn hình kiểm chứng.
3. **Không Tồn Tại Lỗi Nghiêm Trọng (Zero Critical Defects)**:
   - Không còn lỗi Block, Critical hoặc Major nào chưa giải quyết trong báo cáo của EC Agent.
4. **Chuẩn Hóa 5 Trạng Thái UX**:
   - Giao diện người dùng trên web/app hiển thị đầy đủ và mượt mà: Loading, Empty, Error, Success, Updating.
5. **Vệ Sinh Kiến Trúc & Sạch Rác (Anti-Clutter Clean)**:
   - Không có file rác, file nháp vứt ở thư mục gốc.
   - Quét ranh giới kiến trúc (`sa-guard`) không phát hiện rò rỉ ranh giới Clean Architecture.

---

## 3. CẤU TRÚC BIÊN BẢN NGHIỆM THU GATE5_ACCEPTANCE.MD

```markdown
# BIÊN BẢN NGHIỆM THU & PHÊ DUYỆT XUẤT XƯỞNG (GATE 5 SIGN-OFF)

- **Mã Epic / Tính Năng**: [EPIC-ID]
- **Thời gian nghiệm thu**: [YYYY-MM-DD HH:mm]
- **Người ký duyệt**: PO/PM Agent
- **Đại diện Kỹ thuật**: TL/SA Agent & Dev Agent
- **Đại diện Kiểm định**: EC Agent

## 1. KẾT QUẢ ĐỐI SOÁT DEFINITION OF DONE
- [x] Tiêu chí nghiệp vụ: 10/10 AC đạt yêu cầu.
- [x] Kiểm thử tự động: 100% Green (Unit: Pass, Integration: Pass, E2E: Pass).
- [x] Lỗi tồn đọng: 0 Critical, 0 Major.
- [x] UX 5 States: Đạt chuẩn mượt mà.
- [x] Cấu trúc dự án: Sạch sẽ, không rác.

## 2. KẾT LUẬN & HÀNH ĐỘNG TIẾP THEO
- **Quyết định**: [CHÍNH THỨC PHÊ DUYỆT XUẤT XƯỞNG - SHIPPED]
- **Cập nhật Roadmap**: Đổi trạng thái trong `backlog/ROADMAP.md` sang `[SHIPPED]`.
- **Lưu trữ**: Đóng gói toàn bộ tài liệu đặc tả vào `specs/[epic-id]/`.
```
