#!/usr/bin/env bash
# ==============================================================================
# TC IT AGENT FRAMEWORK — UNIVERSAL ENTERPRISE INSTALLER & UPDATER (v4.0)
# Cài đặt & Cập nhật 7 Subagents (.agents/agents/), Hooks, Core Skills, Workflows
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "${BLUE}${BOLD}   TC IT AGENT FRAMEWORK V4.0 — ENTERPRISE MULTI-AGENT SYSTEM                 ${NC}"
echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "Nguồn cài đặt: ${SCRIPT_DIR}\n"

usage() {
    echo -e "Cách sử dụng:"
    echo -e "  1. Cài đặt vào dự án MỚI hoặc ĐANG CHẠY:"
    echo -e "     ${BOLD}./install.sh /duong-dan/toi/du-an --name \"TenDuAn\" [--with-seo] [tùy chọn nền tảng]${NC}"
    echo -e "  2. CẬP NHẬT (--update) bảo toàn code dự án:"
    echo -e "     ${BOLD}./install.sh /duong-dan/toi/du-an --update [--with-seo]${NC}"
    echo -e "  3. Cài đặt toàn cục cho Antigravity IDE:"
    echo -e "     ${BOLD}./install.sh --global [--with-seo]${NC}"
    echo -e ""
    echo -e "  Tùy chọn:"
    echo -e "     ${CYAN}--with-seo${NC}     Cài thêm gói 31 kỹ năng SEO chuyên sâu (packs/seo/)"
    echo -e "     ${CYAN}--all${NC}          Cài adapter cho tất cả IDE (mặc định)"
    echo -e "     ${CYAN}--antigravity${NC}  Cài chuẩn Antigravity (.agents/agents/, hooks.json, skills)"
    echo -e "     ${CYAN}--cursor${NC}       Cài Cursor (.cursorrules & .cursor/rules/)"
    echo -e "     ${CYAN}--windsurf${NC}     Cài Windsurf (.windsurfrules)"
    echo -e "     ${CYAN}--claude${NC}       Cài Claude Code (CLAUDE.md)"
    echo -e "     ${CYAN}--generic${NC}      Cài AGENTS.md chuẩn chung"
    exit 1
}

render_template() {
    local src="$1"
    local dst="$2"
    local proj="$3"
    local dt="$4"
    python3 -c '
import sys, pathlib
src, dst, proj, dt = sys.argv[1:5]
txt = pathlib.Path(src).read_text(encoding="utf-8")
txt = txt.replace("{{PROJECT_NAME}}", proj).replace("{{DATE}}", dt)
pathlib.Path(dst).write_text(txt, encoding="utf-8")
' "$src" "$dst" "$proj" "$dt"
}

TARGET_DIR=""
PROJECT_NAME=""
IS_GLOBAL=false
IS_UPDATE=false
WITH_SEO=false
OPT_ALL=true
OPT_CURSOR=false
OPT_WINDSURF=false
OPT_CLAUDE=false
OPT_ANTIGRAVITY=false
OPT_GENERIC=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --global) IS_GLOBAL=true; shift ;;
        --update) IS_UPDATE=true; shift ;;
        --with-seo) WITH_SEO=true; shift ;;
        --name) PROJECT_NAME="$2"; shift 2 ;;
        --all) OPT_ALL=true; shift ;;
        --cursor) OPT_ALL=false; OPT_CURSOR=true; shift ;;
        --windsurf) OPT_ALL=false; OPT_WINDSURF=true; shift ;;
        --claude) OPT_ALL=false; OPT_CLAUDE=true; shift ;;
        --antigravity) OPT_ALL=false; OPT_ANTIGRAVITY=true; shift ;;
        --generic) OPT_ALL=false; OPT_GENERIC=true; shift ;;
        -h|--help) usage ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then TARGET_DIR="$1"; fi
            shift ;;
    esac
done

if [[ "$IS_GLOBAL" == true ]]; then
    GLOBAL_SKILLS_DIR="${HOME}/.gemini/config/skills"
    GLOBAL_AGENTS_DIR="${HOME}/.gemini/config/agents"
    echo -e "${YELLOW}>> Cài đặt Core Skills -> ${GLOBAL_SKILLS_DIR}${NC}"
    mkdir -p "${GLOBAL_SKILLS_DIR}" "${GLOBAL_AGENTS_DIR}"
    cp -Rf "${SCRIPT_DIR}/skills/"* "${GLOBAL_SKILLS_DIR}/"
    if [[ "$WITH_SEO" == true && -d "${SCRIPT_DIR}/packs/seo/skills" ]]; then
        echo -e "${YELLOW}>> Cài đặt thêm gói SEO Pack (--with-seo)...${NC}"
        cp -Rf "${SCRIPT_DIR}/packs/seo/skills/"* "${GLOBAL_SKILLS_DIR}/"
    fi
    cp -Rf "${SCRIPT_DIR}/.agents/agents/"*.md "${GLOBAL_AGENTS_DIR}/"
    echo -e "${GREEN}✓ Đã cập nhật Skills & 7 Subagents toàn cục thành công!${NC}"
    exit 0
fi

if [[ -z "$TARGET_DIR" ]]; then
    read -p "Nhập đường dẫn thư mục dự án đích: " TARGET_DIR
    [[ -z "$TARGET_DIR" ]] && { echo -e "${RED}Lỗi: Đường dẫn dự án trống!${NC}"; exit 1; }
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    [[ "$IS_UPDATE" == true ]] && { echo -e "${RED}Lỗi: '$TARGET_DIR' không tồn tại!${NC}"; exit 1; }
    read -p "Thư mục '$TARGET_DIR' chưa tồn tại. Tạo mới? (y/N): " CREATE_CONFIRM
    [[ "$CREATE_CONFIRM" =~ ^[Yy]$ ]] && mkdir -p "$TARGET_DIR" || exit 1
fi

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"
DEFAULT_NAME="$(basename "$TARGET_DIR")"
if [[ -z "$PROJECT_NAME" ]]; then
    if [[ "$IS_UPDATE" == false ]]; then
        read -p "Nhập tên dự án [mặc định: $DEFAULT_NAME]: " INPUT_NAME
        PROJECT_NAME="${INPUT_NAME:-$DEFAULT_NAME}"
    else
        PROJECT_NAME="$DEFAULT_NAME"
    fi
fi
CURRENT_DATE="$(date +%Y-%m-%d)"

sync_framework_assets() {
    mkdir -p "${TARGET_DIR}/.agents/agents" "${TARGET_DIR}/.agents/skills" \
             "${TARGET_DIR}/skills" "${TARGET_DIR}/workflows" \
             "${TARGET_DIR}/scripts" "${TARGET_DIR}/engine" "${TARGET_DIR}/dashboard" \
             "${TARGET_DIR}/docs/decisions" "${TARGET_DIR}/docs/system" \
             "${TARGET_DIR}/.facts" "${TARGET_DIR}/.memory/checkpoints" \
             "${TARGET_DIR}/.memory/learnings" "${TARGET_DIR}/.memory/handoffs" \
             "${TARGET_DIR}/logs"

    # 1. Subagents & Hooks
    cp -Rf "${SCRIPT_DIR}/.agents/agents/"*.md "${TARGET_DIR}/.agents/agents/"
    cp -f "${SCRIPT_DIR}/.agents/hooks.json" "${TARGET_DIR}/.agents/hooks.json"

    # 2. Core Skills (+ optional SEO pack)
    cp -Rf "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/"
    cp -Rf "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/.agents/skills/"
    if [[ "$WITH_SEO" == true && -d "${SCRIPT_DIR}/packs/seo/skills" ]]; then
        cp -Rf "${SCRIPT_DIR}/packs/seo/skills/"* "${TARGET_DIR}/skills/"
        cp -Rf "${SCRIPT_DIR}/packs/seo/skills/"* "${TARGET_DIR}/.agents/skills/"
    fi

    # 3. Workflows & Scripts
    cp -Rf "${SCRIPT_DIR}/workflows/"* "${TARGET_DIR}/workflows/"
    cp -Rf "${SCRIPT_DIR}/scripts/"* "${TARGET_DIR}/scripts/"
    chmod +x "${TARGET_DIR}/scripts/"*.sh "${TARGET_DIR}/scripts/"*.py 2>/dev/null || true

    # 4. Engine, ./loop & Dashboard
    cp -f "${SCRIPT_DIR}/engine/tc-loop.py" "${TARGET_DIR}/engine/"
    chmod +x "${TARGET_DIR}/engine/tc-loop.py" 2>/dev/null || true
    if [[ ! -f "${TARGET_DIR}/engine/policy.toml" ]]; then
        cp -f "${SCRIPT_DIR}/engine/policy.toml" "${TARGET_DIR}/engine/"
    fi
    cp -f "${SCRIPT_DIR}/loop" "${TARGET_DIR}/loop"
    chmod +x "${TARGET_DIR}/loop" 2>/dev/null || true
    cp -Rf "${SCRIPT_DIR}/dashboard/"* "${TARGET_DIR}/dashboard/"
}

if [[ "$IS_UPDATE" == true ]]; then
    echo -e "\n${YELLOW}>> CHẾ ĐỘ CẬP NHẬT (--update): ${PROJECT_NAME}${NC}"
    sync_framework_assets
    if [[ -f "${TARGET_DIR}/.cursorrules" || "$OPT_ALL" == true || "$OPT_CURSOR" == true ]]; then
        mkdir -p "${TARGET_DIR}/.cursor/rules"
        render_template "${SCRIPT_DIR}/templates/adapters/cursor.rules.template" "${TARGET_DIR}/.cursorrules" "$PROJECT_NAME" "$CURRENT_DATE"
        render_template "${SCRIPT_DIR}/templates/adapters/cursor.rules.template" "${TARGET_DIR}/.cursor/rules/tc-agent.mdc" "$PROJECT_NAME" "$CURRENT_DATE"
    fi
    if [[ -f "${TARGET_DIR}/.windsurfrules" || "$OPT_ALL" == true || "$OPT_WINDSURF" == true ]]; then
        render_template "${SCRIPT_DIR}/templates/adapters/windsurf.rules.template" "${TARGET_DIR}/.windsurfrules" "$PROJECT_NAME" "$CURRENT_DATE"
    fi
    if [[ -f "${TARGET_DIR}/CLAUDE.md" || "$OPT_ALL" == true || "$OPT_CLAUDE" == true ]]; then
        render_template "${SCRIPT_DIR}/templates/adapters/claude.md.template" "${TARGET_DIR}/CLAUDE.md" "$PROJECT_NAME" "$CURRENT_DATE"
    fi
    echo -e "${GREEN}${BOLD}✓ CẬP NHẬT HOÀN TẤT (v4.0)! Mã nguồn và dữ liệu dự án được bảo toàn 100%.${NC}"
    exit 0
fi

# INITIAL SETUP
mkdir -p "${TARGET_DIR}/docs/00-presale-proposal" \
         "${TARGET_DIR}/docs/01-basic-design" \
         "${TARGET_DIR}/docs/02-detail-design" \
         "${TARGET_DIR}/docs/change-requests" \
         "${TARGET_DIR}/docs/wireframes" \
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
         "${TARGET_DIR}/tests/e2e/screenshots"

touch "${TARGET_DIR}/docs/open-questions.md"
sync_framework_assets

if [[ "$OPT_ALL" == true || "$OPT_ANTIGRAVITY" == true || "$OPT_GENERIC" == true ]]; then
    render_template "${SCRIPT_DIR}/templates/AGENTS.enterprise.template.md" "${TARGET_DIR}/AGENTS.md" "$PROJECT_NAME" "$CURRENT_DATE"
fi
render_template "${SCRIPT_DIR}/templates/constitution.template.md" "${TARGET_DIR}/constitution.md" "$PROJECT_NAME" "$CURRENT_DATE"
if [[ ! -f "${TARGET_DIR}/docs/01-basic-design/BD-00-overview.md" ]]; then
    render_template "${SCRIPT_DIR}/templates/TEMPLATE-basic-design.md" "${TARGET_DIR}/docs/01-basic-design/BD-00-overview.md" "$PROJECT_NAME" "$CURRENT_DATE"
fi

if [[ "$OPT_ALL" == true || "$OPT_CURSOR" == true ]]; then
    mkdir -p "${TARGET_DIR}/.cursor/rules"
    render_template "${SCRIPT_DIR}/templates/adapters/cursor.rules.template" "${TARGET_DIR}/.cursorrules" "$PROJECT_NAME" "$CURRENT_DATE"
    render_template "${SCRIPT_DIR}/templates/adapters/cursor.rules.template" "${TARGET_DIR}/.cursor/rules/tc-agent.mdc" "$PROJECT_NAME" "$CURRENT_DATE"
fi
if [[ "$OPT_ALL" == true || "$OPT_WINDSURF" == true ]]; then
    render_template "${SCRIPT_DIR}/templates/adapters/windsurf.rules.template" "${TARGET_DIR}/.windsurfrules" "$PROJECT_NAME" "$CURRENT_DATE"
fi
if [[ "$OPT_ALL" == true || "$OPT_CLAUDE" == true ]]; then
    render_template "${SCRIPT_DIR}/templates/adapters/claude.md.template" "${TARGET_DIR}/CLAUDE.md" "$PROJECT_NAME" "$CURRENT_DATE"
fi

if [[ -d "${TARGET_DIR}/.git" && -f "${TARGET_DIR}/scripts/install-hooks.sh" ]]; then
    bash "${TARGET_DIR}/scripts/install-hooks.sh" >/dev/null 2>&1 || true
fi

cat << EOF > "${TARGET_DIR}/update-tc-agent.sh"
#!/usr/bin/env bash
set -euo pipefail
SOURCE_REPO="${SCRIPT_DIR}"
[[ ! -d "\$SOURCE_REPO" ]] && { echo "Không tìm thấy TC IT Agent tại: \$SOURCE_REPO"; exit 1; }
"\$SOURCE_REPO/install.sh" "\$(pwd)" --update
EOF
chmod +x "${TARGET_DIR}/update-tc-agent.sh"

echo -e "${GREEN}${BOLD}✓ CÀI ĐẶT THÀNH CÔNG TC IT AGENT FRAMEWORK V4.0 VÀO ${TARGET_DIR}!${NC}"
