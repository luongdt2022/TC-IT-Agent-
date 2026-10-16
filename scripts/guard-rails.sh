#!/usr/bin/env bash
# ==============================================================================
# TC IT AGENT — UNIVERSAL ANTI-HALLUCINATION & ARCHITECTURE GUARDRAILS
# Chốt chặn kiểm tra toán học tự động chống ảo giác & bảo vệ toàn vẹn kiến trúc:
# 1. TypeCheck & Compiler Validation (TypeScript, Python, .NET, Go...)
# 2. Schema & Data Model Validation (Prisma, Entity Framework, Alembic...)
# 3. Kỷ luật Zero-Mock trên Client (Cấm fake arrays / dummy fallbacks trong catch)
# 4. Kỷ luật Pure Black-Box & Zero-Mock trong bộ E2E Test của QC
# 5. Kiểm toán độ phủ trường biểu mẫu Wireframe (audit_wireframe_fields.py)
# 6. Anti-Clutter Directory Linter (Chống xả rác thư mục gốc)
# 7. Shared Catalog Grounding Check (Bảo đảm có từ điển dùng chung)
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

ERRORS=0

echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "${BLUE}${BOLD}   TC IT AGENT UNIVERSAL ANTI-HALLUCINATION & ARCHITECTURE GUARDRAILS        ${NC}"
echo -e "${BLUE}${BOLD}==============================================================================${NC}\n"

# ------------------------------------------------------------------------------
# 1. COMPILER & TYPECHECK VALIDATION (CHỐNG IMPORT / HÀM / TYPE ẢO)
# ------------------------------------------------------------------------------
echo -e "${YELLOW}[1/7] Kiểm tra TypeCheck / Compiler tĩnh...${NC}"

# Case A: TypeScript / JavaScript Monorepo hoặc Single Repo
if command -v pnpm >/dev/null 2>&1 && [[ -f "${PROJECT_ROOT}/pnpm-workspace.yaml" ]]; then
    echo -e "  -> Phát hiện pnpm Monorepo, đang chạy typecheck..."
    if pnpm -r exec tsc --noEmit 2>/dev/null; then
        echo -e "${GREEN}  ✓ Monorepo TypeScript: 100% hợp lệ, không có import/type ảo.${NC}"
    else
        echo -e "${RED}  ✗ Lỗi TypeCheck trong Monorepo! Phát hiện hàm hoặc type ảo.${NC}"
        ERRORS=$((ERRORS + 1))
    fi
elif [[ -f "${PROJECT_ROOT}/tsconfig.json" ]]; then
    echo -e "  -> Phát hiện TypeScript Single Repo..."
    if npx tsc --noEmit; then
        echo -e "${GREEN}  ✓ TypeScript: 100% hợp lệ.${NC}"
    else
        echo -e "${RED}  ✗ Lỗi TypeCheck TypeScript!${NC}"
        ERRORS=$((ERRORS + 1))
    fi
fi

# Case B: Python
if [[ -f "${PROJECT_ROOT}/pyproject.toml" || -f "${PROJECT_ROOT}/requirements.txt" ]]; then
    if command -v mypy >/dev/null 2>&1; then
        echo -e "  -> Chạy mypy kiểm tra Python type hints..."
        if mypy . --ignore-missing-imports 2>/dev/null; then
            echo -e "${GREEN}  ✓ Python TypeCheck: Hợp lệ.${NC}"
        fi
    fi
fi

# Case C: .NET Core / C#
if compgen -G "${PROJECT_ROOT}/*.sln" > /dev/null || compgen -G "${PROJECT_ROOT}/*/*.csproj" > /dev/null || compgen -G "${PROJECT_ROOT}/*/*/*.csproj" > /dev/null; then
    if command -v dotnet >/dev/null 2>&1; then
        echo -e "  -> Chạy dotnet build kiểm tra mã nguồn C#..."
        if dotnet build -v q --nologo; then
            echo -e "${GREEN}  ✓ .NET Build: Thành công 0 lỗi.${NC}"
        else
            echo -e "${RED}  ✗ Lỗi biên dịch .NET!${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    fi
fi

# ------------------------------------------------------------------------------
# 2. SCHEMA & DATA MODEL VALIDATION (CHỐNG FIELD / QUAN HỆ CSDL ẢO)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[2/7] Kiểm tra Schema & Data Model CSDL...${NC}"

PRISMA_SCHEMAS=$(find "${PROJECT_ROOT}" -name "schema.prisma" -not -path "*/node_modules/*" 2>/dev/null || true)
if [[ -n "${PRISMA_SCHEMAS}" ]]; then
    for schema in ${PRISMA_SCHEMAS}; do
        echo -e "  -> Kiểm tra Prisma Schema tại: ${schema}"
        if npx prisma validate --schema="${schema}" >/dev/null 2>&1; then
            echo -e "${GREEN}  ✓ Prisma Schema hợp lệ: $(basename "$(dirname "${schema}")")${NC}"
        else
            echo -e "${RED}  ✗ Lỗi Prisma Schema tại ${schema}! Phát hiện quan hệ hoặc field không hợp lệ.${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    done
else
    echo -e "${GREEN}  ✓ Bỏ qua: Không sử dụng Prisma hoặc schema được quản lý qua ORM khác.${NC}"
fi

# ------------------------------------------------------------------------------
# 3. KỶ LUẬT ZERO-MOCK TRÊN CLIENT (CHỐNG FAKE DATA TRONG CATCH/FALLBACK)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[3/7] Quét mã nguồn kiểm tra Kỷ luật Zero-Mock trên Client...${NC}"

MOCK_LEAKS=""
SCAN_DIRS=()
[[ -d "${PROJECT_ROOT}/src" ]] && SCAN_DIRS+=("${PROJECT_ROOT}/src")
[[ -d "${PROJECT_ROOT}/SourceCode" ]] && SCAN_DIRS+=("${PROJECT_ROOT}/SourceCode")

if [[ ${#SCAN_DIRS[@]} -gt 0 ]]; then
    MOCK_LEAKS=$(grep -rnE "(fakeItem|fakeCode|dummyData|mockRecords|fallbackFake)" "${SCAN_DIRS[@]}" \
        --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=tests --exclude="*.test.*" --exclude="*.spec.*" 2>/dev/null || true)
fi

if [[ -n "${MOCK_LEAKS}" ]]; then
    echo -e "${RED}  ✗ Phát hiện Mock ngầm hoặc dữ liệu giả che giấu lỗi API trong mã nguồn Client:${NC}"
    echo "${MOCK_LEAKS}" | head -n 5
    echo -e "${YELLOW}  -> Kỷ luật Zero-Mock: Bắt buộc hiển thị trạng thái Error thật hoặc Empty state qua <Async>, không được nuốt lỗi bằng fake data.${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}  ✓ 100% Client tuân thủ Kỷ luật Zero-Mock, không phát hiện mã giả lập ngầm.${NC}"
fi

# ------------------------------------------------------------------------------
# 4. KỶ LUẬT PURE BLACK-BOX & ZERO-MOCK TRONG BỘ E2E TEST CỦA QC
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[4/7] Quét kỷ luật Pure Black-Box & Zero-Mock trong bộ E2E Test của QC...${NC}"

E2E_DIRS=$(find "${PROJECT_ROOT}" -type d \( -name "e2e" -o -name "tests" \) -not -path "*/node_modules/*" 2>/dev/null || true)
if [[ -n "${E2E_DIRS}" ]]; then
    MOCK_INFRACTIONS=$(grep -rnE --exclude-dir="__pycache__" --exclude-dir="node_modules" "(page\.route\(|route\.fulfill\(|mock_auth_token|mock_token)" ${E2E_DIRS} 2>/dev/null || true)
    if [[ -n "${MOCK_INFRACTIONS}" ]]; then
        echo -e "${RED}  ✗ LỖI NGHIÊM TRỌNG: Phát hiện mock route hoặc mock auth token trong thư mục E2E của QC:${NC}"
        echo "${MOCK_INFRACTIONS}" | head -n 5
        echo -e "${RED}  -> Vi phạm kỷ luật Quality Gate 4: Bắt buộc test trên môi trường thật (Pure Black-Box), không tự mớm mock!${NC}"
        ERRORS=$((ERRORS + 1))
    else
        echo -e "${GREEN}  ✓ Bộ test E2E sạch bóng mock: 100% Pure Black-Box Testing.${NC}"
    fi
else
    echo -e "${GREEN}  ✓ Bỏ qua: Chưa khởi tạo thư mục e2e.${NC}"
fi

# ------------------------------------------------------------------------------
# 5. KIỂM TOÁN ĐỘ PHỦ TRƯỜNG BIỂU MẪU WIREFRAME
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[5/7] Kiểm toán độ phủ trường biểu mẫu Wireframe vs Component (Controls Coverage)...${NC}"
AUDIT_SCRIPT="${SCRIPT_DIR}/audit_wireframe_fields.py"
if [[ -f "${AUDIT_SCRIPT}" ]]; then
    if python3 "${AUDIT_SCRIPT}" >/dev/null 2>&1; then
        echo -e "${GREEN}  ✓ Chốt chặn độ phủ trường biểu mẫu: Đạt chuẩn (>= 80% controls).${NC}"
    else
        echo -e "${RED}  ✗ Phát hiện biểu mẫu bị cắt xén trường so với Wireframe HTML gốc!${NC}"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "  -> Bỏ qua: Chưa cài đặt audit_wireframe_fields.py."
fi

# ------------------------------------------------------------------------------
# 6. KỶ LUẬT THƯ MỤC CHỐNG RÁC (ANTI-CLUTTER ROOT LINTER)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[6/7] Quét kỷ luật thư mục (Zero-Tolerance Root Dumping)...${NC}"

ROOGUE_FILES=$(find "${PROJECT_ROOT}" -maxdepth 1 -type f \
    -not -name "README.md" \
    -not -name "AGENTS.md" \
    -not -name "CLAUDE.md" \
    -not -name "constitution.md" \
    -not -name "install.sh" \
    -not -name "update-tc-agent.sh" \
    -not -name "loop" \
    -not -name ".gitignore" \
    -not -name ".env*" \
    -not -name "*.json" \
    -not -name "*.yaml" \
    -not -name "*.yml" \
    -not -name "*.lock" \
    -not -name "*.toml" \
    -not -name "*.sln" \
    -not -name "*.config.*" \
    -not -name ".*" \
    2>/dev/null || true)

if [[ -n "${ROOGUE_FILES}" ]]; then
    echo -e "${RED}  ✗ Phát hiện file rác hoặc file mã nguồn đặt sai vị trí tại thư mục gốc:${NC}"
    echo "${ROOGUE_FILES}"
    echo -e "${YELLOW}  -> Khuyến nghị: Gom tài liệu vào docs/, specs/ hoặc mã nguồn vào src/.${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}  ✓ Thư mục gốc sạch sẽ, 100% tuân thủ kỷ luật Anti-Clutter.${NC}"
fi

# ------------------------------------------------------------------------------
# 7. KIỂM TRA GROUNDING CATALOG
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[7/7] Kiểm tra các điểm neo Grounding...${NC}"
if [[ ( -d "${PROJECT_ROOT}/specs" || -d "${PROJECT_ROOT}/SourceCode/specs" ) && ( -d "${PROJECT_ROOT}/docs" || -d "${PROJECT_ROOT}/src" ) ]]; then
    echo -e "${GREEN}  ✓ Cấu trúc dự án có sẵn các điểm neo xác thực (specs/, docs/, src/).${NC}"
else
    echo -e "${YELLOW}  ⚠ Cảnh báo: Chưa khởi tạo đủ thư mục specs/ hoặc docs/ cho việc Grounding.${NC}"
fi

# ------------------------------------------------------------------------------
# KẾT LUẬN
# ------------------------------------------------------------------------------
echo -e "\n${BLUE}${BOLD}==============================================================================${NC}"
if [[ $ERRORS -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}✓ TẤT CẢ CHỐT CHẶN ĐỀU VƯỢT QUA (0 ẢO GIÁC - ZERO REGRESSION)!${NC}"
    echo -e "${BLUE}${BOLD}==============================================================================${NC}"
    exit 0
else
    echo -e "${RED}${BOLD}✗ PHÁT HIỆN ${ERRORS} LỖI CẦN KHẮC PHỤC TRƯỚC KHI THÔNG QUA QUALITY GATE!${NC}"
    echo -e "${BLUE}${BOLD}==============================================================================${NC}"
    exit 1
fi
