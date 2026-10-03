---
name: ba-elicit
description: "Bộ 9 Kỹ thuật Khơi gợi Nghiệp vụ Chuyên sâu (Advanced Elicitation Suite: 5 Whys, Laddering, Strawman Proposal, Devil's Advocate, Socratic Questioning, Boundary Probing) để bóc tách nhu cầu tiềm ẩn của khách hàng."
---

# Kỹ Năng: ba-elicit (Khơi Gợi Nghiệp Vụ Chuyên Sâu 9 Chiều)

> **Role Chịu Trách Nhiệm**: BA Agent (`ba`) — Senior Business Analyst.  
> **Cổng Kiểm Soát**: Gate 1 Elicitation & Discovery.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Đề bài thô hoặc ghi chú phỏng vấn người dùng/khách hàng.
- **Target Output File**: `docs/01-basic-design/ELICITATION_LOG.md`
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. 9 KỸ THUẬT KHƠI GỢI NGHIỆP VỤ ĐỈNH CAO (9 ELICITATION PATTERNS)

1. **5 Whys (Truy Vết Động Cơ Gốc)**:
   - Khi người dùng đưa ra một giải pháp (ví dụ: *"Tôi muốn có nút xuất Excel"*), hỏi sâu 3 - 5 lần "Tại sao" để tìm ra mục đích thật (ví dụ: *"Để gửi báo cáo định kỳ cho Giám đốc"*) $\rightarrow$ Đề xuất giải pháp tự động hóa thông minh hơn.
2. **Laddering (Thang Đo Trừu Tượng)**:
   - Leo thang lên (Upward): *"Tính năng này phục vụ mục tiêu kinh doanh/chiến lược nào?"*
   - Leo thang xuống (Downward): *"Cụ thể màn hình đó cần hiển thị những trường dữ liệu nào?"*
3. **Strawman Proposal (Đề Xuất Bù Nhìn)**:
   - Khi khách hàng mơ hồ, BA chủ động dựng một kịch bản giả lập có chủ đích (kèm cả điểm bất hợp lý nhẹ) để kích thích người dùng phản biện và chỉ ra mong muốn thực sự.
4. **Devil's Advocate (Luật Sư Của Quỷ)**:
   - Chủ động đóng vai người phản đối: *"Nếu người dùng cố tình gửi dữ liệu sai lệch hoặc gian lận thì hệ thống xử lý ra sao?"*
5. **Boundary Probing (Thử Thách Vùng Biên)**:
   - Thử thách các giá trị cực hạn: *"Nếu dữ liệu có 1,000,000 dòng, hoặc giá trị bằng 0, hoặc chuỗi dài 1,000 ký tự thì xử lý thế nào?"*
6. **Socratic Questioning (Vấn Đáp Socrates)**:
   - Dẫn dắt người dùng tự nhận ra mâu thuẫn trong phát biểu của họ bằng các câu hỏi logic tuần tự.
7. **Exception Inversion (Đảo Ngược Ngoại Lệ)**:
   - Bắt đầu từ trường hợp thất bại: *"Khi nào thì quy trình giao dịch này bị coi là thất bại hoàn toàn?"*
8. **Role Swapping (Hoán Đổi Vai Trò)**:
   - Đặt câu hỏi theo góc nhìn đối lập: *"Nếu bạn là đối tác bên ngoài, bạn có muốn thông tin này bị công khai không?"*
9. **Constraint Pressure (Gia Tăng Áp Lực Ràng Buộc)**:
   - *"Nếu người dùng chỉ có 3 giây trên điện thoại di động trong điều kiện mạng yếu, thông tin nào bắt buộc phải nhìn thấy trước tiên?"*

---

## 3. QUY TRÌNH THỰC THI
- Lựa chọn linh hoạt 1 - 2 kỹ thuật phù hợp với từng hoàn cảnh.
- Ghi nhận lại toàn bộ các phát hiện vào `docs/01-basic-design/ELICITATION_LOG.md` làm căn cứ biên soạn Thiết kế Cơ sở (`ba-design`).
