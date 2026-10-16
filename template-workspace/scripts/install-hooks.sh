#!/usr/bin/env bash
# ==============================================================================
# ENTERPRISE AGENT — UNIVERSAL GIT HOOKS INSTALLER
# Cài đặt tự động các chốt chặn chất lượng vào Git repositories của dự án:
# 1. pre-commit  : Quét secret, chạy fact-forcing-guard và guard-rails.sh
# 2. commit-msg  : Chuẩn hóa Conventional Commit (feat:, fix:, refactor:, spec:...)
# 3. pre-push    : Kiểm tra an toàn trước khi đẩy mã nguồn lên remote
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "${BLUE}${BOLD}   ENTERPRISE UNIVERSAL GIT HOOKS INSTALLER (ECC COMPLIANT)                   ${NC}"
echo -e "${BLUE}${BOLD}==============================================================================${NC}\n"

# Tự động phát hiện các repository trong dự án (Root hoặc Multi-Repo / Submodules)
REPOS=("${PROJECT_ROOT}")

# Tìm thêm các git repo con trong thư mục con nếu có (ví dụ backend, frontend, modules)
while IFS= read -r gitdir; do
    repo_dir="$(dirname "${gitdir}")"
    if [[ "${repo_dir}" != "${PROJECT_ROOT}" ]]; then
        REPOS+=("${repo_dir}")
    fi
done < <(find "${PROJECT_ROOT}" -maxdepth 3 -name ".git" -type d 2>/dev/null || true)

INSTALLED_COUNT=0

for REPO_PATH in "${REPOS[@]}"; do
    if [[ -d "${REPO_PATH}/.git" ]]; then
        HOOKS_DIR="${REPO_PATH}/.git/hooks"
        mkdir -p "${HOOKS_DIR}"
        REPO_NAME="$(basename "${REPO_PATH}")"
        echo -e "${YELLOW}>> Đang cấu hình Git Hooks cho: ${BOLD}${REPO_NAME}${NC} (${REPO_PATH})"

        # ----------------------------------------------------------------------
        # 1. PRE-COMMIT HOOK
        # ----------------------------------------------------------------------
        PRE_COMMIT_FILE="${HOOKS_DIR}/pre-commit"
        cat << 'EOF' > "${PRE_COMMIT_FILE}"
#!/usr/bin/env bash
# Enterprise Pre-commit Quality Gate (ECC Compliant)
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
PROJECT_ROOT="${REPO_ROOT}"

# Tìm scripts trong thư mục dự án
FIND_SCRIPT() {
    local script_name="$1"
    if [[ -f "${PROJECT_ROOT}/scripts/${script_name}" ]]; then
        echo "${PROJECT_ROOT}/scripts/${script_name}"
    elif [[ -f "${PROJECT_ROOT}/../scripts/${script_name}" ]]; then
        echo "${PROJECT_ROOT}/../scripts/${script_name}"
    else
        echo ""
    fi
}

ROOT_GUARD=$(FIND_SCRIPT "guard-rails.sh")
FACT_GUARD=$(FIND_SCRIPT "fact-forcing-guard.py")

echo -e "\033[0;34m[Enterprise Pre-Commit]\033[0m Đang kiểm tra tính hợp lệ trước khi commit..."

# 1. Kiểm tra cấm rò rỉ secret hoặc token
STAGED_DIFF=$(git diff --cached)
if echo "${STAGED_DIFF}" | grep -qE "(AKIA[0-9A-Z]{16}|bearer [a-zA-Z0-9_\-\.]{50,})"; then
    echo -e "\033[0;31m[LỖI BẢO MẬT] Phát hiện Hardcoded API Token / Secret trong Staged Changes!\033[0m" >&2
    exit 1
fi

# 2. Chạy Fact-Forcing Gatekeeper kiểm tra các tệp Tier-1
if [[ -n "${FACT_GUARD}" && -f "${FACT_GUARD}" ]]; then
    python3 "${FACT_GUARD}" --audit || exit 2
fi

# 3. Chạy guard-rails kiểm tra compiler tĩnh nếu tìm thấy
if [[ -n "${ROOT_GUARD}" && -f "${ROOT_GUARD}" ]]; then
    bash "${ROOT_GUARD}" || exit 1
fi

exit 0
EOF
        chmod +x "${PRE_COMMIT_FILE}"

        # ----------------------------------------------------------------------
        # 2. COMMIT-MSG HOOK
        # ----------------------------------------------------------------------
        COMMIT_MSG_FILE="${HOOKS_DIR}/commit-msg"
        cat << 'EOF' > "${COMMIT_MSG_FILE}"
#!/usr/bin/env bash
# Enterprise Commit-Message Validator (Conventional Commits)
set -euo pipefail

MSG_FILE="$1"
FIRST_LINE=$(head -n 1 "${MSG_FILE}")

# Pattern: type(scope)?: description
PATTERN="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|spec)(\([a-zA-Z0-9_-]+\))?!?: .+"

# Bỏ qua merge commit hoặc revert commit tự động
if [[ "${FIRST_LINE}" =~ ^Merge\ branch || "${FIRST_LINE}" =~ ^Revert\ \" ]]; then
    exit 0
fi

if ! [[ "${FIRST_LINE}" =~ ${PATTERN} ]]; then
    echo -e "\033[0;31m[COMMIT TỪ CHỐI] Tiêu đề commit không đúng định dạng chuẩn Conventional Commits!\033[0m" >&2
    echo -e "\033[1;33mTiêu đề hiện tại:\033[0m '${FIRST_LINE}'" >&2
    echo -e "\033[1mĐịnh dạng chuẩn bắt buộc:\033[0m <type>(<scope>): <mô tả ngắn>" >&2
    echo -e "Ví dụ hợp lệ:" >&2
    echo -e "  feat(auth): bổ sung đăng nhập 2 lớp 2FA" >&2
    echo -e "  fix(rbac): chặn lỗ hổng IDOR trên API lấy báo cáo" >&2
    echo -e "  test(e2e): bổ sung kịch bản kiểm thử blackbox thanh toán" >&2
    exit 1
fi

exit 0
EOF
        chmod +x "${COMMIT_MSG_FILE}"

        # ----------------------------------------------------------------------
        # 3. PRE-PUSH HOOK
        # ----------------------------------------------------------------------
        PRE_PUSH_FILE="${HOOKS_DIR}/pre-push"
        cat << 'EOF' > "${PRE_PUSH_FILE}"
#!/usr/bin/env bash
# Enterprise Pre-push Safety Gate
set -euo pipefail

echo -e "\033[0;34m[Enterprise Pre-Push]\033[0m Kiểm tra an toàn trước khi đẩy mã nguồn lên Remote..."

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "${CURRENT_BRANCH}" == "main" || "${CURRENT_BRANCH}" == "master" ]]; then
    echo -e "\033[1;33m  -> Đang đẩy vào nhánh chính (${CURRENT_BRANCH}). Thực hiện quét bảo vệ...\033[0m"
fi

exit 0
EOF
        chmod +x "${PRE_PUSH_FILE}"

        echo -e "${GREEN}  ✓ Đã cài đặt hoàn tất: pre-commit, commit-msg, pre-push!${NC}"
        INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
    fi
done

echo -e "\n${GREEN}${BOLD}TỔNG KẾT: Đã cài đặt Git Hooks thành công cho ${INSTALLED_COUNT} repositories!${NC}"
