---
name: srs-standardized-authoring
emoji: 📄
description: Soạn và rà soát tài liệu đặc tả yêu cầu phần mềm (SRS/PRD) chuẩn TracePro — khung 7 mục, căn cứ pháp lý, độ phủ tính năng, đối chiếu mã nguồn, sinh tệp .docx. Dùng khi được yêu cầu tạo, cập nhật hoặc rà soát SRS/PRD của TracePro.
source: chuyển thể cho quy trình Claude Code của TracePro từ quy ước skill `.agents/skills` nội bộ
license: MIT
---

# Soạn SRS chuẩn TracePro

## ⚠️ ĐỌC TRƯỚC — hai việc bắt buộc làm ngay

**1. Mở biểu mẫu trống và viết đè lên nó.** Đừng tự dựng cấu trúc từ đầu:

```
Specs/00-CHUAN-TAI-LIEU/templates/TEMPLATE-SRS-7-muc.md
```

**2. Trước khi báo xong, chạy bảng kiểm ở cuối tệp này và dán kết quả vào câu trả lời.** Không dán được kết quả nghĩa là chưa xong.

> **Bài học 10/08/2026:** năm tệp SRS được soạn *có gọi kỹ năng này* nhưng vẫn vi phạm 4 trong 5 ràng buộc bắt buộc — thừa mục 8 và 9, thiếu văn bản pháp lý, thiếu ba nhóm chỉ số, không tách Phần A/B. Nguyên nhân: đọc ràng buộc rồi quên, vì không có bước kiểm bắt buộc. Bảng kiểm ở cuối tệp sinh ra từ chính sự cố đó.

---

## Tổng quan

Kỹ năng soạn và rà soát tài liệu đặc tả yêu cầu phần mềm (SRS) chuẩn TracePro.

Sản phẩm đầu ra: một tệp Markdown **đúng bảy mục** đặt dưới `Specs/04-SRS/`.

> **Nguồn chuẩn chống lệch:** skill này cùng biểu mẫu thuộc repo `docs`. Không sửa
> bản runtime ở `tracepro-docs/.claude/skills/`; đồng bộ bằng
> `scripts/sync-srs-contract.sh` rồi kiểm bằng tùy chọn `--check`.

**Đọc trước khi soạn:**

| Tệp | Dùng để |
| :--- | :--- |
| `Specs/00-CHUAN-TAI-LIEU/templates/TEMPLATE-SRS-7-muc.md` | **Biểu mẫu trống — bắt đầu từ đây** |
| `Specs/00-CHUAN-TAI-LIEU/quy-uoc-BA.md` | Quy ước viết, hệ mã, quy trình thay đổi |
| `Specs/00-INDEX.md` | Danh sách cảnh báo mở, quyết định đã chốt |
| `Specs/03-PHAM-VI/ma-tran-tinh-nang.md` | Mã tính năng `F-xx` để gắn |
| `Specs/02-NGHIEP-VU/persona-va-vai-tro.md` | Persona `P1`–`P4` và 14 vai trò hệ thống |
| `Specs/01-CAN-CU-PHAP-LY/so-dang-ky-VBQPPL.md` | Căn cứ pháp lý đã xác minh |

---

## Nhãn tiếng Việt — bắt buộc từ 26/08/2026

Biểu mẫu chuẩn đã Việt hoá ngày 26/08/2026. **Nghĩa không đổi**, chỉ đổi nhãn.
Viết SRS mới thì dùng cột phải. Đọc bản `.docx` in trước ngày đó thì tra cột trái.

| Nhãn cũ | Nhãn hiện hành |
| :--- | :--- |
| `USER STORIES & ACCEPTANCE CRITERIA` | `NHU CẦU NGƯỜI DÙNG & TIÊU CHÍ CHẤP NHẬN` |
| `As a … I want to … So that …` | `Là … tôi cần … để …` |
| `GIVEN / WHEN / THEN / AND` | `BỐI CẢNH / KHI / THÌ / VÀ` |
| `TỔNG QUAN & MỤC TIÊU BUSINESS` | `TỔNG QUAN & MỤC TIÊU NGHIỆP VỤ` |
| `GIAO DIỆN UI MOCKUP & LUỒNG XỬ LÝ HỆ THỐNG` | `GIAO DIỆN MÀN HÌNH & LUỒNG XỬ LÝ` |
| `TÀI LIỆU KỸ THUẬT THAM CHIẾU & API SPECIFICATION` | `THAM CHIẾU KỸ THUẬT & ĐẶC TẢ GIAO DIỆN LẬP TRÌNH (API)` |
| `[ĐÃ CÓ TRONG CODEBASE]` | `[ĐÃ CÓ TRONG MÃ NGUỒN]` |
| `[THIẾT KẾ SPEC — CHƯA IMPLEMENT]` | `[MỚI THIẾT KẾ — CHƯA LẬP TRÌNH]` |
| `Target Release` · `Stakeholders` | `Đợt phát hành dự kiến` · `Các bên liên quan` |
| `Field Key DTO` · `Data Type` · `Required` | `Tên trường kỹ thuật (DTO)` · `Kiểu dữ liệu` · `Bắt buộc` |
| `Validation Rule` · `UI Error Message` | `Ràng buộc` · `Thông báo lỗi` |
| `Bảng endpoint` · `Method` · `Xác thực` | `Bảng đường dẫn API` · `Phương thức` · `Cần đăng nhập` |

Nguồn gốc: [`quy-uoc-BA.md §5.2`](../../../Pháp%20lý%20truy%20xuất%20nguồn%20gốc/Specs/00-CHUAN-TAI-LIEU/quy-uoc-BA.md)

> ⚠️ **Biểu mẫu thắng skill khi hai bên khác nhau.** Sửa cả hai trong cùng PR nguồn
> chuẩn và chạy kiểm đồng bộ trước khi cập nhật bản runtime.

---

## Ràng buộc bắt buộc

### R1 · Đúng bảy mục, không thừa không thiếu

Tệp phải có **chính xác** bảy tiêu đề cấp hai: `## 1.` → `## 7.` **Không được tạo mục 8, 9 hay bất kỳ mục nào khác.**

**Những thứ hay bị viết thành mục thừa — đặt vào đây:**

| Nội dung | Đặt ở |
| :--- | :--- |
| Khoảng trống đã biết · cảnh báo · rủi ro kỹ thuật | `### 7.5 Khoảng trống đã biết` |
| Liên kết sang tài liệu khác | `### 7.3 Tài liệu tham chiếu` |
| Kết luận đối chiếu mã nguồn | `### 7.4 Kết luận đối chiếu mã nguồn` |
| Lịch rà soát · nhật ký thay đổi · danh mục tự kiểm | `### 7.6 Lịch rà soát & danh mục tự kiểm` |
| Từ điển thuật ngữ riêng của tài liệu | `### 2.5 Thuật ngữ` |

### R2 · Mục 2.1 chỉ trích căn cứ pháp lý thực sự áp dụng

Bảng căn cứ pháp lý phải nêu đúng văn bản, cơ quan ban hành và điều khoản làm phát
sinh yêu cầu của phân hệ. Không sao chép sáu văn bản nền khi không có tác động trực
tiếp; tài liệu tổng quan có thể khai đầy đủ để các SRS con dẫn chiếu.

| # | Văn bản |
| :--- | :--- |
| L1 | Luật 78/2025/QH15 |
| L2 | NĐ 37/2026/NĐ-CP |
| L3 | TT 02/2024/TT-BKHCN |
| L4 | TT 27/2026/TT-BNNMT |
| L5 | TT 36/2026/TT-BKHCN |
| L6 | TT 33/2026/TT-BCT |

### R3 · Mục 2.1 khai nguyên tắc GS1

Nêu rõ mức áp dụng của: **GTIN-13/14 · GLN · SSCC · SGTIN · EPCIS 2.0**.

### R4 · Mục 2 có ba nhóm chỉ số, đúng ba tiêu đề này

Dùng **nguyên văn** ba tiêu đề dưới đây, không đổi chữ, không gộp:

```
**Nhóm 1 — Tuân thủ**
**Nhóm 2 — Hiệu quả vận hành**
**Nhóm 3 — Giảm rủi ro**
```

Mỗi nhóm ít nhất hai chỉ số **đo được bằng số**. Không viết chỉ số kiểu *"nâng cao trải nghiệm"*.

### R5 · Mục 7 tách Phần A và Phần B

| Phần | Nội dung |
| :--- | :--- |
| **Phần A** | Mẫu dữ liệu lấy từ endpoint **đã có** trong mã nguồn |
| **Phần B** | Mẫu **thiết kế** cho endpoint chưa hiện thực — ghi rõ là đề xuất của BA |

Mỗi đường dẫn API trong bảng ở `7.1` phải mang đúng một nhãn: `[ĐÃ CÓ TRONG MÃ NGUỒN]` kèm `tệp:dòng`, hoặc `[MỚI THIẾT KẾ — CHƯA LẬP TRÌNH]`.

### R6 · Hợp đồng trường dữ liệu đặt tại vị trí đọc thuận

Với màn hình form có ảnh M2, đặt bảng hợp đồng **ngay dưới từng ảnh/dải ảnh
callout tại 4.1**, không sao chép sang mục 5.3. Cột đầu chỉ dùng `#01…#N`; không
ghi mã `ACT-*`/`FLD-*`. Bảng phải có đủ bảy thông tin: callout, nhãn/control,
tên trường kỹ thuật (DTO) và kiểu, nguồn/timing tải, bắt buộc, ràng buộc, lưu/lỗi/kiểm thử.

Màn hình không có ảnh callout vẫn dùng mục `5.3`, theo bảy cột:

```
Mã UI | Nhãn hiển thị | Tên trường kỹ thuật (DTO) | Kiểu dữ liệu | Bắt buộc | Ràng buộc | Thông báo lỗi
```

Lấy từ ba nguồn: kiểu dữ liệu truyền nhận, thành phần biểu mẫu ở giao diện, và lược đồ cơ sở dữ liệu. **Thông báo lỗi ghi nguyên văn tiếng Việt** như người dùng thấy.

Tài liệu thuần quy tắc hệ thống, không có ô nhập nào, thì ghi rõ *"không áp dụng"* — đừng bỏ trống.

### R6a · Không lặp hồ sơ trường đã gắn với ảnh

Với màn hình có callout M2, ảnh phải hiển thị full-width và bảng hợp đồng nằm
ngay sau ảnh; không dùng bố cục ảnh thu nhỏ + chú giải bên cạnh, không tạo
`Field Notes` tách riêng, và mục `5.4` chỉ mô tả vòng đời form. Với màn hình
không có callout, mỗi màn hình có giao diện phải có một khối `5.4` riêng. Khai cả trường nhập,
Textview, cột bảng, tìm kiếm, bộ lọc, phân trang, nút, liên kết và thao tác hàng
loạt. Mỗi dòng nêu: mục đích; nguồn/cách cập nhật dữ liệu; mặc định, định dạng và
tập giá trị; quyền sửa và điều kiện hiển thị; ràng buộc cùng thông báo lỗi nguyên
văn; phụ thuộc và kết quả thao tác. Không dùng "tương tự" để bỏ qua hành vi.

### R6b · Mục 5.5 chuẩn hóa câu chữ giao diện

Với form hoặc luồng nghiệp vụ quan trọng, dùng ma trận `5.5` để xác nhận nhãn,
gợi ý, trạng thái rỗng, câu xác nhận và thông báo lỗi. Câu lỗi phải chỉ cho người
dùng hành động tiếp theo khi có thể.

### R7 · Mọi nhu cầu người dùng nêu cả persona lẫn vai trò hệ thống

Ví dụ đúng: *"**Là** `P3_Admin` có vai trò `MANAGER`, **tôi cần**…"*
Chỉ nêu một trong hai là thiếu.

### R8 · Mọi nhu cầu người dùng có ít nhất một kịch bản lỗi

Chỉ có đường thuận là chưa đạt. Đội kiểm thử không dựng được bộ ca kiểm thử từ tài liệu chỉ có đường thuận.

### R9 · Trích dẫn pháp lý ghi đủ số hiệu, năm, cơ quan ban hành, điều khoản

**Hai văn bản đang CHƯA XÁC MINH, bắt buộc gắn nhãn khi trích:**

| Văn bản | Cảnh báo |
| :--- | :--- |
| `TT 02/2024/TT-BKHCN` | CB-09 — chưa rõ còn hiệu lực |
| Mọi trích dẫn ghi `"NĐ38"` | CB-22 — không có bản gốc trong hồ sơ |

**Không đưa ý kiến pháp lý vào SRS.** Việc đó thuộc Pháp chế.

### R10 · Gắn mã cho mọi màn hình

Mỗi mã màn hình phải gắn một mã tính năng `F-xx` **và** một mã nghĩa vụ `REQ-<MIỀN>-NNN`. Không có nghĩa vụ pháp lý thì ghi rõ `KHÔNG CÓ NGHĨA VỤ PHÁP LÝ` — đừng để trống.

### R11 · Ghi rõ mức độ đối chiếu mã nguồn

Khối thông tin ở mục 1 phải có dòng **Đối chiếu mã nguồn**, nêu: ngày, mã commit của từng repo liên quan, và **mức bằng chứng** theo R12.

### R12 · Thang bằng chứng — mỗi màn hình phải khai một mức

Đây là ràng buộc quan trọng nhất về tính trung thực. Người duyệt cần biết **điều gì đã được nhìn tận mắt** và điều gì mới chỉ suy từ mã nguồn.

| Mức | Nghĩa | Được dùng khi |
| :---: | :--- | :--- |
| **M0** | Chưa xem gì — viết từ mô tả nghiệp vụ | ❌ **Không được** xuất hiện trong SRS trình duyệt |
| **M1** | Đọc mã nguồn tĩnh — biết endpoint, tên trường, quy tắc kiểm tra | Bản nháp. Phải ghi rõ *"chưa chạy thử ứng dụng"* |
| **M2** | **Có ảnh chụp màn hình thật** kèm ngày chụp và môi trường | Mức tối thiểu để trình PO duyệt |
| **M3** | Đã tự thao tác đầu-cuối, kiểm chứng cả nhánh lỗi | Bắt buộc với màn hình có ràng buộc pháp lý hoặc chặn nghiệp vụ |

**Mục `4.1` phải có mã UI, đường dẫn thật, vai trò, trạng thái màn hình và cột
"Mức bằng chứng" cho từng màn hình.** Không được để trống, không được ghi chung
chung cho cả tài liệu.

Ví dụ đúng:

| Màn hình | Đường dẫn thật | Mức | Ảnh |
| :--- | :--- | :---: | :--- |
| `UI-ONB-02` | `/dashboard/onboarding` | **M2** | `assets/onb-02-thong-tin-dn.png` — chụp 10/08/2026, môi trường thử nghiệm |
| `UI-ONB-06` | `/dashboard/batches/new` | **M1** | — chưa chụp được, cần tài khoản có sản phẩm |

> **Quy tắc duyệt:** SRS còn màn hình ở **M1** thì chỉ được duyệt ở trạng thái DỰ THẢO. Muốn lên ĐÃ DUYỆT thì mọi màn hình phải đạt **M2** trở lên, hoặc có lý do ghi rõ vì sao không chụp được.

### R12a · Ảnh tổng quan và ảnh trạng thái của màn hình dài

Với màn hình biểu mẫu dài hơn một khung nhìn, `4.1` phải bắt đầu bằng **một ảnh
tổng quan toàn trang (full-page/stitched)** có callout; nếu chưa có ảnh thật thì
dùng các dải cùng thứ tự cuộn. Mỗi ảnh/dải hiển thị full-width và theo ngay sau
là bảng hợp đồng của các callout thuộc ảnh đó; đây là nguồn đọc duy nhất cho
trường của màn hình.

Chỉ chụp ảnh riêng khi nó thể hiện trạng thái không thể đọc từ ảnh tổng quan:
danh sách xổ xuống, modal, phần hiện/ẩn theo lựa chọn, lỗi kiểm tra, cảnh báo,
kết quả thành công hoặc giao diện mobile. Tiêu đề ảnh phải nói rõ **trạng thái**,
không đặt tên theo kiểu "Bước 0" gây hiểu nhầm là nhiều ảnh trùng một màn hình.

Nếu chưa có ảnh full-page thật, **không ghép các ảnh thuộc trạng thái khác nhau**
để tạo bằng chứng giả. Dùng một bộ dải ảnh theo đúng thứ tự cuộn, ghi rõ phạm vi
của từng dải và giữ mức M2; liệt kê việc cần chụp full-page trước khi nâng M3.

---

## Cấu trúc bảy mục

### 1. Thông tin quản lý tài liệu
Tên dự án · mã tài liệu · dải mã màn hình · mã tính năng · nghĩa vụ pháp lý · phiên bản · trạng thái · ngày cập nhật · người duyệt · các bên liên quan · **đối chiếu mã nguồn (R11)**

### 2. Tổng quan & mục tiêu nghiệp vụ
- `2.1` Căn cứ pháp lý — **R2, R3, R9**
- `2.2` Bài toán nghiệp vụ
- `2.3` Ma trận phụ thuộc phân hệ
- `2.4` Mục tiêu đo lường — **R4**

### 3. Nhu cầu người dùng & tiêu chí chấp nhận
Định dạng `Là … tôi cần … để …`, tiêu chí `BỐI CẢNH … KHI … THÌ …` — **R7, R8**. Thông báo lỗi ghi nguyên văn.

> **Đổi nhãn 26/08/2026.** Toàn bộ SRS đã chuyển sang nhãn tiếng Việt; nghĩa không đổi. Bảng đối chiếu Anh–Việt ở `{specs-root}/00-CHUAN-TAI-LIEU/quy-uoc-BA.md` §5.2. **Đừng viết lại bằng nhãn tiếng Anh.**

### 4. Giao diện & luồng xử lý

#### `4.1` Ảnh chụp màn hình thật — **có sẵn công cụ, đừng bỏ qua**

> ⚠️ **Bộ chụp màn hình ĐÃ TỒN TẠI.** Trước 10/08/2026, kỹ năng này không nhắc tới nó nên mọi SRS đều dừng ở mức M1. Đừng lặp lại.

```
tracepro-docs/huong-dan-su-dung/screenshots/
├── capture-all.mjs       ← chụp toàn bộ màn hình doanh nghiệp
├── capture-admin-gov.mjs ← cổng quản trị + cổng cơ quan
├── capture-onboarding.mjs← chín bước gia nhập, đi qua từng bước
├── routes.mjs            ← bản đồ đường dẫn → tên tệp ảnh
└── seed.mjs · seed-rich.mjs ← tạo dữ liệu mẫu trước khi chụp
```

**Cách chạy:**

```bash
cd tracepro-docs/huong-dan-su-dung/screenshots
node capture-onboarding.mjs      # chín bước gia nhập
node capture-all.mjs             # 74 màn hình doanh nghiệp
```

**Điều kiện cần — hỏi người dùng nếu thiếu:**

| Tệp | Nội dung | Có sẵn? |
| :--- | :--- | :--- |
| `.cred.json` | `{"email": "...", "pass": "..."}` — tài khoản môi trường thử nghiệm | **Thường KHÔNG có. Phải hỏi.** |
| `.seed.json` | Định danh dữ liệu mẫu để dựng đường dẫn có tham số | Sinh bằng `node seed.mjs` |

Cả hai tệp chứa thông tin đăng nhập — **không bao giờ đưa vào git, không in ra màn hình, không chép vào tài liệu.**

**Bộ chụp đã có sẵn ba thứ quan trọng, giữ nguyên khi sửa:**
- Chặn lưu ảnh khi trang trả lỗi hoặc là trang *"Không tìm thấy"* — tránh ảnh rác lọt vào tài liệu
- Chụp cả desktop 1440×900 và điện thoại 414×896
- Ẩn thông báo nổi trước khi chụp cho ảnh sạch

**Nếu không chụp được:** ghi mức **M1** cho màn hình đó, **nêu rõ lý do** (thiếu tài khoản, chưa có dữ liệu, môi trường không chạy), và liệt kê đường dẫn thật để người duyệt tự mở xem. **Không bịa ảnh, không dùng ảnh của màn hình khác.**

#### `4.2` Sơ đồ tuần tự
Mermaid, phủ luồng chính và **ít nhất một nhánh hỏng**.

### 5. Yêu cầu chức năng & quy tắc nghiệp vụ
- `5.1` Quy tắc nghiệp vụ — mỗi quy tắc một mã, kèm cột *"vì sao"*
- `5.2` Bảng kiểm tra dữ liệu
- `5.3` Từ điển trường dữ liệu — **R6**

### 6. Yêu cầu phi chức năng
Năm trụ: hiệu năng · bảo mật · vết kiểm toán · khả năng liên thông · mức sẵn sàng. Yêu cầu phải **đo được**.

### 7. Tham chiếu kỹ thuật & đặc tả giao diện lập trình (API)

Ba tiểu mục đầu **theo đúng biểu mẫu chuẩn** *(bản Việt hoá 26/08/2026)* — giữ nguyên số và tên:

- `7.1` Bảng đường dẫn API — **R5**
- `7.2` Mẫu dữ liệu trao đổi — **Phần A / Phần B**
- `7.3` Tài liệu tham chiếu

Ba tiểu mục sau là **phần thêm của skill**, biểu mẫu không có nhưng cũng không cấm.
Đặt SAU `7.3` để không phá thứ tự biểu mẫu:

- `7.4` Kết luận đối chiếu mã nguồn — đếm bao nhiêu đã có, bao nhiêu chưa
- `7.5` Khoảng trống đã biết
- `7.6` Lịch rà soát & danh mục tự kiểm

---

## ✅ BẢNG KIỂM BẮT BUỘC — chạy trước khi báo xong

Thay `<FILE>` bằng đường dẫn tệp vừa soạn. **Dán kết quả vào câu trả lời.**

```bash
F="<FILE>"

# R1 — đúng bảy mục, không thừa
echo -n "R1: "; grep -oE "^## [0-9]+\." "$F" | tr -d '#. ' | tr '\n' ',' | sed 's/,$//'
echo "   → phải đúng: 1,2,3,4,5,6,7"

# R2 — căn cứ pháp lý theo đúng phân hệ
echo -n "R2: "; grep -q "Căn cứ pháp lý" "$F" && grep -q "Điều" "$F" && echo "có căn cứ + điều khoản" || echo "KIỂM TRA LẠI"

# R3 — nguyên tắc GS1
echo -n "R3: "; grep -q "GTIN" "$F" && grep -q "EPCIS" "$F" && echo "có" || echo "THIẾU"

# R4 — ba nhóm chỉ số, đúng tiêu đề
echo -n "R4: "; grep -c "Nhóm 1 — Tuân thủ\|Nhóm 2 — Hiệu quả vận hành\|Nhóm 3 — Giảm rủi ro" "$F"
echo "   → phải đúng: 3"

# R5 — tách Phần A / Phần B
echo -n "R5: "; grep -qi "Phần A" "$F" && grep -qi "Phần B" "$F" && echo "có" || echo "THIẾU"

# R6 — từ điển trường dữ liệu
echo -n "R6: "; grep -q "Tên trường kỹ thuật\|Field Key DTO\|không áp dụng" "$F" && echo "có" || echo "THIẾU"

# R6a/R6b — hồ sơ chi tiết trường và câu chữ UI
echo -n "R6a: "; grep -q "Hồ sơ chi tiết trường dữ liệu" "$F" && echo "có" || echo "THIẾU"
echo -n "R6b: "; grep -q "Ma trận chuẩn hóa câu chữ giao diện" "$F" && echo "có" || echo "KIỂM TRA THEO PHẠM VI"

# R8 — mỗi nhu cầu người dùng có kịch bản lỗi
# ⚠️ Dùng `grep -o | wc -l` (đếm LẦN XUẤT HIỆN), KHÔNG dùng `grep -c` (đếm DÒNG).
# Chỉ đếm vế đứng đầu dòng / sau <br> — tránh đếm nhầm chữ BỐI CẢNH trong văn xuôi.
# Nhận cả nhãn cũ GIVEN cho tài liệu chưa chuyển.
# Kịch bản nằm chung một ô bảng ngăn bằng <br> ⇒ grep -c đếm thiếu, báo trượt oan.
echo -n "R8: "; echo "$(grep -oE '(^|<br>)[[:space:]]*-?[[:space:]]*(BỐI CẢNH|GIVEN)' "$F" | wc -l | tr -d ' ') vế BỐI CẢNH / $(grep -oE '(Kịch bản|KB) ?[0-9]+ —' "$F" | wc -l | tr -d ' ') kịch bản / $(grep -oE '\*\*`?[A-Z]{2,4}-[A-Z0-9]+`?\*\*<br>' "$F" | wc -l | tr -d ' ') nhu cầu người dùng"
echo "   → số BỐI CẢNH phải BẰNG số kịch bản, và LỚN HƠN số nhu cầu người dùng"

# R11 — khai mức đối chiếu mã nguồn
echo -n "R11: "; grep -q "Đối chiếu mã nguồn" "$F" && echo "có" || echo "THIẾU"
echo -n "R12: "; grep -q "Mức bằng chứng" "$F" && grep -q "Đường dẫn thật" "$F" && echo "có" || echo "THIẾU"
echo -n "R12a: "; grep -q "Ảnh tổng quan\|full-page\|full page" "$F" && echo "có" || echo "KIỂM TRA THEO PHẠM VI"
```

**Chưa đạt hết thì chưa xong.** Sửa rồi chạy lại.

---

## Điều KHÔNG làm

| ❌ | Vì sao |
| :--- | :--- |
| Tạo mục 8, 9 cho phần phụ | Vi phạm R1 — đặt vào `7.4`, `7.5`, `7.6` |
| Ghi *"tích hợp API"* với cơ quan chưa cấp thông tin xác thực | Hứa quá khả năng, mất uy tín khi bị đối chiếu |
| Ghi *"luật bắt buộc"* khi sản phẩm không thuộc danh mục rủi ro | Sai sự thật pháp lý — tra danh mục trước |
| Chép nội dung từ `tracepro-docs/` sang | Trỏ liên kết, đừng chép — hai bản sẽ lệch nhau |
| Khai `[ĐÃ CÓ TRONG MÃ NGUỒN]` mà không có `tệp:dòng` | Không kiểm chứng được |
| Đưa ý kiến pháp lý | Thuộc Pháp chế, không thuộc BA |
| Bịa ảnh chụp màn hình | Ghi rõ lý do không chụp được |

---

## Sinh tệp `.docx` để in và duyệt

Phiên bản trước yêu cầu chạy `convert_specs.py`. **Rà soát 10/08/2026: tệp đó không tồn tại ở bất kỳ đâu trong workspace.** Đã thay bằng công cụ mới:

```bash
cd "Pháp lý truy xuất nguồn gốc/Specs"
python3 _md-sang-docx.py 04-SRS/06-LUONG-DAU-CUOI/SRS-ONB-man-hinh-onboarding.md
python3 _md-sang-docx.py 04-SRS/01-KH-APP/*.md      # cả thư mục
```

Cần `python-docx`. Chưa có thì `pip3 install python-docx`.

**Quy tắc:**

| | |
| :--- | :--- |
| Bản gốc | Luôn là tệp `.md`. Sửa ở đó |
| Bản `.docx` | Chỉ sinh **khi cần in hoặc gửi duyệt**. Không sửa trực tiếp — lần sinh sau sẽ ghi đè |
| Sơ đồ Mermaid | Word không render được. Công cụ giữ nguyên dạng chữ đơn cách kèm ghi chú *"mở bản .md để xem hình"* |

**Sau khi sinh, kiểm bằng lệnh sau — đừng tin vào việc "chạy không báo lỗi":**

```bash
python3 - <<'EOF'
from docx import Document; import re, sys
f = "<đường-dẫn-không-đuôi>"
d = Document(f + ".docx"); md = open(f + ".md", encoding="utf8").read()
print("bảng   :", len(d.tables), "/ markdown có", len(re.findall(r'\n\|[^\n]*\|\n\|[\s:|-]+\|\n', md)))
print("mục    :", [p.text.split('.')[0] for p in d.paragraphs
                   if p.style.name.startswith('Heading') and re.match(r'^\d+\. ', p.text)])
EOF
```

Số bảng phải khớp, và danh sách mục phải là `1 2 3 4 5 6 7`.

---

## Khi được yêu cầu RÀ SOÁT tài liệu có sẵn

1. Chạy bảng kiểm ở trên, dán kết quả.
2. Nêu từng ràng buộc không đạt kèm **vị trí cụ thể**.
3. Đề xuất cách sửa. **Không tự sửa nội dung nghiệp vụ** nếu chưa được yêu cầu — chỉ sửa vấn đề cấu trúc.
4. Đối chiếu lại `tệp:dòng` trong mục 7 với mã nguồn hiện tại. Số dòng lệch sau khi cập nhật mã nguồn là chuyện thường.
