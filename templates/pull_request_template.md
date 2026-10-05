### 📌 1. THÔNG TIN CHUNG (OVERVIEW)
- **Task liên quan**: `specs/TASK-[XX]` (hoặc Issue `#...`)
- **Traceability IDs**: `REQ-[XXX]`, `BR-[XXX]`, `DB-[XXX]`, `UI-[XXX]`, `API-[XXX]`
- **Loại thay đổi**:
  - [ ] 🚀 Tính năng mới (New Feature)
  - [ ] 🐛 Sửa lỗi (Bugfix)
  - [ ] 🔨 Cải tiến cấu trúc / Tối ưu hóa (Refactor / Optimization)
  - [ ] 🗄️ Cập nhật CSDL / Migration (DB Schema)
  - [ ] 🛡️ An ninh / Phân quyền (Security / RBAC)

---

### 📝 2. TÓM TẮT THAY ĐỔI (SUMMARY)
- *Mô tả ngắn gọn 2-3 câu về bối cảnh, giải pháp kỹ thuật và các điểm lưu ý:*
  - ...

---

### 🛡️ 3. DEVELOPER SELF-REVIEW CHECKLIST (Bắt buộc tích đủ trước khi gán Reviewer)

#### A. Kiến trúc & Clean Architecture
- [ ] Controller / Minimal API chỉ nhận Mediator/Service/UseCase, **TUYỆT ĐỐI KHÔNG** inject trực tiếp ORM Context / DbContext.
- [ ] Tầng `Domain` độc lập 100%, không tham chiếu thư viện ngoài hoặc tầng Infrastructure.
- [ ] Truy vấn (Queries) dùng Read-Only/NoTracking và trả về DTO; Lệnh ghi (Commands) gọi qua Entity/Aggregate Root methods.
- [ ] Frontend bọc component xử lý đủ 5 trạng thái UX: Loading Skeleton, Empty, Error (có nút Thử lại), Success, Partial.

#### B. CSDL, Schema & Migration (Nếu có chỉnh sửa DB)
- [ ] Migration phi phá hủy (Non-destructive): Không xóa/đổi tên cột trực tiếp, cột mới thêm có Default hoặc Nullable.
- [ ] Đã kiểm tra chặn đứng N+1 Query (dùng Eager loading hoặc Select projection).
- [ ] Đã đánh Index cho các khóa ngoại và trường lọc/tìm kiếm thường xuyên (`OrgId`, `TenantId`, `Status`, `CreatedAt`).
- [ ] Bảng trạng thái quan trọng có Concurrency Token (Optimistic Locking) chống Race Condition.

#### C. An ninh & Scoped RBAC
- [ ] Mọi endpoint mới (trừ public) đều gắn Policy phân quyền theo `Role` + `Scope` + `Action`.
- [ ] Chống IDOR: Mọi query/update dữ liệu sở hữu bắt buộc kèm điều kiện `OrgId` / `TenantId` / `UserId`.
- [ ] File Upload: Kiểm tra Magic Bytes thực tế, giới hạn kích thước tối đa, lưu trữ an toàn.

#### D. Kiểm thử & Đảm bảo chất lượng (Quality & Tests)
- [ ] Đã viết Unit Test bao phủ 100% các quy tắc trong `BR-[MODULE]-[STT]`.
- [ ] Không có assertion vô hiệu (`assertNotNull` hình thức), test assert giá trị thực tế.
- [ ] Đã build thử Release không phát sinh lỗi hoặc warning mới.
- [ ] 100% Unit Test & Integration Test chạy PASS cục bộ.

---

### 📸 4. BẰNG CHỨNG KIỂM THỬ (TEST EVIDENCE)
*(Bắt buộc đính kèm ảnh chụp màn hình UI, log chạy test PASS, hoặc response API Swagger/Postman)*
- **Kết quả Test**:
  - Log terminal chạy test pass 100%: [Ảnh chụp / log terminal]
- **Giao diện / API Response**:
  - [Ảnh chụp màn hình 5 trạng thái UX hoặc Postman response]

---

### 👥 5. CỔNG DUYỆT BẮT BUỘC (STAGE-GATE APPROVAL)
*Chỉ được phép merge khi cả 2 cổng dưới đây đều được tích xác nhận và Approve:*

- [ ] **Gate 3: TechLead / SA Review** (Xác nhận tính toàn vẹn Clean Architecture, Schema CSDL, An ninh RBAC, N+1 Query).
  - *Reviewer (SA)*: `@reviewer_username`
  - *Kết luận*: `[ ] APPROVED` | `[ ] REQUEST CHANGES`
- [ ] **Gate 4: QC Verification** (Xác nhận kiểm thử 3 tầng, kiểm thử góc khuất Edge-case và E2E Flow).
  - *Reviewer (QC)*: `@qc_username`
  - *Kết luận*: `[ ] VERIFIED PASS` | `[ ] REJECTED`
