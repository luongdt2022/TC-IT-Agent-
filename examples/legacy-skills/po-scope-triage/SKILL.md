---
name: po-scope-triage
description: "Chuyên viên Sàng lọc & Đánh giá Phạm vi Yêu cầu (Scope Triage Specialist). Phân loại yêu cầu mới, đánh giá rủi ro lan truyền (Cross-Surface Impact Matrix), và xác định lộ trình MVP / Post-MVP."
metadata:
  short-description: Sàng lọc yêu cầu mới và phân tích tác động lan truyền
---

# Scope Triage & Impact Analysis Specialist (`po-scope-triage`)

Skill chuyên trách dành cho **Agent PO / PM** để sàng lọc yêu cầu đầu vào, kiểm soát phạm vi và ngăn chặn rủi ro Scope Creep.

## 1. NGUYÊN TẮC SÀNG LỌC ĐẦU VÀO (TRIAGE RULES)
Khi có bất kỳ yêu cầu, ý tưởng hoặc tính năng mới được đưa ra:
1. **Phân Định Ranh Giới Module**:
   - Xác định tính năng này thuộc phân hệ nào:
     - Module 1: Kho Dữ liệu Công nghệ & Truy xuất (Tech Data & TracePro)
     - Module 2: Đào tạo Trực tuyến & Kết nối Chuyên gia (LMS & Expert Network)
     - Module 3: Nền tảng Quản trị & Hạ tầng Dữ liệu (Core Platform & RBAC)
2. **Đánh Giá Lộ Trình (Priority Classification)**:
   - `P1 (MVP Core)`: Tính năng thiết yếu để luồng Walking Skeleton chạy thông suốt từ đầu đến cuối.
   - `P2 (Important)`: Cần thiết cho vận hành thực tế nhưng có thể làm ngay sau MVP.
   - `P3 (Nice-to-have / Future)`: Tiện ích mở rộng, đưa vào Backlog dài hạn.

## 2. MA TRẬN PHÂN TÍCH TÁC ĐỘNG LAN TRUYỀN (CROSS-SURFACE IMPACT MATRIX)
Trước khi phê duyệt đưa vào triển khai, bắt buộc rà soát 8 bề mặt chịu ảnh hưởng:

| Bề mặt | Câu hỏi đối soát | Có ảnh hưởng? (Có/Không) | Mức độ tác động |
| :--- | :--- | :---: | :--- |
| **1. Basic Design / Wireframe** | Có thay đổi luồng nghiệp vụ hoặc layout màn hình không? | | Thấp / Vừa / Cao |
| **2. Detail Spec (SRS 7 mục)** | Cần bổ sung thêm `REQ-` hay `BR-` mới không? | | Thấp / Vừa / Cao |
| **3. API & DTO Contracts** | Có thay đổi tham số request / response payload không? | | Thấp / Vừa / Cao |
| **4. Domain Validation** | Có thêm điều kiện biên logic nghiệp vụ không? | | Thấp / Vừa / Cao |
| **5. Database / Migration** | Cần thêm bảng, thêm cột, hay sửa quan hệ? Có an toàn với data cũ không? | | Thấp / Vừa / Cao |
| **6. Web Frontend** | Màn hình nào trên Web Portal bị thay đổi? | | Thấp / Vừa / Cao |
| **7. Zalo Mini App / Mobile** | Form nhập liệu trên Zalo có cần cập nhật đồng bộ không? | | Thấp / Vừa / Cao |
| **8. Test Suite** | Cần cập nhật Unit Test, Integration Test hay E2E Test nào? | | Thấp / Vừa / Cao |

## 3. QUYẾT ĐỊNH ĐẦU RA (TRIAGE VERDICT)
- **CHẤP THUẬN (APPROVED)**: Gán mã `TASK-XX` hoặc `CR-XXXX-XX`, cập nhật vào `Specification/02_BASIC_DESIGN/DANH_SACH_TIEN_DO_BASIC_DESIGN.md` và bàn giao cho Agent BA.
- **TỪ CHỐI / HOÃN (DEFERRED / REJECTED)**: Ghi chú lý do rõ ràng vào Backlog để bảo vệ tiến độ hiện tại.
