# TC IT AGENT FRAMEWORK — TÀI LIỆU YÊU CẦU SẢN PHẨM & KẾ HOẠCH TỔNG THỂ (PRD)

> **Phiên bản**: `v2.0.0-Enterprise`  
> **Trạng thái**: Đã phê duyệt kế hoạch (Approved Plan)  
> **Tác giả**: TC IT Architecture Board  
> **Phạm vi**: Khung vận hành Đa Tác Tử (Multi-Agent) phát triển phần mềm doanh nghiệp khép kín, độc lập nền tảng và mô hình LLM.

---

## 1. MỤC TIÊU VÀ TẦM NHÌN CHIẾN LƯỢC

1. **Độc lập nền tảng (Universal Platform & LLM Agnostic)**: Hoạt động trơn tru trên mọi nền tảng AI Agentic (Google Antigravity, Cursor, Windsurf, Claude Code, OpenAI Codex, DeepSeek CLI, Aider, Cline) và mọi mô hình LLM (Claude 3.5/3.7, GPT-4o/o1/o3, Gemini 2.0/3.0, DeepSeek V3/R1).
2. **Bộ máy 6 Tác tử Doanh nghiệp (6 Core Roles)**: Bao phủ trọn vẹn từ Tiền dự án (Presale, Solution, Báo giá) đến Thực thi phát triển (PO/PM, BA, TL/SA, Dev, EC/QC).
3. **Bộ Kỹ năng chuẩn hóa (Role-Prefix Skill Matrix)**: Định danh theo tiền tố role ngắn gọn: `ps-`, `po-`, `ba-`, `sa-`, `dev-`, `ec-`.
4. **Cơ chế Chống Rác & Quản lý Tệp Tin Nghiêm Ngặt (Zero-Tolerance File Dumping)**: Mọi tệp tin sinh ra hoặc cập nhật đều có địa chỉ cố định, tự động định tuyến đúng thư mục chức năng, không để rác ở root hay xáo trộn vị trí.
5. **Quy trình Chống Trôi Dạt Tri Thức (Two-Way Anti-Drift Workflows)**: Đảm bảo "Tài liệu đi trước, Code theo sau". Khi có thay đổi (Change Request), tài liệu kiến trúc (Basic/Detail Design) bắt buộc phải được đồng bộ trước khi viết code.

---

## 2. BỘ MÁY 6 TÁC TỬ DOANH NGHIỆP (6 CORE AGENT ROLES)

```
┌────────────────────────────────────────────────────────────────────────┐
│               GIAI ĐOẠN 0: TIỀN DỰ ÁN & GIẢI PHÁP (PRE-SALES)          │
│  [Khách hàng / Giám đốc] ──(RFP / Đề bài)──> [0. PS Agent (Presale)]  │
│                                                     │                  │
│                      ┌──────────────────────────────┴──────────────┐   │
│                      ▼                                             ▼   │
│             [IT Proposal / Báo giá]                    [Ký duyệt Hợp đồng]
└─────────────────────────────────────────────────────────────┬──────────┘
                                                              │ Handover
┌─────────────────────────────────────────────────────────────▼──────────┐
│              GIAI ĐOẠN 1 - 5: THỰC THI DỰ ÁN (5 STAGE-GATES)           │
│                                                                        │
│   [1. PO/PM Agent] ──(Scope & Brief)──> [2. BA Agent]                  │
│          ▲                                   │                         │
│          │ (Gate 5: DoD Nghiệm thu)          │ (Basic Design & SRS)    │
│          │                                   ▼                         │
│   [5. EC Agent] <──(Code & Unit Test)── [3. TL/SA Agent]               │
│          ▲                                   │                         │
│          │ (Gate 4: Test 3 Tầng)             │ (Detail Design & Tasks) │
│          │                                   ▼                         │
│          └──────── (Mã nguồn) ───────── [4. Dev Agent]                 │
└────────────────────────────────────────────────────────────────────────┘
```

### Chi tiết phân vai:
1. **`ps` — Presale & IT Solution Consultant**:
   - Am hiểu giải pháp kỹ thuật chuyên sâu (Cloud, Microservices, Monolith, Security, AI, Scalability).
   - Tư duy tài chính & kinh doanh: Bóc tách khối lượng (WBS), tính toán Man-Month (MM), dự toán chi phí hạ tầng Cloud (AWS/Azure/GCP/On-Prem), TCO, ROI.
   - Soạn thảo IT Proposal & bài thuyết trình kỹ thuật cho Giám đốc/Khách hàng.
2. **`po-pm` — Product Owner & Project Manager**:
   - Quản trị phạm vi (Scope Triage), phân rã Milestone, Master Roadmap, gác cổng Gate 1 (đề bài) và Gate 5 (nghiệm thu).
3. **`ba` — Senior Business Analyst**:
   - Khơi gợi nghiệp vụ 9 chiều (5 Whys, Laddering...), lập Thiết kế Cơ sở (Basic Design - Kihon Sekkei), đặc tả SRS 7 mục, kiểm soát ma trận truy vết `REQ-` ↔ `BR-`.
4. **`techlead-sa` — Software Architect & Tech Lead**:
   - Thiết kế kỹ thuật chi tiết (Detail Design - Shousai Sekkei): C4 diagrams, ERD CSDL (`DB-`), hợp đồng API (`API-`), bảo vệ ranh giới Clean Architecture, Adversarial Review mã nguồn (Gate 2 & 3).
5. **`dev` — Senior Full-Stack Developer**:
   - Thực thi mã nguồn chuẩn xác 1:1 theo `tasks.md`, viết Unit Test cho mọi Business Rule (`BR-*`), chuẩn hóa 5 trạng thái UX (`<Async>`).
6. **`ec` — Edge-Case Hunter & Quality Control Specialist**:
   - Săn tìm kịch bản biên (Edge cases, boundary conditions), fuzzing bảo mật & RBAC, tự động sinh Playwright E2E từ Acceptance Criteria, điều phối kiểm thử 3 tầng khép kín (Gate 4).

---

## 3. DANH MỤC SKILL THEO ROLE (ROLE-PREFIX SKILL MATRIX)

| Tiền tố | Thư mục Skill | Tên Skill | Chức năng thực thi |
| :--- | :--- | :--- | :--- |
| **`ps-`** | `skills/ps-*/` | `ps-proposal` | Soạn thảo hồ sơ giải pháp kỹ thuật (IT Technical Proposal) |
| | | `ps-estimate` | Bóc tách khối lượng, tính toán Man-Month & dự toán chi phí/TCO |
| | | `ps-solution` | So sánh phương án kiến trúc & phân tích trade-off cho Giám đốc |
| | | `ps-rfp` | Thẩm định hồ sơ thầu (RFP/RFI) & tính khả thi kỹ thuật |
| **`po-`** | `skills/po-*/` | `po-scope` | Sàng lọc yêu cầu, ma trận ảnh hưởng chéo & MVP roadmap |
| | | `po-roadmap` | Quản trị Master Roadmap, Milestones & Epics |
| | | `po-gate` | Tiêu chí nghiệm thu DoD & biên bản xuất xưởng (Gate 5) |
| | | `po-party` | Triệu tập bàn tròn tranh luận đa tác tử (Party Mode) |
| | | `po-course` | Nắn dòng & chống trôi dạt nghiệp vụ (Course Correction Specialist) |
| | | `po-issues` | Đồng bộ hóa danh mục Task thành GitHub/GitLab Issues |
| **`ba-`** | `skills/ba-*/` | `ba-elicit` | 9 kỹ thuật khơi gợi nghiệp vụ chuyên sâu (5 Whys, Laddering...) |
| | | `ba-design` | Soạn thảo Thiết kế Cơ sở (Basic Design - Kihon Sekkei) |
| | | `ba-srs` | Soạn thảo Đặc tả yêu cầu phần mềm chuẩn 7 mục khép kín (REQ-, BR-) |
| | | `ba-trace` | Kiểm toán ma trận truy vết khép kín REQ ↔ BR ↔ DB ↔ Test |
| | | `ba-clarify` | Rà soát và làm rõ các vùng yêu cầu chưa rõ ràng (Clarification) |
| | | `ba-docx` | Đóng gói và xuất bản hồ sơ tài liệu Word/PDF chuyên nghiệp |
| **`sa-`** | `skills/sa-*/` | `sa-design` | Thiết kế kỹ thuật chi tiết (Detail Design: ERD, API, Sequence) |
| | | `sa-plan` | Lập kế hoạch kiến trúc & phân rã module |
| | | `sa-guard` | Vệ binh giám sát ranh giới Clean Architecture |
| | | `sa-refactor` | Quét dự án cũ (Chỉ đọc) & Đề xuất giải pháp Refactor an toàn |
| | | `sa-review` | Rà soát code đối kháng trước khi bàn giao sang kiểm thử |
| | | `sa-analyze` | Phân tích tính nhất quán chéo giữa Spec - Plan - Tasks |
| **`dev-`** | `skills/dev-*/` | `dev-tasks` | Phân rã checklist công việc kỹ thuật [BE]/[FE] |
| | | `dev-code` | Lập trình thực thi tuần tự bám sát task có kiểm chứng |
| | | `dev-uiux` | Chuẩn hóa giao diện 5 trạng thái UX (`<Async>`) |
| | | `dev-unit` | Viết mã kiểm thử Unit Test cho Business Rules (TDD) |
| | | `dev-converge` | Đối soát mã nguồn thực tế với spec để đảm bảo hội tụ 100% |
| **`ec-`** | `skills/ec-*/` | `ec-hunt` | Săn kịch bản ngoại lệ, lỗi góc khuất & điều kiện biên |
| | | `ec-e2e` | Tự động sinh Playwright E2E từ Acceptance Criteria |
| | | `ec-fuzz` | Fuzzing bảo mật, chống leo thang đặc quyền & kiểm tra RBAC |
| | | `ec-test` | Điều phối thực thi bộ kiểm thử 3 tầng (Quality Gate 4) |
| **`wf-`** | `workflows/` & `skills/wf-*/` | `wf-presale` | Quy trình tiền dự án: Đề bài -> Proposal & Báo giá |
| | | `wf-kickoff` | Khởi động dự án: Basic Design & Master Roadmap |
| | | `wf-refactor` | Quét phân tích chỉ đọc dự án cũ & đề xuất lộ trình Refactor |
| | | `wf-autopilot` | Tự động hóa toàn trình phát triển Epic (7 chặng) |
| | | `wf-hotfix` | Vá lỗi khẩn cấp Production/UAT theo chuẩn phẫu thuật tối thiểu |
| | | `wf-delta` | Thay đổi yêu cầu chuẩn Spec-First, chống trôi dạt tri thức |
| | | `wf-uiux` | Chuẩn hóa giao diện 5 trạng thái UX & Playwright Visual QA |
| | | `wf-audit` | Kiểm toán toàn diện: Kiến trúc, Truy vết, Rác & Coverage |

---

## 4. KHUNG QUẢN LÝ THƯ MỤC & CƠ CHẾ ĐỊNH TUYẾN CHỐNG RÁC (DIRECTORY ROUTING & ANTI-CLUTTER POLICY)

### 4.1. Cấu trúc thư mục chuẩn mực

```text
{{PROJECT_ROOT}}/
├── .agents/                         # Cấu hình 6 Persona (ps, po-pm, ba, techlead-sa, dev, ec)
├── AGENTS.md                        # Bộ luật điều phối chung (Universal Agent Rulebook)
├── constitution.md                  # Hiến pháp kỹ thuật & Ranh giới chất lượng bất biến
│
├── docs/                            # TOÀN BỘ TÀI LIỆU DỰ ÁN (Có địa chỉ cố định)
│   ├── 00-presale-proposal/         # [PS] Hồ sơ giải pháp & Báo giá
│   │   ├── PROPOSAL.md              # IT Technical Proposal
│   │   ├── ESTIMATION_AND_COST.md   # Dự toán Man-Month, chi phí Cloud, hạ tầng
│   │   ├── SOLUTION_COMPARISON.md   # Phân tích phương án so sánh
│   │   └── EXECUTIVE_SUMMARY.md     # Bản tóm lược cho C-Level / Khách hàng
│   ├── 01-basic-design/             # [BA] Thiết kế Cơ sở (Kihon Sekkei)
│   │   ├── BD-00-overview.md        # Tầm nhìn, Walking Skeleton, Story Mapping
│   │   ├── BD-01-c4-context.md      # Sơ đồ C4 Context & C4 Container
│   │   └── BD-02-domain-model.md    # Domain Entities, Bounded Contexts
│   ├── 02-detail-design/            # [SA] Thiết kế Chi tiết (Shousai Sekkei)
│   │   ├── DD-01-database-erd.md    # Schema CSDL, Từ điển dữ liệu (DB-*)
│   │   ├── DD-02-api-contracts.md   # OpenAPI, REST/gRPC contracts (API-*)
│   │   ├── DD-03-sequence-flows.md  # Sequence diagrams luồng phức tạp
│   │   └── DD-04-state-machines.md  # Máy trạng thái thực thể
│   ├── decisions/                   # [SA] Architecture Decision Records (ADR-001...)
│   └── change-requests/             # [PO/BA] Yêu cầu thay đổi (CR-001...)
│
├── backlog/                         # [PO] QUẢN LÝ TIẾN ĐỘ & YÊU CẦU CẤP CAO
│   ├── ROADMAP.md                   # Master Roadmap & Tiến độ Milestone
│   ├── EPICS/                       # Phân rã danh sách Epic lớn
│   └── USER_STORIES/                # Danh sách User Story
│
├── specs/                           # [BA/SA/DEV] ĐẶC TẢ SPEC KIT CHO TỪNG EPIC
│   └── [epic-id]/                   # Ví dụ: specs/EPIC-01-AUTH/
│       ├── spec.md                  # Đặc tả chi tiết 7 mục (REQ-, BR-)
│       ├── plan.md                  # Kế hoạch kỹ thuật & kiến trúc phân tầng
│       ├── tasks.md                 # Phân rã công việc thực thi [x]
│       └── checklist.md             # Tiêu chí nghiệm thu DoD
│
├── src/                             # [DEV] MÃ NGUỒN CHUẨN CLEAN ARCHITECTURE
│   ├── Domain/                      # Thực thể lõi, Domain Events (Không phụ thuộc tầng ngoài)
│   ├── Application/                 # Use Cases, DTOs, Validators, Interfaces
│   ├── Infrastructure/              # DB Context, Repositories, Third-party SDKs
│   ├── Presentation/ (hoặc API/)    # Controllers, Route Handlers, Middlewares
│   └── WebApp/ (hoặc Client/)       # UI Frontend React/Vue chuẩn 5 trạng thái UX
│
└── tests/                           # [DEV/EC] HỆ THỐNG KIỂM THỬ 3 TẦNG
    ├── unit/                        # Unit test nghiệp vụ (100% BR-*)
    ├── integration/                 # Integration test CSDL & API
    └── e2e/                         # Playwright E2E test hành trình người dùng
```

---

### 4.2. Cơ Chế Tự Động Định Tuyến & Ngăn Ngừa Tệp Tin Rác (Anti-Clutter Engine)

Để ngăn chặn tuyệt đối tình trạng agent sinh file bừa bãi ra thư mục gốc (`root`) hoặc để lẫn lộn các file:

#### 1. Nguyên Tắc Zero-Tolerance Root Dumping (Luật Thư Mục Gốc)
Tại thư mục gốc (`root`), **CHỈ ĐƯỢC PHÉP** tồn tại các tệp tin cấu hình dự án chuẩn:
- `README.md`, `install.sh`, `.gitignore`
- `AGENTS.md`, `constitution.md`
- Tệp cấu hình IDE (`.cursorrules`, `.windsurfrules`, `CLAUDE.md`)
- Tệp cấu hình build hệ thống (`package.json`, `pom.xml`, `.sln`...)
- **CẤM TUYỆT ĐỐI**: Không cho phép bất kỳ Agent nào tạo file `.md`, file nháp, script tạm, log hoặc test ở thư mục root!

#### 2. Bản Hợp Đồng Đầu Ra Bắt Buộc Của Từng Skill (Skill I/O Artifact Contract)
Mỗi kỹ năng (`SKILL.md`) đều có định nghĩa **Đường dẫn tệp đích bắt buộc (Enforced Output Path)**. Tác tử khi dùng tool `write_to_file` chỉ được phép ghi vào đúng vị trí này:
- `ps-proposal` ➔ Bắt buộc ghi vào: `docs/00-presale-proposal/PROPOSAL.md`
- `ps-estimate` ➔ Bắt buộc ghi vào: `docs/00-presale-proposal/ESTIMATION_AND_COST.md`
- `ba-design` ➔ Bắt buộc ghi vào: `docs/01-basic-design/BD-*.md`
- `sa-design` ➔ Bắt buộc ghi vào: `docs/02-detail-design/DD-*.md`
- `sa-plan` ➔ Bắt buộc ghi vào: `specs/[epic-id]/plan.md`
- `dev-tasks` ➔ Bắt buộc ghi vào: `specs/[epic-id]/tasks.md`
- `dev-code` ➔ Bắt buộc ghi vào: `src/[Domain|Application|Infrastructure|Presentation|WebApp]/`
- `ec-e2e` ➔ Bắt buộc ghi vào: `tests/e2e/[epic-id].spec.ts`

#### 3. Chốt Chặn Kiểm Tra Tự Động (Automated File Organizer & Lint Guard)
- Tích hợp kiểm tra cấu trúc cây thư mục vào skill `sa-guard` và script kiểm thử Gate:
- Nếu phát hiện file lạ nằm sai vị trí (ví dụ: `test.js` nằm ở `src/`, `draft.md` nằm ở `root`), hệ thống tự động:
  1. Cảnh báo lỗi vi phạm cấu trúc (Structure Lint Violation).
  2. Tự động di chuyển file về đúng thư mục quy định (`docs/`, `tests/`, `specs/`).
  3. Chặn không cho phép vượt qua Quality Gate nếu chưa dọn sạch.

---

## 5. QUY TRÌNH CHỐNG TRÔI DẠT TRI THỨC (SPEC-FIRST ANTI-DRIFT)

### Cơ chế 2 chiều (Two-Way Synchronization)
```
            ┌──────────────────────────────────────────┐
            │   TIẾP NHẬN YÊU CẦU THAY ĐỔI (CR)       │
            └────────────────────┬─────────────────────┘
                                 │
                                 ▼
            ┌──────────────────────────────────────────┐
            │  BƯỚC 1: PHÂN TÍCH TÁC ĐỘNG (SA + BA)    │
            │  Quét ảnh hưởng tới Basic & Detail Design│
            └────────────────────┬─────────────────────┘
                                 │
                                 ▼
            ┌──────────────────────────────────────────┐
            │  BƯỚC 2: CẬP NHẬT TÀI LIỆU THIẾT KẾ      │
            │  docs/01-basic-design/ & 02-detail-design│  <─── ĐIỀU KIỆN TIÊN QUYẾT
            └────────────────────┬─────────────────────┘       (BẮT BUỘC TRƯỚC KHI CODE)
                                 │
                                 ▼
            ┌──────────────────────────────────────────┐
            │  BƯỚC 3: CẬP NHẬT SPEC & SINH TASK DELTA │
            │  specs/[epic]/spec.md & tasks.md [DELTA] │
            └────────────────────┬─────────────────────┘
                                 │
                                 ▼
            ┌──────────────────────────────────────────┐
            │  BƯỚC 4: THỰC THI MÃ NGUỒN & REGRESSION  │
            │  Dev sửa code -> EC chạy test hồi quy   │
            └────────────────────┬─────────────────────┘
                                 │
                                 ▼
            ┌──────────────────────────────────────────┐
            │  BƯỚC 5: ĐỒNG BỘ TRUY VẾT & ĐÓNG CR      │
            │  traceability-auditor PASS -> Merged     │
            └──────────────────────────────────────────┘
```

1. **Nguyên tắc "Tài liệu đi trước, Code theo sau"**: Tuyệt đối không cho phép Dev nhảy vào sửa code khi chưa cập nhật tài liệu thiết kế.
2. **Ký hiệu Delta rõ ràng**: Mọi task phát sinh do thay đổi đều được gắn mã `[DELTA-xx]` trong `tasks.md` để đối soát dễ dàng.
3. **Traceability Auditor**: Kiểm tra ma trận truy vết khép kín: nếu có code mới mà không có `REQ-` hay `BR-` trong `spec.md`, mã nguồn đó sẽ bị đánh dấu là "Mã mồ côi" (Orphan Code) và bị từ chối merge.

---

## 6. LỘ TRÌNH THỰC THI (ACTION ITEMS)

1. **Giai đoạn 1: Chuẩn hóa 6 Persona**:
   - Tạo mới `.agents/ps.md` (Presale & IT Solution Consultant).
   - Nâng cấp `.agents/ec.md` (Edge-Case Hunter & QC).
   - Chuẩn hóa và decoupling hoàn toàn các persona: `po-pm.md`, `ba.md`, `techlead-sa.md`, `dev.md`.
2. **Giai đoạn 2: Sắp xếp lại Skills & Đặt tên tiền tố chuẩn**:
   - Tạo các thư mục `skills/00-presale/`, `01-po-pm/`, `02-ba/`, `03-sa-tl/`, `04-dev/`, `05-ec/`.
   - Đổi tên toàn bộ skills theo tiền tố ngắn gọn (`ps-*`, `po-*`, `ba-*`, `sa-*`, `dev-*`, `ec-*`).
   - Cập nhật hợp đồng đường dẫn file đích (Enforced Output Path) vào từng `SKILL.md`.
3. **Giai đoạn 3: Xây dựng Bộ Templates Chuẩn & Khung Thư Mục Mẫu**:
   - Thêm `TEMPLATE-it-proposal.md`, `TEMPLATE-cost-estimation.md`.
   - Thêm `TEMPLATE-detail-design-erd.md`, `TEMPLATE-detail-design-api.md`.
   - Xây dựng thư mục mẫu `template-workspace/` hoàn chỉnh cho dự án mới.
4. **Giai đoạn 4: Bộ Adapter Đa Nền Tảng (Multi-Platform Adapters)**:
   - Tạo bộ sinh cấu hình cho: Cursor (`.cursorrules`), Windsurf (`.windsurfrules`), Claude Code (`CLAUDE.md`), Codex/DeepSeek (`AGENTS.md`).
   - Nâng cấp `install.sh` hỗ trợ tham số `--antigravity`, `--cursor`, `--windsurf`, `--claude`, `--all`.
5. **Giai đoạn 5: Hoàn thiện Báo cáo, Kiểm tra & Đóng gói**:
   - Kiểm thử toàn diện quy trình chạy thử nghiệm.
   - Cập nhật lại tài liệu [README.md](file:///Users/luongdt/Documents/TC%20IT%20Agent/README.md).
