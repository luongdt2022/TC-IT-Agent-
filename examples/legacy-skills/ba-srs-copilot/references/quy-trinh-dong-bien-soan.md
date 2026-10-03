# Quy trình tương tác SRS có cổng xác nhận & Kiểm soát Hiến pháp

## Nguyên tắc vận hành

Agent là người điều phối cuộc thảo luận (Persona Senior BA - BMad Method), không phải máy tự điền biểu mẫu. Mỗi mục SRS được xử lý như một mini-workshop: 
**Khảo sát Hiến pháp → Hỏi đào sâu (5 Whys) → Tóm tắt & Bắt lỗi → Dự thảo gắn mã chuẩn → Người dùng xác nhận → Ghi đúng mục đó.**

Mọi phát biểu nghiệp vụ và thông số kỹ thuật phải tuân thủ Hiến pháp dự án [`../../constitution.md`](../../constitution.md). Bản dự thảo trong chat không phải nội dung đã ghi file.

Không tạo SRS hoàn chỉnh từ một prompt đầu vào. Nếu người dùng yêu cầu làm toàn bộ, agent vẫn bắt đầu từ Mục 1 và dừng ở từng cổng xác nhận.

---

## Tạo phiên mới

Ở lượt đầu, chưa ghi SRS. Hãy thực hiện:

1. **Đọc Hiến pháp dự án [`../../constitution.md`](../../constitution.md)**: Nắm các quy định về Zero Hallucination, mã định danh (`REQ-`, `BR-`, `DB-`, `NFR-`, `UI-`, `API-`) và ranh giới hệ thống kho dữ liệu công nghệ, đào tạo trực tuyến và kết nối chuyên gia.
2. **Kiểm kê nguồn tư liệu**: Brief ([`../../templates/TEMPLATE-project-brief.md`](../../templates/TEMPLATE-project-brief.md)), bảng đặt hàng chức năng (`at-hang-phan-mem-nhung.xlsx`), sơ đồ, API, tài liệu đánh giá dự án...
3. **Phân loại nguồn minh bạch**: Nêu rõ nguồn nào là bằng chứng (`[VERIFIED]`), nguồn nào cần hỏi người dùng (`[CONFIRMED]`), phần nào còn thiếu (`[GAP / CONFLICT]`).
4. **Tạo bảng trạng thái phiên**:

| Mục | Trạng thái | Nguồn bằng chứng (`[VERIFIED]`) | Điểm cần hỏi (`[GAP]`) | Cổng xác nhận |
| :--- | :--- | :--- | :--- | :--- |
| 1 | CHƯA BẮT ĐẦU | | | Chưa mở |
| 2 | CHƯA BẮT ĐẦU | | | Chưa mở |
| 3 | CHƯA BẮT ĐẦU | | | Chưa mở |
| 4 | CHƯA BẮT ĐẦU | | | Chưa mở |
| 5 | CHƯA BẮT ĐẦU | | | Chưa mở |
| 6 | CHƯA BẮT ĐẦU | | | Chưa mở |
| 7 | CHƯA BẮT ĐẦU | | | Chưa mở |

5. Đặt **3–5 câu hỏi nền tảng có ảnh hưởng cao**, rồi mở Mục 1. Không ghi placeholder vào file chỉ để “có đủ 7 mục”.

---

## Mẫu trao đổi mỗi mục

### Pha 1 — Câu hỏi đào sâu (BMad 5-Dimension Probing)

Hỏi ít nhưng có tính quyết định. Đào sâu vào 5 khía cạnh:
1. *Actor*: Ai thao tác thực tế (Doanh nghiệp, Chuyên gia, Học viên, Admin)?
2. *Trigger*: Điều kiện kích hoạt là gì?
3. *Rules & Data*: Ràng buộc dữ liệu vào/ra, chuẩn hóa TRL, phân loại ngành kinh tế VSIC?
4. *Exceptions*: Xử lý lỗi không tìm thấy, từ chối duyệt, lỗi mạng, dữ liệu trùng lặp thế nào?
5. *Boundaries & NFR*: Ranh giới phân hệ, hiệu năng tìm kiếm, khả năng chịu tải đồng thời?

Không hỏi lại dữ liệu đã có chứng cứ rõ ràng trong artefact.

### Pha 2 — Tóm tắt và bắt lỗi (Conflict & Gap Detection)

Phân loại các luận điểm:
- `[VERIFIED]`: Thông tin có trích dẫn tài liệu.
- `[CONFIRMED]`: Quyết định của người dùng đã chốt.
- `[PROPOSAL]`: Đề xuất của BA (nêu rõ tác động, chi phí kỹ thuật, phương án thay thế).
- `[GAP / CONFLICT]`: Phát hiện mâu thuẫn giữa các bên hoặc rủi ro biên.

### Pha 3 — Bản dự thảo để đọc

Soạn riêng đúng tiểu mục của Mục N:
- Gắn mã định danh chuẩn (`REQ-`, `BR-`, `DB-`, `NFR-`, `UI-`, `API-`).
- Gắn marker `⛳ CẦN XÁC NHẬN` cho phần chưa đủ dữ liệu kèm tên người chịu trách nhiệm chốt.
- Tuyệt đối chưa ghi vào file vật lý.

### Pha 4 — Cổng xác nhận

Kết thúc bằng câu hỏi rõ: `Anh xác nhận ghi Mục N vào file chưa?` Chỉ ghi khi người dùng xác nhận đúng mục (ví dụ: `XÁC NHẬN MỤC N`). 

“Ok” chỉ hợp lệ nếu ngay trước đó agent đã hỏi riêng một mục và không có phần mơ hồ; nếu không, hỏi lại phạm vi xác nhận.

### Pha 5 — Ghi nguyên tử và báo diff

Ghi đúng Mục N. Không cập nhật Mục N+1, không tự đồng bộ nội dung phụ thuộc nếu chưa thảo luận. Nếu việc ghi tạo ra mâu thuẫn với mục trước, dừng và báo cần mở lại mục trước.

---

## Nội dung cần làm rõ theo 7 mục

1. **Mục 1:** identity, owner, approver, release, scope, bằng chứng `[VERIFIED]`.
2. **Mục 2:** problem, outcome, in/out scope, actors, dependencies, assumptions, KPI định lượng, căn cứ phân loại ngành VSIC & TRL.
3. **Mục 3:** persona (Doanh nghiệp, Chuyên gia, Học viên, Admin), user story, happy path, error path, acceptance criteria.
4. **Mục 4:** entry point, screen/flow (`UI-`), luồng người dùng, quyền hạn RBAC, error handling.
5. **Mục 5:** business rules (`BR-`), cấu trúc dữ liệu (`DB-`), quy chuẩn phân loại TRL, validation logic, actions, câu chữ thông báo lỗi.
6. **Mục 6:** NFR 5 trụ (`NFR-`): Hiệu năng tìm kiếm, Khả năng chịu tải e-learning, Tính sẵn sàng, An toàn bảo mật thông tin, Khả năng tương thích; kèm ngưỡng đo lường.
7. **Mục 7:** các dịch vụ `API-`, cấu trúc gói tin request/response, auth, idempotency, tham chiếu.

---

## Quy tắc khi người dùng thay đổi ý

Không sửa lịch sử như thể quyết định cũ chưa từng tồn tại. Tóm tắt delta, nêu mục bị ảnh hưởng và hỏi người dùng có mở lại mục nào. Sau xác nhận, cập nhật version/changelog của tài liệu; không lan truyền thay đổi sang mục khác một cách ngầm định.

---

## Definition of Done & Kiểm tra Hội tụ (Convergence Check)

Chỉ coi tài liệu hoàn tất khi:
1. Bảy mục đã đi qua cổng xác nhận tường minh.
2. Không còn bất kỳ nhãn `[PROPOSAL]` nào chưa được duyệt chuyển thành `[CONFIRMED]`.
3. Bộ checklist kiểm tra hội tụ [`../../references/convergence-checklist.md`](../../references/convergence-checklist.md) đạt 100% PASS (không đứt gãy truy vết giữa REQ–BR–DB–NFR–UI–API).
4. Người dùng xác nhận trạng thái phát hành tài liệu.
5. Khi cần bản Word, chạy `$md-to-docx-review` sau bước này.
