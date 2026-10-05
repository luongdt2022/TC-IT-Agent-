# TIÊU CHUẨN KIỂM SOÁT BỀ MẶT TOÀN DIỆN & KIỂM THỬ 4 TẦNG (TC-IT-STANDARD-04)
## DÀNH CHO TOÀN BỘ CÁC DỰ ÁN SỬ DỤNG HỆ THỐNG TC IT AGENT

- **Mã Tiêu Chuẩn**: `TC-IT-STANDARD-04`
- **Phiên Bản**: `1.0.0`
- **Áp Dụng Cho**: Tất cả các Agent trong hệ sinh thái TC IT Agent (`ba`, `sa`, `dev`, `ec`, `po`, `ps`).

---

## 1. NGUYÊN NHÂN RA ĐỜI CỦA TIÊU CHUẨN

Trong quá trình phát triển dự án thực tế, các AI Agent thường xuyên mắc phải hội chứng **"Mù Cục Bộ" (Scope Tunnel Vision)**:
1. **BA chỉ nhìn vào 1 file spec hẹp**: Khi nhận yêu cầu thay đổi (CR/Delta) liên quan đến Master Data hoặc Danh mục dùng chung, BA chỉ sửa đúng spec của Epic đang giao mà không quét xem có bao nhiêu màn hình UI khác trên toàn hệ thống đang hiển thị hoặc tiêu thụ dữ liệu này.
2. **SA để UI hardcode phân mảnh**: Không thiết kế Shared Master Data Hook/SDK, để từng trang web tự hardcode mảng danh mục tĩnh độc lập (Trang chủ tự code 6 cái, Admin code 10 cái, Dashboard code text tĩnh).
3. **Dev code "Hàng Mã" (Mock UI)**: Màn hình CRUD làm ra nhưng chỉ lấy state từ mảng tĩnh trong RAM, không gọi API CSDL thật nhưng vẫn báo hoàn tất.
4. **QC kiểm thử trong "Phòng Kín"**: Lập Test Matrix chỉ dựa trên file spec hẹp của BA, chạy hàng trăm test cases backend đều xanh 100% nhưng ngoài giao diện Portal/Trang chủ của người dùng thì dữ liệu vỡ nát và mang số liệu cũ.
5. **Không có Cổng Xác Nhận với Khách Hàng (Missing User Gate)**: Tự suy diễn ngầm, không lập danh sách màn hình bị ảnh hưởng để trình Khách hàng/PO xác nhận phạm vi trước khi code.

Tiêu chuẩn `TC-IT-STANDARD-04` được thiết lập nhằm **chặn đứng vĩnh viễn 5 lỗi trên** bằng các cơ chế cơ học bắt buộc.

---

## 2. NGUYÊN TẮC BẤT BIẾN DÀNH CHO BA & PO (GREP-FIRST & SCOPE GATE)

1. **Cơ chế Grep-First Scope Discovery**:
   - Trước khi viết spec hoặc chốt scope Delta/CR, BA **bắt buộc** phải chạy lệnh quét toàn cục trên codebase:
     ```bash
     grep -rn "<TỪ_KHÓA_HOẶC_MÃ>" src/
     ```
   - Bóc tách ra **Cross-Surface Impact Matrix**:
     $$\text{Surface Impact Matrix} = \{\text{DB Tables}\} \times \{\text{APIs}\} \times \{\text{UI Screens \& Components}\}$$

2. **Cổng Duyệt Phạm Vi (User Scope Gate)**:
   - Bắt buộc xuất trình bảng Surface Impact Matrix cho User/PO kèm câu hỏi tường minh.
   - **Chỉ được chuyển giao sang SA/Dev khi User/PO gõ xác nhận rõ ràng `XÁC NHẬN SCOPE`.**

---

## 3. NGUYÊN TẮC BẤT BIẾN DÀNH CHO SA & DEV (ZERO-MOCK & CENTRALIZED CLIENT)

1. **Kiến Trúc Master Data Tập Trung Trên Client**:
   - Nghiêm cấm mọi component UI tự khai báo mảng danh mục tĩnh cục bộ.
   - Bắt buộc mọi màn hình phải lấy dữ liệu qua Hook/SDK dùng chung (`useMasterData()`, `useSectors()`) có kết nối API CSDL.

2. **Kỷ Luật Zero-Mock in Production Views**:
   - Cấm Dev bàn giao màn hình quản trị chỉ dùng mock state tĩnh. Bắt buộc 100% màn hình phải có integration API thật kết nối CSDL và hiển thị đủ 3 trạng thái: Loading, Error, Empty.

3. **Kỷ Luật Quét Sạch Toàn Cục (Global Refactor Sweep)**:
   - Khi đổi mã/enum (ví dụ: `SEC-*` sang `LV*`), Dev bắt buộc chạy lệnh:
     ```bash
     grep -rn "<MÃ_CŨ>" src/
     ```
   - **Chỉ được phép đánh dấu `[x]` vào task khi kết quả quét bằng 0.**

---

## 4. CHU TRÌNH KIỂM THỬ 4 TẦNG BẮT BUỘC DÀNH CHO QC (QUALITY GATE 4)

QC Agent (`ec`) bắt buộc phải điều phối kiểm thử theo tháp 4 tầng:

```
             / \
            /   \      TẦNG 4: Playwright E2E & Scoped RBAC Fuzzing (ec-hunt / ec-fuzz)
           / E2E \     - Hành trình người dùng & 5 UX States (<Async>)
          /-------\    - Săn lỗi biên, fuzzing phân quyền 403 Forbidden
         / Integr- \   TẦNG 3: Database Integration Tests (PostgreSQL Container thật)
        /   ation   \  - Seed dữ liệu, Unique constraints, Transaction rollback
       /-------------\ TẦNG 2: API Contracts & Architecture Boundary
      /   Contract    \ - DTO Shape, ValidationException format, Clean Arch sentinel
     /-----------------\ TẦNG 1: Unit & Invariants Tests (BR-*)
    /    Unit Tests     \- 100% Quy tắc nghiệp vụ BR-*, AggregateRoot life-cycle
   /---------------------\
```

### Tiêu Chuẩn Screen Coverage Guard:
- QC lập Test Matrix bắt buộc phải đối chiếu với **Cross-Surface Impact Matrix** của BA.
- **Cấm ký Gate 4** nếu phát hiện có bất kỳ màn hình nào trong kết quả quét mã nguồn mà chưa có bài test kiểm chứng.
- Biên bản nghiệm thu bắt buộc phải ghi nhận vào: `docs/decisions/GATE4_VERIFICATION.md`.
