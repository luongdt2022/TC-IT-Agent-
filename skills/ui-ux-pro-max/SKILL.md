---
name: "ui-ux-pro-max"
description: "Bộ máy suy luận & tra cứu hệ thống thiết kế UI/UX chuyên sâu (Design Intelligence Engine): 80 style UI, 192 bảng màu & quy tắc ngành, 74 cặp font, 119 hướng dẫn UX (WCAG AA/AAA), 22 tech stack guidelines (Do/Don't & Code mẫu), và sinh Master Design System tokens tự động."
---

# UI/UX Pro Max — Design Intelligence Engine

Bộ máy suy luận thiết kế và kho tri thức UI/UX cục bộ (Zero-dependency, offline, BM25 ranking): **80 phong cách UI** (51 active), **192 quy tắc ngành & bảng màu**, **74 cặp typography**, **119 hướng dẫn UX**, **105 biểu tượng SVG**, **25 dạng biểu đồ**, và **22 công nghệ lập trình frontend/mobile**.

---

## 1. Khi Nào Cần Kích Hoạt Kỹ Năng Này?

Kích hoạt kỹ năng này khi tác vụ liên quan đến:
1. **Khởi tạo hệ thống thiết kế mới (Design System)**: Sinh bảng màu, font chữ, CSS variables, bố cục giao diện cho dự án hoặc màn hình mới.
2. **Quy chuẩn lập trình theo Framework**: Tra cứu thực hành chuẩn (`Do / Don't`, `Code Good / Code Bad`) cho 22 Tech Stacks (React 19, Next.js 15, Tailwind, Vue, Nuxt, Svelte, Angular, Flutter, SwiftUI, Jetpack Compose...).
3. **Kiểm soát chất lượng UX & A11y (Pre-Delivery Checklist)**: Rà soát độ tương phản (Contrast >= 4.5:1), vùng bấm (Touch Target >= 44×44px), trạng thái focus phím, tôn trọng `prefers-reduced-motion`, và loại bỏ triệt để Emoji làm icon cấu trúc.
4. **Giải quyết vấn đề giao diện vi mô**: Xử lý rớt dòng tiêu đề (`text-wrap: balance`), chip/badge tràn viền, modal accessibility, tối ưu hóa re-render.

*Bỏ qua kỹ năng này đối với các tác vụ thuần backend, database schema, DevOps CI/CD trừ khi tác vụ ảnh hưởng trực tiếp đến trải nghiệm nhìn, chạm, hoặc tương tác của người dùng.*

---

## 2. Đường Dẫn Thực Thi Công Cụ Cục Bộ (CLI Search Engine)

Script tìm kiếm nằm trực tiếp trong thư mục kỹ năng, chạy hoàn toàn bằng Python 3 standard library (không cần cài đặt thư viện bên ngoài):

```bash
# Cú pháp chạy chung từ thư mục gốc dự án:
python3 skills/ui-ux-pro-max/scripts/search.py "<truy_vấn>" [tùy_chọn]
```

---

## 3. Quy Trình Sử Dụng Chuẩn 4 Bước

### Bước 1: Phân Tích Đề Bài & Ngữ Cảnh Dự Án
Xác định:
- **Loại sản phẩm (Product Type)**: Fintech/Ngân hàng, Y tế/Bệnh viện, SaaS B2B, E-commerce, EdTech, GovTech, Mạng xã hội, Dashboard phân tích...
- **Đối tượng & Ngữ cảnh**: Người dùng văn phòng, thiết bị di động, người cao tuổi, màn hình bảng điều khiển...
- **Tech Stack**: Phát hiện từ `package.json`, `pubspec.yaml`, `composer.json`... (Không bao giờ đoán mò hoặc gán mặc định sai framework).

### Bước 2: Sinh & Lưu Vết Hệ Thống Thiết Kế (Master + Overrides Pattern)
Khi bắt đầu một dự án mới hoặc một Epic lớn, chạy lệnh sinh Design System kèm cờ `--persist` để tạo Single Source of Truth:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<tên_ngành_hoặc_loại_sản_phẩm>" --design-system --persist -p "<TênDựÁn>" --output-dir "."
```

Lệnh trên tự động tạo cây thư mục:
```
design-system/
└── <project-slug>/
    ├── MASTER.md            # Chân lý thiết kế duy nhất (Màu sắc, Typography, Spacing tokens, Anti-patterns)
    └── pages/               # Thư mục chứa các ghi đè đặc thù cho từng trang (nếu có)
```

Nếu cần ghi đè riêng cho một màn hình (ví dụ `dashboard` hoặc `checkout`):
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<truy_vấn>" --design-system --persist -p "<TênDựÁn>" --output-dir "." --page "dashboard"
```

> **Nguyên tắc truy xuất khi lập trình:**
> 1. Đọc `design-system/<project-slug>/MASTER.md`.
> 2. Kiểm tra xem `design-system/<project-slug>/pages/<page-name>.md` có tồn tại không. Nếu có, áp dụng các quy tắc ghi đè trong đó.
> 3. Tuyệt đối không dùng cờ `--force` khi chưa có sự đồng ý của User để tránh làm mất các quyết định thiết kế đã chốt trước đó.

### Bước 3: Tra Cứu Quy Chuẩn Theo Stack & Miền Chuyên Biệt
Khi bắt tay vào code các component, tra cứu chính xác hướng dẫn của framework:

```bash
# Tra cứu theo Stack kỹ thuật
python3 skills/ui-ux-pro-max/scripts/search.py "form validation" --stack react
python3 skills/ui-ux-pro-max/scripts/search.py "responsive layout" --stack html-tailwind
python3 skills/ui-ux-pro-max/scripts/search.py "state management" --stack flutter

# Tra cứu theo Miền chuyên sâu (--domain)
python3 skills/ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style
python3 skills/ui-ux-pro-max/scripts/search.py "accessible button label" --domain icons
python3 skills/ui-ux-pro-max/scripts/search.py "realtime metric" --domain chart
python3 skills/ui-ux-pro-max/scripts/search.py "error summary keyboard" --domain ux
```

| Nhu cầu tra cứu | Miền (`--domain`) | Ví dụ |
| :--- | :---: | :--- |
| Phong cách giao diện | `style` | `"minimalist clean" --domain style` |
| Bảng màu theo ngành | `color` | `"fintech security" --domain color` |
| Cặp font chữ tối ưu | `typography` | `"modern sans" --domain typography` |
| Phông chữ Google Fonts | `google-fonts` | `"sans serif variable" --domain google-fonts` |
| Khuyến nghị Biểu đồ | `chart` | `"financial trend candlestick" --domain chart` |
| Thực hành UX & WCAG | `ux` | `"keyboard focus modal trap" --domain ux` |
| Biểu tượng SVG chuẩn | `icons` | `"navigation menu lucide" --domain icons` |
| Hoạt ảnh chuyển động GSAP| `gsap` | `"fade in stagger list" --domain gsap` |

### Bước 4: Kiểm Soát Chất Lượng Trước Khi Bàn Giao (Pre-Delivery Checklist)
Trước khi bàn giao code cho QC hoặc đóng Task, bắt buộc đối soát theo checklist:

- [ ] **Icon cấu trúc**: 100% là vector SVG (Lucide, Heroicons), **tuyệt đối không dùng Emoji** (🎨, 🚀, ⚙️) làm biểu tượng nút bấm hay điều hướng.
- [ ] **Con trỏ & Tương tác**: `cursor-pointer` trên mọi phần tử click được; hiệu ứng hover chuyển tiếp mượt mà (150-250ms).
- [ ] **Độ tương phản (Contrast)**: Văn bản chính đạt tối thiểu 4.5:1 so với nền (chế độ sáng lẫn chế độ tối).
- [ ] **Vùng bấm (Touch Targets)**: Đạt tối thiểu 44×44px trên iOS / Web di động và 48×48dp trên Android.
- [ ] **Focus bàn phím**: Đường viền focus (focus-ring) hiển thị rõ ràng khi bấm Tab điều hướng.
- [ ] **Khả năng giảm chuyển động**: Tuân thủ `@media (prefers-reduced-motion: reduce)`.
- [ ] **Không tràn chữ**: Tiêu đề và badge tự co giãn hoặc xuống dòng tự nhiên, không bị cắt cụt hay vỡ khung.
- [ ] **Thiết kế thích ứng (Responsive)**: Hoạt động chuẩn xác trên các kích thước: Mobile (375px), Tablet (768px), Desktop (1024px, 1440px).

---

## 4. Tài Liệu Tham Khảo Nâng Cao (Quick Reference)

Để tra cứu chi tiết hơn:
- Xem [`references/quick-reference.md`](file:///Users/luongdt/Documents/TC%20IT%20Agent/skills/ui-ux-pro-max/references/quick-reference.md): Toàn bộ 119 quy tắc UX chia theo 10 mức ưu tiên từ Khả năng tiếp cận, Vùng chạm, Hiệu năng đến Biểu đồ.
- Xem [`references/pro-rules.md`](file:///Users/luongdt/Documents/TC%20IT%20Agent/skills/ui-ux-pro-max/references/pro-rules.md): Bộ tiêu chuẩn chi tiết dành riêng cho Mobile App UI (Safe areas, Gesture conflicts, Native primitives).
