---
name: "chot"
description: "Chốt các quyết định kiến trúc và kỹ thuật đã thống nhất trong phiên làm việc thành ADR trong docs/decisions/, đồng thời cập nhật docs/open-questions.md. Chạy cuối buổi làm việc, hoặc ngay sau khi vừa chốt một vấn đề quan trọng."
argument-hint: "(tuỳ chọn) mô tả quyết định muốn ghi, nếu muốn chỉ định thay vì để tự quét"
compatibility: "Cần docs/decisions/ và docs/open-questions.md (xem docs/WORKFLOW.md)"
user-invocable: true
disable-model-invocation: false
---

## Đầu vào từ người dùng

```text
$ARGUMENTS
```

Nếu người dùng có nhập nội dung, đó là quyết định họ muốn ghi — ưu tiên xử lý nội dung đó
trước, rồi mới quét thêm phần còn lại của hội thoại. Nếu để trống, quét toàn bộ phiên.

## Nhiệm vụ

Biến những gì vừa được chốt trong hội thoại thành **ADR** (Architecture Decision Record) lưu ở
`docs/decisions/`, và cập nhật `docs/open-questions.md` cho khớp.

Lý do tồn tại của skill này: quyết định quan trọng nhất thường được chốt lúc cuối buổi, đúng lúc
người ta mệt và quên ghi lại. Ba tháng sau không ai nhớ **vì sao** chốt như vậy.

## Luật bất di bất dịch

1. **KHÔNG BỊA.** Chỉ ghi những gì đã thực sự được chốt trong hội thoại này. Không suy diễn,
   không "chắc là ý người dùng muốn vậy". Không tìm thấy quyết định nào thì nói thẳng là không có.
2. **KHÔNG GHI KHI CHƯA HỎI.** Luôn trình bày danh sách quyết định định ghi và chờ người dùng
   xác nhận. Đây là bản ghi vĩnh viễn, ghi sai còn hại hơn không ghi.
3. **ADR là append-only.** Không bao giờ sửa ADR đã tồn tại. Quyết định cũ bị thay đổi thì viết
   ADR mới có dòng `Supersedes NNNN`, và chỉ sửa **trạng thái** của ADR cũ thành
   `Thay thế bởi NNNN`.
4. **Phần "Phương án đã loại" phải là thật.** Lấy từ những gì đã thực sự được cân nhắc trong hội
   thoại. Không có phương án nào được bàn thì ghi thẳng "Không cân nhắc phương án khác trong lần
   quyết định này" — đừng bịa ra hai lựa chọn giả để trông cho đầy đủ.

## Cái gì tính là quyết định

**Có tính** — đáng ghi ADR:

- Chọn công nghệ, thư viện, dịch vụ, nhà cung cấp, framework
- Chốt schema dữ liệu, cấu trúc payload, contract giữa các service / module
- Chốt phạm vi: làm hay không làm cái gì, ở phase nào
- Trả lời dứt điểm một câu hỏi đang nằm trong `docs/open-questions.md`
- Đổi hướng so với một quyết định đã ghi trước đó
- Chốt một ngưỡng, hệ số, tham số có ảnh hưởng sản phẩm (ví dụ: quota, rate limit, timeout, SLA)

**Không tính** — đừng ghi:

- Cách viết một hàm, đặt tên biến, bố cục file
- Sửa bug, refactor không đổi hành vi
- Thảo luận chưa kết luận ("chắc là...", "để xem sau", "tính sau") → cái này vào
  `open-questions.md`, không phải ADR
- Quyết định đã có ADR rồi và không thay đổi gì

## Các bước

### Bước 1 — Đọc bối cảnh hiện có

Đọc, theo thứ tự:

1. `docs/decisions/README.md` — bảng danh sách ADR và mẫu ADR đang dùng
2. Liệt kê `docs/decisions/` để biết **số ADR lớn nhất đang có** (số tiếp theo = số đó + 1,
   định dạng 4 chữ số, không tái sử dụng số của ADR bị loại)
3. `docs/open-questions.md` — để biết câu hỏi nào đang treo

Nếu `docs/decisions/` không tồn tại, tự động tạo thư mục `docs/decisions/` và file index theo mẫu chuẩn.

### Bước 2 — Quét hội thoại

Rà toàn bộ phiên làm việc hiện tại. Với mỗi thứ tìm được, phân loại:

| Loại | Xử lý |
|---|---|
| Quyết định đã chốt | → ADR mới |
| Câu hỏi mới phát sinh, chưa chốt | → thêm vào `open-questions.md` |
| Câu hỏi trong `open-questions.md` vừa được trả lời | → ADR mới + xoá khỏi `open-questions.md` |
| Quyết định cũ bị đảo | → ADR mới `Supersedes NNNN` + đổi trạng thái ADR cũ |
| Không thuộc các loại trên | → bỏ qua, không nhắc tới |

Với mỗi quyết định, xác định thêm:

- **Vùng ảnh hưởng**: module hoặc file nào trong hệ thống tài liệu (`docs/system/` hoặc `docs/01-basic-design/`)
- **Một chiều hay không**: đảo ngược có tốn re-index, migration dữ liệu lớn, hay breaking change cho
  khách hàng không? Nếu có, ghi rõ tốn cái gì. Các quyết định một chiều thường gặp: lựa chọn công nghệ lõi, cấu trúc schema cơ sở dữ liệu chính, giải pháp xác thực/phân quyền, kiến trúc giao tiếp liên dịch vụ.

### Bước 3 — Xác nhận với người dùng (BẮT BUỘC)

Trình bày gọn, mỗi quyết định 2–3 dòng:

```
Định ghi 2 ADR:

  0001 · Chọn PostgreSQL + Prisma làm nền tảng CSDL & ORM
         Vùng: database · Một chiều: Có (migration dữ liệu)
         Trả lời Q1 trong open-questions.md → sẽ xoá Q1 khỏi đó

  0002 · Áp dụng Redis Streams cho luồng xử lý sự kiện bất đồng bộ
         Vùng: messaging · Một chiều: Không

Thêm 1 câu hỏi mở mới:
  Q3 · Có cần mã hóa trường số CCCD/Email người dùng ở cấp CSDL (at-rest) không?

Ghi chứ? (có thể bảo bỏ bớt cái nào)
```

Chờ người dùng trả lời. Họ có quyền bỏ bớt, sửa lại câu chữ, hoặc huỷ toàn bộ.

Nếu **không tìm thấy quyết định nào**, nói thẳng:
"Phiên này mình không thấy quyết định nào đủ tầm ghi ADR — chủ yếu là [tóm tắt 1 dòng phiên này
đã làm gì]. Không ghi gì cả." Rồi dừng. Đừng cố nặn ra một ADR cho có.

### Bước 4 — Ghi ADR

Với mỗi quyết định được duyệt, tạo file `docs/decisions/NNNN-<slug-tieng-viet-khong-dau>.md`
theo đúng mẫu:

```markdown
# NNNN. Tiêu đề ngắn ở thể khẳng định

- **Trạng thái**: Chấp nhận
- **Ngày**: <hôm nay, YYYY-MM-DD>
- **Vùng**: <module / thư mục tài liệu hệ thống liên quan>
- **Một chiều?**: Có/Không — <nếu Có, đảo ngược tốn gì>

## Bối cảnh
<Vấn đề là gì, ràng buộc nào đang tồn tại. Lấy từ hội thoại.>

## Quyết định
<Chốt cái gì. Thể khẳng định, thì hiện tại. Cụ thể, có số nếu có số.>

## Phương án đã loại
<Những gì đã thực sự cân nhắc và vì sao không chọn. Không có thì nói không có.>

## Hệ quả
<Cái gì dễ hơn, cái gì khó hơn, cái gì phải theo dõi về sau.>
```

Quy ước viết:

- Tiêu đề ở **thể khẳng định**: "Dùng JWT kèm Redis Refresh Token", không phải "Bàn về cơ chế xác thực"
- Slug tên file không dấu, kebab-case: `0001-dung-jwt-redis-refresh-token.md`
- Liên kết ADR liên quan bằng `[[ten-file-khong-duoi-md]]`
- Nếu quyết định nâng lên thành nguyên tắc trong constitution, ghi dòng cuối:
  "Đã nâng thành constitution nguyên tắc **N. Tên**."

### Bước 5 — Cập nhật index và câu hỏi mở

1. **`docs/decisions/README.md`** — thêm dòng vào bảng Danh sách, giữ đúng thứ tự số tăng dần.
2. **`docs/open-questions.md`** — xoá câu hỏi đã được trả lời (thêm dòng trỏ tới ADR vừa ghi
   nếu hữu ích), thêm câu hỏi mới phát sinh vào đúng nhóm mức chặn.
3. Nếu có ADR bị thay thế, sửa **duy nhất** dòng trạng thái của nó thành
   `**Trạng thái**: Thay thế bởi NNNN` — không đụng phần nội dung.

### Bước 6 — Báo cáo

Ngắn gọn:

- Đã ghi ADR nào (số + tiêu đề + đường dẫn)
- `open-questions.md` thay đổi gì
- Gợi ý commit message, ví dụ:
  `docs: ghi ADR 0001-0002 (database engine, event bus)`
- Nếu ADR vừa ghi khiến tài liệu thiết kế trở nên sai lệch: **nói rõ tài liệu nào sai ở chỗ
  nào**, rồi cập nhật hoặc nhắc người dùng cập nhật.

## Không làm gì trong skill này

- Không sửa code nghiệp vụ
- Không sửa constitution (đó là việc của `/speckit-constitution`) — nhưng nếu ADR vừa ghi mâu
  thuẫn với constitution, **phải nói rõ** và đề nghị amend
- Không tạo spec
