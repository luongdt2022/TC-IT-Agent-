---
name: bmad-advanced-elicitation
description: "Bộ Kỹ thuật Khơi gợi Nghiệp vụ Chuyên sâu 9 Chiều (Advanced Elicitation Suite). Ứng dụng các kỹ thuật: 5 Whys, Laddering, Strawman Proposal, Devil's Advocate, Socratic Questioning, Boundary Probing để bóc tách nhu cầu tiềm ẩn của khách hàng."
metadata:
  short-description: Khơi gợi nghiệp vụ 9 chiều nâng cao chuẩn BMad
---

# Advanced Requirements Elicitation Suite (`bmad-advanced-elicitation`)

Skill chuyên trách dành cho **Agent BA** để phỏng vấn và khai thác nghiệp vụ ở mức độ chuyên gia cao cấp, vượt xa việc hỏi đáp biểu mẫu thông thường.

## 1. 9 KỸ THUẬT KHƠI GỢI NGHIỆP VỤ ĐỈNH CAO (9 ELICITATION PATTERNS)

1. **5 Whys (Truy Vết Động Cơ Gốc)**:
   - Khi người dùng đưa ra một giải pháp (ví dụ: *"Tôi muốn có nút xuất Excel"*), hỏi sâu từ 3-5 lần chữ "Tại sao" để tìm ra mục đích thật (ví dụ: *"Để gửi báo cáo định kỳ cho lãnh đạo tỉnh"*) $\rightarrow$ Đề xuất giải pháp tối ưu hơn (Tự động gửi email lịch định kỳ).
2. **Laddering (Thang Đo Trừu Tượng)**:
   - Leo thang lên (Upward): *"Tính năng này phục vụ mục tiêu kinh doanh nào của NacenTech?"*
   - Leo thang xuống (Downward): *"Cụ thể màn hình đó cần hiển thị những cột số liệu nào?"*
3. **Strawman Proposal (Đề Xuất Bù Nhìn)**:
   - Khi khách hàng mơ hồ, BA chủ động dựng một kịch bản giả lập có chủ đích (kèm cả điểm bất hợp lý nhẹ) để kích thích người dùng phản biện và chỉ ra mong muốn thực sự.
4. **Devil's Advocate (Luật Sư Của Quỷ)**:
   - Chủ động đóng vai người phản đối: *"Nếu chuyên gia cố tình upload CV giả mạo bằng cấp thì hệ thống xử lý ra sao?"*
5. **Boundary Probing (Thử Thách Vùng Biên)**:
   - Thử thách các giá trị cực hạn: *"Nếu doanh nghiệp có 10,000 công nghệ, hoặc giá chuyển giao là 0 đồng thì luồng chạy thế nào?"*
6. **Socratic Questioning (Vấn Đáp Socrates)**:
   - Dẫn dắt người dùng tự nhận ra mâu thuẫn trong chính phát biểu của họ bằng các câu hỏi logic.
7. **Exception Inversion (Đảo Ngược Ngoại Lệ)**:
   - Bắt đầu từ trường hợp thất bại: *"Khi nào thì giao dịch kết nối cung cầu này bị coi là thất bại hoàn toàn?"*
8. **Role Swapping (Hoán Đổi Vai Trò)**:
   - Đặt câu hỏi theo góc nhìn đối lập: *"Nếu bạn là Doanh nghiệp tìm mua công nghệ, bạn có muốn thông tin doanh thu của mình hiển thị công khai cho Seller không?"*
9. **Constraint Pressure (Gia Tăng Áp Lực Ràng Buộc)**:
   - *"Nếu chỉ có 3 giây để học viên quyết định mua khóa học này trên di động, thông tin nào bắt buộc phải thấy ngay?"*

## 2. QUY TRÌNH THỰC THI TRONG PHIÊN BA COPILOT
- BA không áp dụng máy móc cả 9 kỹ thuật cùng lúc.
- Lựa chọn linh hoạt 1-2 kỹ thuật phù hợp nhất với từng bối cảnh của 7 mục SRS để đạt được sự hội tụ (Convergence) nhanh nhất mà không gây mệt mỏi cho người dùng.
