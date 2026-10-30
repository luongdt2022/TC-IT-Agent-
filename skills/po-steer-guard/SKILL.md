---
name: po-steer-guard
description: "Kỹ năng Điều Phối & Giám Sát Thiết Quân Luật Dev - QC dành cho PO/PM. Chặn đứng thói quen làm ẩu, bỏ bước, làm đối phó của Dev (ép checklist đầy đủ) và QC (thẩm vấn data test chuẩn, kiểm thử 4 tầng không mock/hardcode, định lượng test case/luồng, và hoài nghi tuyệt đối khi báo 0 bug)."
metadata:
  short-description: Điều hướng, giám sát và kiểm soát chất lượng Dev & QC
---

# Kỹ Năng: po-steer-guard (Điều Phối & Giám Sát Thiết Quân Luật Dev - QC)

> **Role Chịu Trách Nhiệm**: PO/PM Agent (`po-pm`) — Product Owner & Project Manager.  
> **Mục Tiêu Tối Thượng**: Triệt tiêu thói quen bỏ bước, làm ẩu, làm cho xong của Dev và QC; thiết lập kỷ luật kiểm chứng thép trong mọi lần điều hướng và chuyển giao công việc.

---

## 1. NGUYÊN TẮC TƯ DUY ĐIỀU PHỐI CỦA PO (CORE MINDSET)

1. **Dev và QC có xu hướng bẩm sinh là làm tắt, bỏ bước và làm cho xong**:
   - Dev thường vội vã viết code cho chạy được giao diện/API bề mặt mà bỏ qua xử lý lỗi biên, bỏ qua 5 trạng thái UX, mock tạm dữ liệu hoặc không viết test.
   - QC thường kiểm tra hời hợt vài case Happy Path trên giao diện tĩnh, lười chuẩn bị data test thật, lạm dụng mock/hardcode và vội vàng kết luận "Tất cả đều PASS".
2. **PO là Tổng tư lệnh chất lượng — Không tin lời nói, chỉ tin bằng chứng**:
   - PO tuyệt đối không chấp nhận báo cáo kiểu "Em làm xong rồi", "Em test hết rồi không thấy lỗi gì".
   - Mọi lời khẳng định phải đi kèm file log, seed data CSDL thật, số lượng test case cụ thể và mã nguồn kiểm chứng.
3. **Triết lý kiểm thử sống còn: "QC phải tìm ra bug thì mới được việc"**:
   - Không có phần mềm nào mới viết xong mà hoàn hảo không tì vết.
   - **Ngay khi QC báo "Không có bug / 100% Pass ngay lần đầu" là PO PHẢI LẬP TỨC NGHI NGỜ!**
   - Báo cáo 0 bug là dấu hiệu rõ nhất của việc test đối phó, test nông cạn hoặc bỏ bước.

---

## 2. QUY TRÌNH ĐIỀU HƯỚNG VÀ KIỂM SOÁT DEV (DEV CHECKLIST OVERSIGHT)

Mỗi lần PO giao việc hoặc nghiệm thu tiến độ của Dev, PO bắt buộc phải đối soát **Checklist 6 Điểm Thép**:

| STT | Tiêu Chí Kiểm Soát Dev | Cách PO Đối Soát & Kiểm Chứng | Mức Độ |
| :---: | :--- | :--- | :---: |
| **D1** | **Bám Sát 1:1 `tasks.md`** | Kiểm tra danh sách task có được phân rã chi tiết từ `plan.md` không. Cấm gộp task chung chung. Từng task hoàn thành phải có bằng chứng commit/file cụ thể mới được tick `[x]`. | **CHẶN** |
| **D2** | **Pre-flight Grounding** | Đã đọc kỹ schema CSDL thật (PostgreSQL/MySQL/SQL Server) và DTO hiện hữu chưa? Tuyệt đối cấm Dev bịa tên bảng, bịa trường dữ liệu hoặc đoán mò API. | **CHẶN** |
| **D3** | **Đầy Đủ 3 Tầng Kỹ Thuật** | Kiểm tra mã nguồn có đủ 3 tầng: `[BE]` Service/Repository/Controller $\rightarrow$ `[FE]` Component/Page $\rightarrow$ `[Test]` Unit Test cho 100% quy tắc nghiệp vụ `BR-*`. Thiếu 1 tầng $\rightarrow$ Đánh trượt ngay. | **CHẶN** |
| **D4** | **Chuẩn Hóa 5 Trạng Thái UX** | Kiểm tra Frontend có bọc component qua `<Async>` chuẩn không? Phải xử lý đủ 5 trạng thái: `Loading`, `Empty`, `Error`, `Success`, `Partial`. Cấm chỉ làm mỗi Success rồi bỏ mặc Error/Empty. | **CHẶN** |
| **D5** | **Kỷ Luật Zero-Mock Tận Gốc** | Quét mã nguồn kiểm tra: Có `fakeItem`, `fakeCode`, static dummy array trong khối `catch` hay không? Dữ liệu hiển thị có gọi API và lấy từ CSDL thật không? Phát hiện mock ngầm $\rightarrow$ Kỷ luật lập tức. | **CHẶN** |
| **D6** | **Kỷ Luật Test Immobility** | Kiểm tra Git Diff: Dev có tự ý sửa đổi điều kiện assertion của test case hoặc giảm bớt tiêu chí để test pass đối phó không? | **CHẶN** |

> **Hành động của PO**: Nếu Dev vi phạm bất kỳ mục nào từ D1 đến D6 $\rightarrow$ PO **TỪ CHỐI BÀN GIAO SANG QC**, yêu cầu Dev hoàn thành đúng checklist trước khi tiếp tục.

---

## 3. BỘ 3 THẨM VẤN THÉP DÀNH CHO QC (QC STRICT AUDIT)

Khi QC nộp kết quả hoặc đề xuất chuyển sang Gate tiếp theo, PO bắt buộc phải thực hiện **3 câu hỏi thẩm vấn thép**:

### 🎯 Ý 1: Chuẩn Bị Data Test & Kiểm Thử 4 Tầng (Nghiêm Cấm Mock & Hardcode)
- **Chuẩn bị Data Test chuẩn chưa?**
  - Data test phải là dữ liệu sống thực tế được khởi tạo (seed) trực tiếp vào CSDL thật, có đầy đủ ràng buộc toàn vẹn khóa ngoại (FK), index và trạng thái logic.
  - Tuyệt đối cấm QC dùng dữ liệu giả lập, dữ liệu rác không đúng cấu trúc schema thật.
- **Đã kiểm thử Blackbox và đủ 4 tầng kiểm thử chưa?**
  1. *Tầng 1 (Unit Test logic)*: 100% quy tắc nghiệp vụ (`BR-*`) đã pass?
  2. *Tầng 2 (Contract Test API)*: DTO giữa Client và Backend có lệch trường, lệch kiểu dữ liệu không?
  3. *Tầng 3 (Database Integration Test)*: Đã query trực tiếp vào DB thật để kiểm tra trạng thái dòng ghi (Row state) sau khi thực hiện thao tác chưa? (Cấm shallow assertion chỉ nhìn giao diện `is_visible()`).
  4. *Tầng 4 (E2E & Scoped RBAC Fuzzing)*: Đã chạy Playwright trên trình duyệt thật và fuzzing ma trận phân quyền các vai trò chưa?
- **Kỷ luật Zero-Mock của QC**:
  - **Tuyệt đối nghiêm cấm QC mock API responses hoặc hardcode kết quả** để pass test.
  - QC phải chứng minh mọi request đi qua mạng thật, controller thật, service thật và DB thật.

### 🎯 Ý 2: Định Lượng Rõ Ràng — Số Test Case, Số Luồng & Độ Phủ Spec
- **Có bao nhiêu test case?**
  - Báo cáo phải định lượng chính xác: Có bao nhiêu test case Happy Path? Bao nhiêu test case Negative? Bao nhiêu test case Boundary / Lỗi biên? Bao nhiêu test case phân quyền RBAC?
- **Bao nhiêu luồng hành trình người dùng (User Journeys)?**
  - Liệt kê tường minh từng luồng người dùng (ví dụ: Tạo mới $\rightarrow$ Duyệt $\rightarrow$ Thanh toán $\rightarrow$ Hủy $\rightarrow$ Xem báo cáo).
- **Đã phủ kín ma trận truy vết khép kín chưa?**
  - Đối soát 1:1 với `spec.md`: Từng mã `REQ-*` và `BR-*` có test case tương ứng không? Nếu còn mã mồ côi (chưa có test) $\rightarrow$ Yêu cầu bổ sung ngay.

### 🎯 Ý 3: Phản Xạ Hoài Nghi Khi Báo 0 Bug & Tiêu Chí "QC Phải Tìm Ra Bug"
- **Nguyên tắc vàng**: *"QC không tìm ra bug thì hoàn toàn vô dụng!"*
- Khi QC nộp báo cáo "Không có bug / Pass 100%":
  - **PO LẬP TỨC ĐẶT DẤU HỎI HOÀI NGHI**: *Liệu QC có đang test hời hợt? Có bỏ qua lỗi biên? Có chạy kịch bản phá hoại không?*
  - PO **BÁC BỎ BÁO CÁO 0 BUG** nếu QC không chứng minh được đã thử nghiệm các kịch bản phá hoại (Stress, Chaos, Boundary, Abuse Cases, Spam click, Network drop, SQLi/XSS payload, Concurrency race condition).
- **Yêu cầu QC thực hiện kịch bản phá hoại**:
  - Gửi payload vượt quá giới hạn độ dài trường dữ liệu.
  - Spam click submit liên tục 10 lần xem có bị duplicate record không (Idempotency).
  - Ngắt kết nối mạng giữa chừng khi đang submit form xem có hiển thị thông báo lỗi thân thiện không.
  - Đăng nhập tài khoản User A để truy cập ID tài nguyên của User B (kiểm tra lỗi IDOR / rò rỉ dữ liệu ngoài phạm vi).
- Chỉ khi QC đã thử toàn bộ các kịch bản phá hoại và báo cáo chi tiết các lỗi biên/nguy cơ tiềm ẩn thì PO mới xem xét phê duyệt.

---

## 4. QUY TRÌNH ĐIỀU HƯỚNG BẮT BUỘC MỖI PHIÊN LÀM VIỆC (MANDATORY STEERING FLOW)

Mỗi khi PO thực hiện điều hướng dự án (giao task mới, họp checkpoint, bàn giao Dev $\rightarrow$ QC, hoặc nghiệm thu Gate 5), PO phải tuân thủ 4 bước:

```mermaid
flowchart TD
    A["PO Bắt Đầu Điều Hướng"] --> B["BƯỚC 1: Rà Soát Dev Checklist"]
    B -->|Có task bỏ bước / Mock / Thiếu tầng| B1["PO REJECT Dev<br/>Bắt quay lại làm đủ checklist"]
    B -->|Checklist Dev Đạt Chuẩn 100%| C["BƯỚC 2: Giao Việc Cho QC & Thẩm Định Đề Bài"]
    C --> D["BƯỚC 3: Kích Hoạt Bộ 3 Thẩm Vấn Thép Cho QC"]
    D --> D1["Hỏi Data Test chuẩn chưa? 4 tầng không mock?"]
    D --> D2["Hỏi Số test case? Số luồng? Độ phủ spec?"]
    D --> D3{"QC Báo Có Bug Không?"}
    D3 -->|"QC báo 0 BUG / Pass hết"| D4["PO Nghi Ngờ & Bác Bỏ Báo Cáo<br/>Bắt QC chạy kịch bản phá hoại / tìm lỗi biên"]
    D3 -->|"QC tìm ra bug & logs xác thực"| E["BƯỚC 4: Điều Hướng Dev Sửa Lỗi & Xác Nhận Chất Lượng"]
    D4 --> D
    E --> F["PO Ký Duyệt Chuyển Chặng / Xuất Xưởng"]
```

### Bước 1: Rà soát Dev Checklist (Trước khi chuyển giao)
- PO yêu cầu Dev nộp danh sách task đã hoàn thành.
- PO kiểm tra ngẫu nhiên 2–3 file mã nguồn để xác thực: Có đủ BE-FE-Unit Test không? Có mock không? Có bọc `<Async>` không?
- Nếu phát hiện Dev làm ẩu $\rightarrow$ Trả về ngay lập tức, không khoan nhượng.

### Bước 2: Thiết lập yêu cầu kiểm thử cho QC
- PO giao spec cho QC và nêu rõ: Yêu cầu chuẩn bị data test thật trên CSDL sống, yêu cầu kiểm thử 4 tầng độc lập, nghiêm cấm mock.

### Bước 3: Kích hoạt Bộ 3 Thẩm Vấn Thép khi QC nộp báo cáo
- PO yêu cầu QC điền và trả lời 3 câu hỏi:
  1. Bằng chứng data test thật & kết quả chạy 4 tầng (không mock/hardcode)?
  2. Bảng kê số lượng test case & danh sách luồng kiểm thử?
  3. Danh sách bug/lỗ hổng/điểm yếu đã tìm được?
- Nếu QC báo "0 bug": Kích hoạt cơ chế hoài nghi, yêu cầu QC chạy test phá hoại, stress test, edge cases.

### Bước 4: Ra quyết định điều hướng
- Nếu cả Dev và QC đều vượt qua thẩm định với bằng chứng thật: PO mới ký chuyển chặng hoặc ký duyệt xuất xưởng (`po-gate` / `xong`).

---

## 5. MẪU BÁO CÁO ĐIỀU HƯỚNG PO (PO STEERING VERDICT ARTIFACT)

Khi thực hiện điều hướng, PO có thể xuất báo cáo kiểm soát theo mẫu:

```markdown
# BÁO CÁO ĐIỀU HƯỚNG & KIỂM SOÁT DEV - QC (PO STEERING REPORT)

- **Mã Epic / Feature**: [Tên Epic]
- **Thời Điểm Kiểm Tra**: [YYYY-MM-DD HH:mm]
- **Người Điều Hướng**: PO/PM Agent

### 1. KẾT QUẢ ĐỐI SOÁT DEV CHECKLIST
- [x] D1. Bám sát 1:1 tasks.md (Không gộp việc, có bằng chứng file/commit)
- [x] D2. Pre-flight Grounding (Đúng schema CSDL thật)
- [x] D3. Đủ 3 tầng ([BE] Service/API + [FE] Component + [Test] BR-*)
- [x] D4. Chuẩn hóa 5 UX States qua <Async> (Không bỏ sót Loading/Empty/Error)
- [x] D5. Kỷ luật Zero-Mock tận gốc (Không fakeItem, không dummy arrays)
- [x] D6. Kỷ luật Test Immobility (Không sửa assertion test)
-> **Đánh giá Dev**: [ĐẠT / CHƯA ĐẠT - Yêu cầu làm lại task ...]

### 2. KẾT QUẢ BỘ 3 THẨM VẤN THÉP CHO QC
- **Ý 1 (Data Test & 4 Tầng)**:
  + Nguồn data test: [DB Seed script / Fixtures sống]
  + Kết quả 4 tầng: Tầng 1 (Unit BR-*): PASS | Tầng 2 (Contract): PASS | Tầng 3 (DB Int): PASS | Tầng 4 (E2E Playwright & RBAC): PASS
  + Xác nhận Zero-Mock QC: [Đã xác nhận không mock API / không hardcode]
- **Ý 2 (Số lượng Test Case & Luồng)**:
  + Tổng test case: [XX] cases (Happy: [X], Negative: [Y], Boundary: [Z], RBAC: [W])
  + Số luồng kiểm thử: [YY] User Journeys (Liệt kê: ...)
  + Độ phủ ma trận truy vết: 100% REQ-* và BR-*
- **Ý 3 (Phát hiện Bug & Thái độ Hoài nghi)**:
  + Số bug tìm được: [ZZ] bugs (Liệt kê: P1/P2/P3...)
  + QC đã test các case phá hoại chưa: [Đã test Spam Click, Long Strings, IDOR, Broken DB]
  + Thái độ thẩm định của PO: [Hài lòng vì QC đã bới lông tìm vết ra lỗi thật / Nghi ngờ vì báo 0 bug - Bắt test lại]

### 3. KẾT LUẬN ĐIỀU HƯỚNG CỦA PO
- **Quyết định**: [CHẤP THUẬN CHUYỂN BƯỚC / TỪ CHỐI - BẮT DEV/QC LÀM LẠI]
- **Chỉ thị bước tiếp theo**: [Giao việc cụ thể]
```
