---
name: "xong"
description: "Đóng một spec/tính năng đã làm xong: kiểm tra thật checklist Definition of Done, cập nhật living docs trong docs/system/ (hoặc docs/), đổi Status sang Shipped và cập nhật specs/README.md / specs/ROADMAP.md. Chạy khi vừa hoàn thành một spec, trước khi merge."
argument-hint: "Số spec cần đóng, ví dụ: 003 hoặc EPIC-01 (để trống thì tự dò)"
compatibility: "Cần docs/ (hoặc docs/system/), specs/ (xem AGENTS.md / WORKFLOW.md)"
user-invocable: true
disable-model-invocation: false
---

## Đầu vào từ người dùng

```text
$ARGUMENTS
```

Thường là mã định danh spec (`003`, `EPIC-01-AUTH`, hoặc đường dẫn). Để trống thì tự dò.

## Nhiệm vụ

Đóng một spec cho đúng quy trình chất lượng doanh nghiệp. Đây là **cổng chặn merge**, không phải thủ tục hình thức.

Việc quan trọng nhất của skill này là **cập nhật tài liệu sống (Living Docs)** — mắt xích hay đứt nhất trong
cả quy trình. `specs/` ghi *ý định tại một thời điểm*; `docs/system/` (hoặc `docs/01-basic-design/`) mô tả *hệ thống hiện tại*.
Thành viên mới và AI Agent đọc tài liệu hiện tại. Nếu tài liệu hiện tại sai thì cả đội làm sai theo.

## Luật bất di bất dịch

1. **KHÔNG tick suông.** Mỗi mục checklist phải được **kiểm chứng thật** bằng cách đọc file,
   grep test, chạy test thực tế, so sánh nội dung. Không được kết luận "chắc là có" hay suy từ tên file.
2. **Có mục chặn không đạt thì KHÔNG đổi Status.** Dừng lại, báo cáo, để người dùng quyết. Đổi
   `Status: Shipped` khi checklist chưa qua là phá hỏng chính lý do skill này tồn tại.
3. **Không sửa spec đã `Shipped`.** Nếu spec đang đóng vốn đã ở trạng thái `Shipped`, dừng và
   báo — có thể người dùng nhầm mã spec.
4. **Living doc viết ở thì hiện tại.** "Hệ thống làm X", không phải "sẽ làm X". Và chỉ mô tả cái
   **đã thực sự chạy được**, không phải cái spec dự định.

## Các bước

### Bước 1 — Xác định spec

Nếu người dùng cung cấp mã spec → dùng mã đó. Nếu để trống, dò theo thứ tự:

1. Tên nhánh git hiện tại
2. Thư mục spec được chỉnh sửa gần nhất trong `specs/`
3. Không dò được → hỏi người dùng, không suy đoán bừa bãi

Đọc `spec.md` của spec đó. Ghi nhận:

- `Status:` hiện tại
- Có header `Amends: [ID]` không
- **Vùng bị chạm**: module hoặc miền nghiệp vụ bị tác động bởi tính năng này.

### Bước 2 — Chạy checklist, kiểm chứng thật

Checklist nghiệm thu xuất xưởng (Definition of Done - Gate 5):

| # | Tiêu chí | Cách kiểm chứng | Mức độ |
|---|---|---|---|
| 1 | **Kiểm thử ranh giới / Phân quyền / Cô lập dữ liệu** | Grep test kiểm tra logic phân quyền (RBAC) và cô lập dữ liệu (Multi-tenant/User boundary) cho endpoint/hàm mới. Phải thấy assert cụ thể (401/403/404 hoặc exception). | **Chặn** |
| 2 | **Kiểm thử quy tắc nghiệp vụ (BR-*)** | Kiểm tra toàn bộ mã kiểm thử Unit / Integration kiểm chứng các quy tắc nghiệp vụ `BR-*` đã pass 100%. | **Chặn** |
| 3 | **Kiểm thử hợp đồng / Tương thích API** | Spec có thay đổi hợp đồng DTO giữa Frontend và Backend hoặc giữa các Microservices không? Nếu có, kiểm tra Contract Test tương ứng. | **Chặn** |
| 4 | **Cập nhật Living Docs phản ánh hiện trạng** | Đọc living doc của các vùng bị chạm (`docs/system/<vùng>.md` hoặc `docs/`), so sánh với những gì code thực tế đã làm. Xem Bước 3. | **Chặn** |
| 5 | **ADR cho quyết định một chiều** | Spec có chốt quyết định một chiều nào (công nghệ lõi, cấu trúc schema CSDL, giải pháp bảo mật)? Nếu có, kiểm tra `docs/decisions/` đã có ADR chưa. | **Chặn** |
| 6 | **Cập nhật Status và Roadmap** | Cập nhật `Status: Shipped` và đánh dấu hoàn thành trên Roadmap. Xem Bước 4. | Tự làm |

Khi không tìm thấy test: **nói rõ đã grep cái gì mà không thấy**, để người dùng phân biệt được
"thiếu test thật" với "test có nhưng đặt tên khác nên grep trượt".

### Bước 3 — Cập nhật living doc (việc chính)

Với mỗi vùng/module bị chạm:

1. Đọc tài liệu hiện hành của vùng đó (`docs/system/<vùng>.md` hoặc `docs/`).
2. Đọc spec + xem mã nguồn thực tế đã làm gì (code là chân lý cuối cùng).
3. Tìm những chỗ tài liệu **không còn đúng**:
   - Nội dung mô tả sai so với code hiện tại
   - Endpoint / Interface / Service mới chưa được liệt kê
   - Trường dữ liệu, tham số, trạng thái mới chưa có
   - Mục "Spec liên quan" thiếu spec này
4. Viết lại tài liệu thành **mô tả hiện trạng thật** và cập nhật Trạng thái thành `Hoạt động`.

Trình bày thay đổi cho người dùng xem trước khi ghi nếu thay đổi lớn. Sửa nhỏ thì ghi thẳng rồi báo cáo.

### Bước 4 — Đóng spec

**Chỉ làm bước này khi mọi mục Chặn đều đạt.**

1. Đổi header trong `spec.md`: `**Status**: Shipped <YYYY-MM-DD>`.
2. Cập nhật `specs/README.md` hoặc `specs/ROADMAP.md`: chuyển trạng thái sang `[x] Shipped`.
3. Nếu spec này có `Amends: [ID]`, cập nhật spec cũ tương ứng (Superseded nếu thay thế toàn bộ).

### Bước 5 — Báo cáo

Ngắn gọn:

- Mã spec và tên tính năng đã đóng
- Kết quả kiểm chứng checklist (Pass/Fail)
- Các file tài liệu Living Docs đã cập nhật
- Gợi ý commit message chuẩn conventional commit.

## Không làm gì trong skill này

- Không viết code hay test hộ (báo thiếu, để người dùng quyết định viết)
- Không ghi ADR (đó là việc của `/chot`)
- Không sửa constitution
- Không tự merge hay push khi chưa có lệnh
