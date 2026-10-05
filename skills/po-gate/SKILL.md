---
name: po-gate
description: "Bộ tiêu chuẩn nghiệm thu sản phẩm (Definition of Done - DoD), thẩm định chất lượng cuối cùng và ký biên bản xuất xưởng (Quality Gate 5 Sign-off) để đóng Epic/Release."
---

# Kỹ Năng: po-gate (Biên Bản Nghiệm Thu & Phê Duyệt Xuất Xưởng Gate 5)

> **Role Chịu Trách Nhiệm**: PO/PM Agent (`po-pm`) — Product Owner & Project Manager.  
> **Cổng Kiểm Soát**: Quality Gate 5 Final Acceptance & Shipped Sign-off.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Báo cáo kiểm thử đạt chuẩn từ EC Agent (`docs/decisions/GATE4_VERIFICATION.md`) và mã nguồn hoàn thiện.
- **Target Output File**: `docs/decisions/GATE5_ACCEPTANCE.md`
- **Cập nhật trạng thái**: Đổi trạng thái Epic trong `specs/ROADMAP.md` (hoặc `backlog/ROADMAP.md`) sang `[SHIPPED]`.
- **Cập nhật Living Docs**: Sử dụng kết hợp kỹ năng `xong` để đồng bộ trạng thái thực tế vào `docs/system/` (hoặc `docs/`).
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. MA TRẬN ĐỐI SOÁT DEFINITION OF DONE (DOD CHECKLIST)

PO/PM chỉ ký duyệt xuất xưởng khi thỏa mãn 100% các điều kiện:

1. **Độ Bao Phủ Nghiệp Vụ (Requirements Coverage)**:
   - 100% tiêu chí nghiệm thu (`AC-*`) và quy tắc nghiệp vụ (`BR-*`) trong `specs/[epic-id]/spec.md` đã được chuyển giao đầy đủ.
2. **Kiểm Thử Xanh Tuyệt Đối (Zero Failing Tests)**:
   - 100% Unit Tests logic, Database Integration Tests và E2E Visual QA tests đều pass (màu xanh).
   - Không tồn tại bất kỳ lỗi loại P0 (Blocker) hay P1 (Critical) nào.
3. **Kỷ Luật Kiểm Thử Bất Biến (Test Immobility Verified)**:
   - Xác nhận Dev không sửa đổi assertion của test để đối phó.
4. **Đồng Bộ Tài Liệu Sống (Living Docs Up-to-Date)**:
   - Tài liệu mô tả hiện trạng hệ thống đã được cập nhật chính xác với code thực tế.
5. **Quyết Định Kiến Trúc Được Lưu Trữ (ADR Recorded)**:
   - Các quyết định một chiều, schema CSDL, hoặc công nghệ lõi mới đã được ghi thành ADR trong `docs/decisions/`.

---

## 3. MẪU BIÊN BẢN GATE5_ACCEPTANCE.MD

```markdown
# BIÊN BẢN NGHIỆM THU XUẤT XƯỞNG (QUALITY GATE 5 SIGN-OFF)

- **Mã Epic**: [epic-id]
- **Tên Phân Hệ**: [Tên Epic]
- **Người Ký Duyệt**: PO/PM Agent
- **Thời Gian Ký**: [YYYY-MM-DD HH:mm]

## 1. ĐỐI SOÁT DEFINITION OF DONE
| Tiêu Chí Nghiệm Thu | Kết Quả Thẩm Định | Người Xác Nhận | Trạng Thái |
| :--- | :--- | :---: | :---: |
| **Phạm Vi Nghiệp Vụ** | 100% AC-* & BR-* hoàn tất | BA Agent | [PASS] |
| **Kiến Trúc & Mã Nguồn** | Clean Architecture, TypeCheck Green | TL/SA Agent | [PASS] |
| **Chất Lượng Kiểm Thử** | 3-Tier Tests Pass 100%, 0 Blocker | EC Agent | [PASS] |
| **Tài Liệu Sống** | docs/system/ đã phản ánh hiện trạng | PO/PM Agent | [PASS] |

## 2. KẾT LUẬN & HÀNH ĐỘNG TIẾP THEO
- **Quyết định**: [CHÍNH THỨC PHÊ DUYỆT XUẤT XƯỞNG - SHIPPED]
- **Cập nhật Roadmap**: Đổi trạng thái trong `specs/ROADMAP.md` (hoặc `backlog/ROADMAP.md`) sang `[SHIPPED]`.
- **Lưu trữ**: Đóng gói toàn bộ tài liệu đặc tả vào `specs/[epic-id]/`.
```
