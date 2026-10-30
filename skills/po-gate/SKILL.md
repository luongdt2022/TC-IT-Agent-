---
name: po-gate
description: "Bộ tiêu chuẩn nghiệm thu sản phẩm (Definition of Done - DoD), thẩm định chất lượng cuối cùng và ký biên bản xuất xưởng (Quality Gate 5 Sign-off) để đóng Epic/Release."
---
# Kỹ Năng: po-gate (Biên Bản Nghiệm Thu & Phê Duyệt Xuất Xưởng Gate 5)

> **Role Chịu Trách Nhiệm**: PO/PM Agent (`po-pm`) — Product Owner & Project Manager.  
> **Cổng Kiểm Soát**: Quality Gate 5 Final Acceptance & Shipped Sign-off.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Báo cáo kiểm thử đạt chuẩn từ EC / QC Agent (`docs/decisions/GATE4_VERIFICATION.md`) và mã nguồn hoàn thiện.
- **Target Output File**: `docs/decisions/GATE5_ACCEPTANCE.md`
- **Cập nhật trạng thái**: Đổi trạng thái Epic trong `specs/ROADMAP.md` (hoặc `backlog/ROADMAP.md`) sang `[SHIPPED]`.
- **Cập nhật Living Docs**: Sử dụng kết hợp kỹ năng `xong` để đồng bộ trạng thái thực tế vào `docs/system/` (hoặc `docs/`).
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. MA TRẬN ĐỐI SOÁT DEFINITION OF DONE (DOD CHECKLIST)

PO/PM chỉ ký duyệt xuất xưởng khi thỏa mãn 100% các điều kiện thiết quân luật:

### A. Kiểm Soát Kỷ Luật Dev (Dev Checklist Audit)
1. **Bám sát 1:1 `tasks.md` (Zero Skip Steps)**: 100% các task được phân rã đã hoàn thành và có bằng chứng đối soát thực tế. Tuyệt đối cấm bỏ bước, làm tắt.
2. **Đầy đủ 3 tầng kỹ thuật**: Mã nguồn có đủ `[BE]` Service/API $\rightarrow$ `[FE]` Component $\rightarrow$ `[Test]` Unit Test cho 100% `BR-*`.
3. **Chuẩn hóa 5 UX States**: Mọi màn hình UI phải bọc qua `<Async>` và xử lý đủ Loading, Empty, Error, Success, Partial.
4. **Kỷ luật Zero-Mock**: Không chứa bất kỳ dữ liệu fake/mock ngầm nào trong catch hoặc UI.
5. **Kỷ luật Test Immobility**: Xác nhận Dev không sửa đổi assertion của test để đối phó.

### B. Bộ 3 Thẩm Vấn Thép Cho QC (QC Strict Audit)
6. **Data Test Chuẩn & 4 Tầng Kiểm Thử (Không Mock/Hardcode)**:
   - Data test chạy trên CSDL thật (có seed data script, đủ case biên và quan hệ khóa ngoại).
   - Kiểm thử Blackbox và đủ 4 tầng: Unit Test (`BR-*`), Contract Test (DTO), DB Integration Test, Playwright E2E & Scoped RBAC Fuzzing.
   - **Tuyệt đối nghiêm cấm QC mock dữ liệu hoặc hardcode assertion**.
7. **Định Lượng Test Case & Luồng Kiểm Thử**:
   - Thống kê rõ: Tổng số test cases (Happy Path, Negative, Edge/Boundary, RBAC) và số luồng hành trình người dùng (User Journeys).
   - Đảm bảo đối soát khép kín 100% tiêu chí nghiệm thu (`AC-*`) và quy tắc nghiệp vụ (`BR-*`) trong `specs/[epic-id]/spec.md`.
8. **Phản Xạ Hoài Nghi Khi Báo 0 Bug & Tiêu Chí "QC Phải Tìm Ra Bug"**:
   - **PO lập tức từ chối duyệt nếu QC báo "0 bug / Pass 100% ngay lần đầu"** mà không xuất trình bằng chứng kiểm thử phá hoại (Chaos, Spam click, Network drop, IDOR, SQLi, Long input).
   - QC phải chứng minh đã bới lông tìm vết, tìm ra bug và xác nhận Dev đã fix triệt để thì mới được tính là hoàn thành nhiệm vụ.

### C. Quản Trị Hệ Thống & Tài Liệu Sống
9. **Đồng Bộ Tài Liệu Sống (Living Docs Up-to-Date)**:
   - Tài liệu mô tả hiện trạng hệ thống (`docs/system/`) đã được cập nhật chính xác với code thực tế.
10. **Quyết Định Kiến Trúc Được Lưu Trữ (ADR Recorded)**:
    - Các quyết định một chiều, schema CSDL, hoặc công nghệ lõi mới đã được ghi thành ADR trong `docs/decisions/`.

---

## 3. MẪU BIÊN BẢN GATE5_ACCEPTANCE.MD

```markdown
# BIÊN BẢN NGHIỆM THU XUẤT XƯỞNG (QUALITY GATE 5 SIGN-OFF)

- **Mã Epic**: [epic-id]
- **Tên Phân Hệ**: [Tên Epic]
- **Người Ký Duyệt**: PO/PM Agent
- **Thời Gian Ký**: [YYYY-MM-DD HH:mm]

## 1. ĐỐI SOÁT DEFINITION OF DONE THIẾT QUÂN LUẬT
| Nhóm Kiểm Soát | Tiêu Chí Nghiệm Thu | Kết Quả Thẩm Định | Người Xác Nhận | Trạng Thái |
| :--- | :--- | :--- | :---: | :---: |
| **Kỷ Luật Dev** | 1:1 tasks.md, Đủ 3 tầng [BE/FE/Test], 5 UX States, Zero-Mock | Đã đối soát code thật, không bỏ bước | Dev Senior | [PASS] |
| **QC Data & 4 Tầng** | Data CSDL thật, Test 4 tầng, Cấm Mock/Hardcode | Đã kiểm tra seed data & script | QC Specialist | [PASS] |
| **QC Coverage** | Định lượng [XX] test cases, [YY] luồng hành trình | Phủ kín 100% AC-* & BR-* | QC Specialist | [PASS] |
| **QC Bug Mandate** | Đã test phá hoại, tìm ra bug và Dev đã fix triệt để | Bác bỏ báo cáo 0 bug, đã verify bug thật | QC Specialist | [PASS] |
| **Kiến Trúc & Mã Nguồn** | Clean Architecture, TypeCheck Green, Zero Drift | Quét AST & biên dịch sạch | TL/SA Agent | [PASS] |
| **Tài Liệu Sống** | docs/system/ & ADR đã phản ánh đúng hiện trạng | Cập nhật living docs | PO/PM Agent | [PASS] |

## 2. KẾT LUẬN & HÀNH ĐỘNG TIẾP THEO
- **Quyết định**: [CHÍNH THỨC PHÊ DUYỆT XUẤT XƯỞNG - SHIPPED]
- **Cập nhật Roadmap**: Đổi trạng thái trong `specs/ROADMAP.md` (hoặc `backlog/ROADMAP.md`) sang `[SHIPPED]`.
- **Lưu trữ**: Đóng gói toàn bộ tài liệu đặc tả vào `specs/[epic-id]/`.
```
