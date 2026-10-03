---
name: md-to-docx-review
description: Chuyển tài liệu Markdown, đặc biệt SRS theo template dự án, sang DOCX có định dạng đọc duyệt và kiểm tra mở được. Dùng khi cần tạo bản Word để gửi reviewer/PO/QA.
metadata:
  short-description: Xuất SRS Markdown thành Word để duyệt
---

# Markdown to DOCX Review

## Mục tiêu

Tạo một bản `.docx` từ file `.md` làm bản phát hành để người duyệt đọc và bình luận. File Markdown vẫn là nguồn chuẩn; không sửa nội dung nghiệp vụ trong lúc convert.

## Quy trình bắt buộc

1. Nhận đường dẫn Markdown và đường dẫn output `.docx`. Nếu chưa được chỉ rõ, đặt output cạnh file Markdown, cùng basename.
2. Đọc Markdown và kiểm tra nhanh: có đúng 7 mục SRS nếu là SRS; không có marker chưa chủ ý; bảng không bị thiếu dấu `|`.
3. Chạy [`scripts/md_to_docx.py`](scripts/md_to_docx.py). Bộ chuyển đổi giữ heading, bảng, danh sách, block code/Mermaid và ảnh Markdown có đường dẫn cục bộ; cấu hình trang A4 ngang để bảng ma trận dễ đọc.
4. Kiểm tra `.docx` bằng LibreOffice headless: mở/chuyển sang PDF, kiểm tra số trang và bảo đảm không có lỗi. Nếu có thể, render vài trang đầu để xem bảng không bị cắt.
5. Báo rõ file `.docx`, file nguồn `.md`, thời điểm sinh và các giới hạn còn lại. Không tuyên bố “đã duyệt”; DOCX chỉ là bản trình duyệt.

## Quy tắc nội dung

- Không tự đổi số liệu, câu chữ nghiệp vụ, mã REQ, role, quyền hoặc API.
- Mermaid không được giả vờ là sơ đồ đã render; giữ dạng code monospace và ghi chú người duyệt xem sơ đồ trực quan trong Markdown nếu cần.
- Marker `⛳ CẦN XÁC NHẬN`, `[MỚI THIẾT KẾ — CHƯA LẬP TRÌNH]` và trạng thái DỰ THẢO phải được giữ nguyên.
- Nếu file có ảnh, chỉ nhúng ảnh cục bộ tồn tại; ảnh thiếu phải để nguyên alt text và báo trong kết quả.
- Khi convert lại, có thể ghi đè DOCX cũ nếu người dùng yêu cầu; không ghi đè file Markdown.

## Cách gọi

```bash
python3 md-to-docx-review/scripts/md_to_docx.py \
  TRUYXUAT/SRS-RBAC-PHAN-QUYEN-TRACEPRO.md \
  TRUYXUAT/SRS-RBAC-PHAN-QUYEN-TRACEPRO.docx
```

Sau đó kiểm tra:

```bash
soffice --headless --convert-to pdf \
  --outdir /tmp/srs-docx-check \
  TRUYXUAT/SRS-RBAC-PHAN-QUYEN-TRACEPRO.docx
```

`python-docx` và LibreOffice là dependency runtime. Nếu thiếu, báo dependency cụ thể; không tự cài package ngoài phạm vi người dùng yêu cầu.
