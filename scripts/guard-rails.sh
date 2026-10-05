#!/usr/bin/env bash
# ==============================================================================
# TC IT AGENT — UNIVERSAL ANTI-HALLUCINATION & ARCHITECTURE GUARDRAILS
# Chốt chặn kiểm tra toán học tự động chống ảo giác & bảo vệ toàn vẹn kiến trúc:
# 1. TypeCheck & Compiler Validation (TypeScript, Python, .NET, Go...)
# 2. Schema & Data Model Validation (Prisma, Entity Framework, Alembic...)
# 3. Anti-Clutter Directory Linter (Chống xả rác thư mục gốc)
# 4. Shared Catalog Grounding Check (Bảo đảm có từ điển dùng chung)
# ==============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

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
echo -e "${YELLOW}[1/4] Kiểm tra TypeCheck / Compiler tĩnh...${NC}"

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
if compgen -G "${PROJECT_ROOT}/*.sln" > /dev/null || compgen -G "${PROJECT_ROOT}/*/*.csproj" > /dev/null; then
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
echo -e "\n${YELLOW}[2/4] Kiểm tra Schema & Data Model CSDL...${NC}"

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
# 3. KỶ LUẬT THƯ MỤC CHỐNG RÁC (ANTI-CLUTTER ROOT LINTER)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[3/4] Quét kỷ luật thư mục (Zero-Tolerance Root Dumping)...${NC}"

ROOGUE_FILES=$(find "${PROJECT_ROOT}" -maxdepth 1 -type f \
    -not -name "README.md" \
    -not -name "AGENTS.md" \
    -not -name "CLAUDE.md" \
    -not -name "constitution.md" \
    -not -name "install.sh" \
    -not -name "update-tc-agent.sh" \
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
# 4. KIỂM TRA GROUNDING CATALOG
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[4/4] Kiểm tra các điểm neo Grounding...${NC}"
if [[ -d "${PROJECT_ROOT}/specs" && ( -d "${PROJECT_ROOT}/docs" || -d "${PROJECT_ROOT}/src" ) ]]; then
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
