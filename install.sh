#!/usr/bin/env bash
# ==============================================================================
# TC IT AGENT FRAMEWORK — UNIVERSAL ENTERPRISE INSTALLER & UPDATER (v2.0)
# Cài đặt & Cập nhật bộ 6 Persona, Kỹ năng Role, Workflows & Cấu trúc Thư mục
# Hoạt động độc lập trên mọi nền tảng: Antigravity, Cursor, Windsurf, Claude, Codex
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "${BLUE}${BOLD}   TC IT AGENT FRAMEWORK V2.0 — BỘ MÁY ĐA TÁC TỬ DOANH NGHIỆP UNIVERSAL        ${NC}"
echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "Nguồn cài đặt: ${SCRIPT_DIR}\n"

usage() {
    echo -e "Cách sử dụng:"
    echo -e "  1. Cài đặt vào 1 dự án MỚI hoặc dự án ĐANG CHẠY:"
    echo -e "     ${BOLD}./install.sh /duong-dan/toi/du-an --name \"TenDuAn\" [tùy chọn nền tảng]${NC}"
    echo -e ""
    echo -e "  2. CẬP NHẬT (Update) cho một dự án đã tích hợp trước đó (Không làm mất code dự án):"
    echo -e "     ${BOLD}./install.sh /duong-dan/toi/du-an --update${NC}"
    echo -e ""
    echo -e "  Tùy chọn nền tảng hỗ trợ:"
    echo -e "     ${CYAN}--all${NC}          Cài đặt adapter cho TẤT CẢ các nền tảng (Cursor, Windsurf, Claude, Codex)"
    echo -e "     ${CYAN}--cursor${NC}       Cài đặt cấu hình cho Cursor IDE (.cursorrules & .cursor/rules/)"
    echo -e "     ${CYAN}--windsurf${NC}     Cài đặt cấu hình cho Windsurf IDE (.windsurfrules)"
    echo -e "     ${CYAN}--claude${NC}       Cài đặt cấu hình cho Claude Code CLI (CLAUDE.md)"
    echo -e "     ${CYAN}--antigravity${NC}  Cài đặt cho Google Antigravity (.agents/ & skills/)"
    echo -e "     ${CYAN}--generic${NC}      Cài đặt chuẩn Markdown cho Codex, DeepSeek, Aider, Cline (AGENTS.md)"
    echo -e ""
    echo -e "  3. Cài đặt kỹ năng toàn cục (Global cho Antigravity IDE trên máy):"
    echo -e "     ${BOLD}./install.sh --global${NC}\n"
    exit 1
}

TARGET_DIR=""
PROJECT_NAME=""
IS_GLOBAL=false
IS_UPDATE=false
OPT_ALL=true
OPT_CURSOR=false
OPT_WINDSURF=false
OPT_CLAUDE=false
OPT_ANTIGRAVITY=false
OPT_GENERIC=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --global)
            IS_GLOBAL=true
            shift
            ;;
        --update)
            IS_UPDATE=true
            shift
            ;;
        --name)
            PROJECT_NAME="$2"
            shift 2
            ;;
        --all)
            OPT_ALL=true
            shift
            ;;
        --cursor)
            OPT_ALL=false
            OPT_CURSOR=true
            shift
            ;;
        --windsurf)
            OPT_ALL=false
            OPT_WINDSURF=true
            shift
            ;;
        --claude)
            OPT_ALL=false
            OPT_CLAUDE=true
            shift
            ;;
        --antigravity)
            OPT_ALL=false
            OPT_ANTIGRAVITY=true
            shift
            ;;
        --generic)
            OPT_ALL=false
            OPT_GENERIC=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            fi
            shift
            ;;
    esac
done

# If global installation requested
if [[ "$IS_GLOBAL" == true ]]; then
    GLOBAL_SKILLS_DIR="${HOME}/.gemini/config/skills"
    echo -e "${YELLOW}>> Đang cài đặt/cập nhật bộ Kỹ năng vào thư viện toàn cục:${NC} ${GLOBAL_SKILLS_DIR}"
    mkdir -p "${GLOBAL_SKILLS_DIR}"
    cp -Rf "${SCRIPT_DIR}/skills/"* "${GLOBAL_SKILLS_DIR}/"
    echo -e "${GREEN}✓ Đã cập nhật thành công Skills toàn cục vào ${GLOBAL_SKILLS_DIR}!${NC}"
    exit 0
fi

# Interactive mode if target dir is empty
if [[ -z "$TARGET_DIR" ]]; then
    echo -e "${YELLOW}[Chế độ tương tác]${NC}"
    read -p "Nhập đường dẫn thư mục dự án đích cần cài đặt / cập nhật: " TARGET_DIR
    if [[ -z "$TARGET_DIR" ]]; then
        echo -e "${RED}Lỗi: Đường dẫn dự án không được để trống!${NC}"
        exit 1
    fi
fi

# Resolve absolute path for target directory
if [[ ! -d "$TARGET_DIR" ]]; then
    if [[ "$IS_UPDATE" == true ]]; then
        echo -e "${RED}Lỗi: Thư mục '$TARGET_DIR' không tồn tại, không thể chạy chế độ --update!${NC}"
        exit 1
    fi
    read -p "Thư mục '$TARGET_DIR' chưa tồn tại. Bạn có muốn tạo mới không? (y/N): " CREATE_CONFIRM
    if [[ "$CREATE_CONFIRM" =~ ^[Yy]$ ]]; then
        mkdir -p "$TARGET_DIR"
    else
        echo -e "${RED}Đã hủy cài đặt.${NC}"
        exit 1
    fi
fi

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

if [[ -z "$PROJECT_NAME" ]]; then
    DEFAULT_NAME="$(basename "$TARGET_DIR")"
    if [[ "$IS_UPDATE" == false ]]; then
        read -p "Nhập tên dự án [mặc định: $DEFAULT_NAME]: " INPUT_NAME
        PROJECT_NAME="${INPUT_NAME:-$DEFAULT_NAME}"
    else
        PROJECT_NAME="$DEFAULT_NAME"
    fi
fi

CURRENT_DATE="$(date +%Y-%m-%d)"

# ==============================================================================
# CHẾ ĐỘ CẬP NHẬT (--update) — AN TOÀN TUYỆT ĐỐI CHO SOURCE CODE HIỆN TẠI
# ==============================================================================
if [[ "$IS_UPDATE" == true ]]; then
    echo -e "\n${YELLOW}>> CHẾ ĐỘ CẬP NHẬT: Đang đồng bộ phiên bản Agent mới nhất vào dự án...${NC}"
    echo -e "Dự án: ${BOLD}${PROJECT_NAME}${NC} (${TARGET_DIR})\n"

    # 1. Cập nhật .agents/
    echo -e "${CYAN}[1/4] Cập nhật 6 Persona (.agents/)...${NC}"
    mkdir -p "${TARGET_DIR}/.agents"
    cp -Rf "${SCRIPT_DIR}/.agents/"*.md "${TARGET_DIR}/.agents/"

    # 2. Cập nhật skills/
    echo -e "${CYAN}[2/4] Cập nhật bộ Kỹ năng (skills/)...${NC}"
    mkdir -p "${TARGET_DIR}/skills"
    cp -Rf "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/"

    # 3. Cập nhật workflows/
    echo -e "${CYAN}[3/4] Cập nhật các Quy trình chuẩn (workflows/)...${NC}"
    mkdir -p "${TARGET_DIR}/workflows"
    cp -Rf "${SCRIPT_DIR}/workflows/"* "${TARGET_DIR}/workflows/"

    # 4. Cập nhật các Adapters cấu hình IDE (Không ghi đè constitution hay dữ liệu dự án)
    echo -e "${CYAN}[4/4] Cập nhật các Platform Adapters...${NC}"
    if [[ -f "${TARGET_DIR}/.cursorrules" || "$OPT_ALL" == true ]]; then
        sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" "${SCRIPT_DIR}/templates/adapters/cursor.rules.template" > "${TARGET_DIR}/.cursorrules"
        mkdir -p "${TARGET_DIR}/.cursor/rules"
        sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" "${SCRIPT_DIR}/templates/adapters/cursor.rules.template" > "${TARGET_DIR}/.cursor/rules/tc-agent.mdc"
    fi

    if [[ -f "${TARGET_DIR}/.windsurfrules" || "$OPT_ALL" == true ]]; then
        sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" "${SCRIPT_DIR}/templates/adapters/windsurf.rules.template" > "${TARGET_DIR}/.windsurfrules"
    fi

    if [[ -f "${TARGET_DIR}/CLAUDE.md" || "$OPT_ALL" == true ]]; then
        sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" "${SCRIPT_DIR}/templates/adapters/claude.md.template" > "${TARGET_DIR}/CLAUDE.md"
    fi

    echo -e "\n${GREEN}${BOLD}✓ CẬP NHẬT HOÀN TẤT!${NC}"
    echo -e "Toàn bộ Agent Personas, Skills và Workflows đã được nâng cấp lên phiên bản mới nhất."
    echo -e "Lưu ý: Mã nguồn, tài liệu dự án trong ${BOLD}src/, docs/, backlog/, specs/${NC} được bảo toàn nguyên vẹn 100%.\n"
    exit 0
fi

# ==============================================================================
# CHẾ ĐỘ CÀI ĐẶT MỚI (INITIAL SETUP)
# ==============================================================================
echo -e "\n${BLUE}==============================================================================${NC}"
echo -e "Bắt đầu triển khai Framework vào: ${BOLD}${TARGET_DIR}${NC}"
echo -e "Tên dự án: ${BOLD}${PROJECT_NAME}${NC}"
echo -e "${BLUE}==============================================================================${NC}\n"

# 1. Tạo Khung Thư Mục Chuẩn Chống Rác (Anti-Clutter Directory Matrix)
echo -e "${YELLOW}[1/6] Khởi tạo khung thư mục chuẩn mực (Zero-Tolerance Root Dumping)...${NC}"
mkdir -p "${TARGET_DIR}/.agents" \
         "${TARGET_DIR}/docs/00-presale-proposal" \
         "${TARGET_DIR}/docs/01-basic-design" \
         "${TARGET_DIR}/docs/02-detail-design" \
         "${TARGET_DIR}/docs/decisions" \
         "${TARGET_DIR}/docs/change-requests" \
         "${TARGET_DIR}/backlog/EPICS" \
         "${TARGET_DIR}/backlog/USER_STORIES" \
         "${TARGET_DIR}/specs" \
         "${TARGET_DIR}/src/Domain" \
         "${TARGET_DIR}/src/Application" \
         "${TARGET_DIR}/src/Infrastructure" \
         "${TARGET_DIR}/src/Presentation" \
         "${TARGET_DIR}/src/WebApp" \
         "${TARGET_DIR}/tests/unit" \
         "${TARGET_DIR}/tests/integration" \
         "${TARGET_DIR}/tests/e2e/screenshots" \
         "${TARGET_DIR}/workflows" \
         "${TARGET_DIR}/skills"

touch "${TARGET_DIR}/docs/00-presale-proposal/.gitkeep" \
      "${TARGET_DIR}/docs/01-basic-design/.gitkeep" \
      "${TARGET_DIR}/docs/02-detail-design/.gitkeep" \
      "${TARGET_DIR}/docs/decisions/.gitkeep" \
      "${TARGET_DIR}/docs/change-requests/.gitkeep" \
      "${TARGET_DIR}/backlog/EPICS/.gitkeep" \
      "${TARGET_DIR}/backlog/USER_STORIES/.gitkeep" \
      "${TARGET_DIR}/specs/.gitkeep" \
      "${TARGET_DIR}/src/Domain/.gitkeep" \
      "${TARGET_DIR}/src/Application/.gitkeep" \
      "${TARGET_DIR}/src/Infrastructure/.gitkeep" \
      "${TARGET_DIR}/src/Presentation/.gitkeep" \
      "${TARGET_DIR}/src/WebApp/.gitkeep" \
      "${TARGET_DIR}/tests/unit/.gitkeep" \
      "${TARGET_DIR}/tests/integration/.gitkeep" \
      "${TARGET_DIR}/tests/e2e/screenshots/.gitkeep"

echo -e "${GREEN}✓ Đã tạo thành công cây thư mục phân tầng chuẩn Clean Architecture & Docs!${NC}"

# 2. Cài đặt 6 Personas vào .agents/
echo -e "\n${YELLOW}[2/6] Cài đặt 6 Persona chuyên trách (PS, PO/PM, BA, SA, Dev, EC)...${NC}"
cp -Rf "${SCRIPT_DIR}/.agents/"*.md "${TARGET_DIR}/.agents/"
echo -e "${GREEN}✓ Đã sao chép 6 Personas vào .agents/!${NC}"

# 3. Cài đặt Kỹ năng theo Role & Workflows
echo -e "\n${YELLOW}[3/6] Cài đặt bộ Kỹ năng & 6 Quy trình chuẩn (wf-*)...${NC}"
cp -Rf "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/"
cp -Rf "${SCRIPT_DIR}/workflows/"* "${TARGET_DIR}/workflows/"
echo -e "${GREEN}✓ Đã cài đặt bộ Kỹ năng và Quy trình chuẩn!${NC}"

# 4. Khởi tạo AGENTS.md, constitution.md và BD-00-overview.md
echo -e "\n${YELLOW}[4/6] Khởi tạo tài liệu điều hành AGENTS.md và Hiến pháp kỹ thuật...${NC}"
sed -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
    -e "s/{{DATE}}/${CURRENT_DATE}/g" \
    "${SCRIPT_DIR}/templates/AGENTS.enterprise.template.md" > "${TARGET_DIR}/AGENTS.md"

sed -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
    -e "s/{{DATE}}/${CURRENT_DATE}/g" \
    "${SCRIPT_DIR}/templates/constitution.template.md" > "${TARGET_DIR}/constitution.md"

if [[ ! -f "${TARGET_DIR}/docs/01-basic-design/BD-00-overview.md" ]]; then
    sed -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
        -e "s/{{DATE}}/${CURRENT_DATE}/g" \
        "${SCRIPT_DIR}/templates/TEMPLATE-basic-design.md" > "${TARGET_DIR}/docs/01-basic-design/BD-00-overview.md"
fi

# 5. Cài đặt Adapters Đa Nền Tảng (Cursor, Windsurf, Claude Code, etc.)
echo -e "\n${YELLOW}[5/6] Cài đặt các Platform Adapters...${NC}"
if [[ "$OPT_ALL" == true || "$OPT_CURSOR" == true ]]; then
    sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" "${SCRIPT_DIR}/templates/adapters/cursor.rules.template" > "${TARGET_DIR}/.cursorrules"
    mkdir -p "${TARGET_DIR}/.cursor/rules"
    sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" "${SCRIPT_DIR}/templates/adapters/cursor.rules.template" > "${TARGET_DIR}/.cursor/rules/tc-agent.mdc"
    echo -e "${GREEN}  ✓ Đã kích hoạt Cursor Rules (.cursorrules & .cursor/rules/)${NC}"
fi

if [[ "$OPT_ALL" == true || "$OPT_WINDSURF" == true ]]; then
    sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" "${SCRIPT_DIR}/templates/adapters/windsurf.rules.template" > "${TARGET_DIR}/.windsurfrules"
    echo -e "${GREEN}  ✓ Đã kích hoạt Windsurf Cascade Rules (.windsurfrules)${NC}"
fi

if [[ "$OPT_ALL" == true || "$OPT_CLAUDE" == true ]]; then
    sed "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" "${SCRIPT_DIR}/templates/adapters/claude.md.template" > "${TARGET_DIR}/CLAUDE.md"
    echo -e "${GREEN}  ✓ Đã kích hoạt Claude Code CLI (CLAUDE.md)${NC}"
fi

# 6. Tạo Script cập nhật 1 chạm (update-tc-agent.sh) cho dự án con
echo -e "\n${YELLOW}[6/6] Tạo script cập nhật 1 chạm (update-tc-agent.sh)...${NC}"
cat << 'EOF' > "${TARGET_DIR}/update-tc-agent.sh"
#!/usr/bin/env bash
set -euo pipefail
SOURCE_REPO="TC_AGENT_SOURCE_PATH_PLACEHOLDER"

if [[ ! -d "$SOURCE_REPO" ]]; then
    echo "Lỗi: Không tìm thấy thư mục gốc của TC IT Agent tại: $SOURCE_REPO"
    echo "Hãy kiểm tra lại đường dẫn hoặc clone lại TC IT Agent."
    exit 1
fi

echo ">> Đang lấy bản cập nhật Agent mới nhất từ: $SOURCE_REPO ..."
"$SOURCE_REPO/install.sh" "$(pwd)" --update
EOF

sed -i '' "s|TC_AGENT_SOURCE_PATH_PLACEHOLDER|${SCRIPT_DIR}|g" "${TARGET_DIR}/update-tc-agent.sh" 2>/dev/null || \
sed -i "s|TC_AGENT_SOURCE_PATH_PLACEHOLDER|${SCRIPT_DIR}|g" "${TARGET_DIR}/update-tc-agent.sh"
chmod +x "${TARGET_DIR}/update-tc-agent.sh"

echo -e "${GREEN}  ✓ Đã tạo script '${BOLD}update-tc-agent.sh${NC}' trong thư mục dự án.${NC}"

echo -e "\n${BLUE}${BOLD}==============================================================================${NC}"
echo -e "${GREEN}${BOLD}✓ CÀI ĐẶT THÀNH CÔNG TC IT AGENT FRAMEWORK V2.0 VÀO DỰ ÁN!${NC}"
echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "Thư mục dự án: ${BOLD}${TARGET_DIR}${NC}"
echo -e "Các bước tiếp theo:"
echo -e "  1. Mở dự án trong Cursor, Antigravity, Windsurf hoặc Claude Code."
echo -e "  2. Bắt đầu bằng lệnh: ${CYAN}/wf-presale${NC} (để lên Proposal) hoặc ${CYAN}/wf-kickoff${NC} (để khởi tạo Basic Design)."
echo -e "  3. Khi TC IT Agent gốc có bản nâng cấp trên Git, ở dự án này chỉ cần chạy: ${BOLD}./update-tc-agent.sh${NC}\n"
