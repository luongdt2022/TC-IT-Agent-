---
name: ba-design
description: "Soạn thảo tài liệu Thiết kế Cơ sở (Basic Design - Kihon Sekkei) đóng vai trò khung xương sống định hướng kiến trúc: Story Mapping, Walking Skeleton, C4 Context & Container, và Domain Model tổng thể."
---

# Kỹ Năng: ba-design (Soạn Thảo Thiết Kế Cơ Sở - Kihon Sekkei)

> **Role Chịu Trách Nhiệm**: BA Agent (`ba`) — Senior Business Analyst.  
> **Cổng Kiểm Soát**: Gate 1 Backbone Architecture Gate.

---

## 1. ENFORCED ARTIFACT CONTRACT (QUY ĐỊNH GHI FILE BẮT BUỘC)
- **Input**: Báo cáo khơi gợi `docs/01-basic-design/ELICITATION_LOG.md` hoặc đề bài từ `docs/00-presale-proposal/PROPOSAL.md`.
- **Target Output Directory**: `docs/01-basic-design/`
  - `docs/01-basic-design/BD-00-overview.md` (Tầm nhìn, Story Mapping, Walking Skeleton)
  - `docs/01-basic-design/BD-01-c4-context.md` (Sơ đồ C4 Context & C4 Container)
  - `docs/01-basic-design/BD-02-domain-model.md` (Mô hình Domain Entities & Bounded Contexts)
- **NGHIÊM CẤM**: Không ghi file ra thư mục gốc (`root`).

---

## 2. NỘI DUNG 3 TRỤ CỘT CỦA THIẾT KẾ CƠ SỞ

### Trụ Cột 1: `BD-00-overview.md`
1. **Executive Summary & System Vision**: Tầm nhìn cốt lõi, mục tiêu chiến lược và các bên liên quan (Stakeholders).
2. **User Personas & User Journeys**: Danh sách vai trò người dùng và hành trình người dùng xuyên suốt.
3. **Story Mapping Backbone**: Xương sống các hoạt động người dùng từ trái sang phải.
4. **Walking Skeleton Definition**: Lát cắt mỏng nhất kết nối từ Frontend qua API, Domain và CSDL chạy thông suốt ngay từ Sprint 1.

### Trụ Cột 2: `BD-01-c4-context.md`
1. **C4 Level 1 - System Context Diagram**: Vẽ bằng Mermaid biểu diễn hệ thống trung tâm với các Actor và hệ thống bên ngoài (External Systems/APIs).
2. **C4 Level 2 - Container Diagram**: Biển diễn Web App, Mobile App, API Gateway, Backend Services, Cache, Message Broker, Database.

### Trụ Cột 3: `BD-02-domain-model.md`
1. **Domain Entities & Aggregates**: Các thực thể cốt lõi của doanh nghiệp và mối quan hệ (1-1, 1-N, N-N).
2. **Bounded Contexts Mapping**: Phân định ranh giới giữa các ngữ cảnh phân hệ (ví dụ: Identity, Catalog, Order, Billing, Notification).

---

## 3. TIÊU CHUẨN NGHIỆM THU GATE 1 CHO BASIC DESIGN
- Không bắt đầu bẻ nhỏ sang các file SRS chi tiết nếu bản Thiết kế Cơ sở chưa được PO/PM ký duyệt `[GATE 1 PASS]`.
