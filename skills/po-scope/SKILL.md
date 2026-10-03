---
name: po-scope
description: "Sàng lọc yêu cầu mới (Scope Triage), đánh giá rủi ro lan truyền (Cross-Surface Impact Matrix), phân loại MVP/Post-MVP và ngăn chặn Scope Creep."
---

# Kỹ Năng: po-scope (Sàng Lọc Yêu Cầu & Quản Trị Phạm Vi)

> **Role Chịu Trách Nhiệm**: PO/PM Agent (`po-pm`) — Product Owner & Project Manager.  
> **Cổng Kiểm Soát**: Gate 1 Scope Filter.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Yêu cầu tính năng mới từ người dùng, đề xuất cải tiến hoặc ý kiến đóng góp.
- **Target Output File**: `backlog/SCOPE_TRIAGE.md`
- **Cập nhật liên kết**: Cập nhật trực tiếp trạng thái vào `backlog/ROADMAP.md`.
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. NGUYÊN TẮC SÀNG LỌC ĐẦU VÀO (TRIAGE RULES)

Mỗi khi có yêu cầu hoặc ý tưởng mới xuất hiện, PO/PM Agent tiến hành 3 bước phân loại dứt khoát:

1. **Phân Định Trọng Tâm Giá Trị**:
   - Tính năng này giải quyết vấn đề cốt lõi nào của người dùng?
   - Có đóng góp trực tiếp vào mục tiêu của giai đoạn phát triển hiện tại không?
2. **Phân Loại Mức Độ Ưu Tiên (Priority Classification)**:
   - `P1 (MVP Core)`: Bắt buộc phải có để luồng đi mẫu (*Walking Skeleton*) chạy thông suốt từ đầu đến cuối.
   - `P2 (Important)`: Cần thiết cho vận hành thực tế nhưng có thể làm ngay sau MVP.
   - `P3 (Nice-to-have / Future)`: Tiện ích bổ sung, lưu vào `backlog/USER_STORIES/` để xem xét sau.
   - `REJECT`: Yêu cầu gây loãng phạm vi (Scope Creep), từ chối và giải thích lý do cụ thể.

---

## 3. MA TRẬN PHÂN TÍCH TÁC ĐỘNG LAN TRUYỀN (CROSS-SURFACE IMPACT MATRIX)

Trước khi phê duyệt đưa vào triển khai, bắt buộc rà soát 7 bề mặt kỹ thuật chịu ảnh hưởng:

| Bề mặt chịu ảnh hưởng | Câu hỏi đối soát | Có ảnh hưởng? (Có/Không) | Mức độ tác động |
| :--- | :--- | :---: | :--- |
| **1. Basic Design / UI** | Có thay đổi luồng nghiệp vụ hoặc layout màn hình không? | | Thấp / Vừa / Cao |
| **2. Detail Spec (SRS)** | Cần bổ sung thêm `REQ-` hay `BR-` mới không? | | Thấp / Vừa / Cao |
| **3. API & Contracts** | Có thay đổi tham số request / response payload (`API-*`) không? | | Thấp / Vừa / Cao |
| **4. Domain Validation** | Có thêm quy tắc nghiệp vụ hoặc điều kiện biên mới không? | | Thấp / Vừa / Cao |
| **5. Database Schema** | Cần thêm bảng, thêm cột, hay migration mới (`DB-*`) không? | | Thấp / Vừa / Cao |
| **6. Frontend Web/App** | Màn hình nào trên Web hoặc Mobile App bị thay đổi? | | Thấp / Vừa / Cao |
| **7. Test Suite** | Cần bổ sung Unit Test, Integration Test hay Playwright E2E nào? | | Thấp / Vừa / Cao |

---

## 4. QUYẾT ĐỊNH ĐẦU RA (TRIAGE VERDICT)
- **APPROVED (Chấp thuận)**: Gán mã Epic/Story, ghi nhận vào `backlog/SCOPE_TRIAGE.md`, cập nhật `backlog/ROADMAP.md` và bàn giao cho BA Agent (`ba-srs`).
- **DEFERRED (Tạm hoãn)**: Lưu vào `backlog/USER_STORIES/` kèm điều kiện kích hoạt trong tương lai.
- **REJECTED (Từ chối)**: Đóng yêu cầu kèm giải thích ngắn gọn, súc tích dựa trên mục tiêu dự án.
