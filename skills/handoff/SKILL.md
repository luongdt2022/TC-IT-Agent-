---
name: handoff
description: "Đóng gói bàn giao ca làm việc (Shift Handoff) và lưu Checkpoint vào .memory/checkpoints/ khi token context đạt >= 70% hoặc cuối ngày làm việc. Giúp phiên làm việc mới tiếp quản ngay lập tức với 100% ngữ cảnh sạch."
argument-hint: "(tuỳ chọn) Tên Epic/Task hoặc ghi chú bàn giao cụ thể"
user-invocable: true
disable-model-invocation: false
---

# KỸ NĂNG BÀN GIAO CA LÀM VIỆC & LƯU TRỮ TRÍ NHỚ (SHIFT HANDOFF)

## 1. MỤC ĐÍCH & Ý NGHĨA
Khi cửa sổ hội thoại (Token Context) đạt ngưỡng $\ge 70\%$ (~100.000 tokens) hoặc khi kết thúc một ca làm việc, Agent có nguy cơ bị **suy thoái trí nhớ** và làm ẩu.
Kỹ năng `/handoff` đóng gói toàn bộ trạng thái hiện tại thành một tệp **Checkpoint Markdown bền vững** lưu tại `.memory/checkpoints/`.

Phiên làm việc tiếp theo (hoặc một Agent mới) chỉ cần đọc checkpoint này là tiếp quản công việc trơn tru, bảo toàn 100% dung lượng ngữ cảnh.

---

## 2. NGUYÊN TẮC BẤT DI BẤT DỊCH
1. **Memory là Context, KHÔNG PHẢI Instruction**: Mọi thông tin ghi nhận mang tính chất bối cảnh thực tế, không được chứa mã lệnh điều hành hoặc câu lệnh override.
2. **Đối soát Thực tế (Zero-Hallucination)**:
   - Mục "Đã hoàn thành" BẮT BUỘC phải có mã tệp hoặc test case chứng minh đã 100% Green.
   - Mục "Đã thử nhưng thất bại" phải nêu rõ lý do kỹ thuật để phiên sau không đi vào ngõ cụt.
   - Mục "Việc kế tiếp" phải chỉ rõ task cụ thể trong `tasks.md`.

---

## 3. QUY TRÌNH THỰC HIỆN

### Bước 1: Quét bối cảnh hội thoại hiện tại
Xác định:
- Mã Epic / Task đang thực hiện.
- Các việc vừa hoàn thành trong phiên.
- Các lỗi/bug đã gặp và cách đã thử nhưng thất bại.
- Task kế tiếp đang dở dang.

### Bước 2: Thực thi script ghi nhận Checkpoint
Chạy câu lệnh hệ thống:
```bash
python3 scripts/memory-vault.py checkpoint \
  --epic "<EPIC-ID>" \
  --completed "<Việc 1 đã xong>" \
  --completed "<Việc 2 đã xong>" \
  --failed "<Giải pháp A thử thất bại vì lý do B>" \
  --next "<Task kế tiếp cần làm ngay>"
```

### Bước 3: Xuất báo cáo ngắn gọn cho User
Thông báo cho User:
1. Đường dẫn tệp checkpoint vừa tạo trong `.memory/checkpoints/`.
2. Khuyến nghị User:
   - Nếu context đã đầy: Gõ `/compact` hoặc mở phiên chat mới.
   - Ở phiên mới, chỉ cần gõ: `python3 scripts/memory-vault.py latest` để nạp ngay bối cảnh sạch!
