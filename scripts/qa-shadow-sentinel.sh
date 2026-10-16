#!/usr/bin/env bash
# ==============================================================================
# TC IT AGENT FRAMEWORK — SHADOW QA SENTINEL & REAL-TIME AUDIT INSPECTOR
# Tác tử kiểm toán độc lập bảo vệ quy trình:
# 1. Đo lường dung lượng Token Context (Ngưỡng 60% - 80%) từ transcript log
# 2. Bắt quả tang vi phạm Gate 2: Sửa code khi chưa có plan.md / tasks.md
# 3. Quét triệt tiêu Mock ngầm (Zero-Mock Detector) trong Frontend & Backend
# 4. Kiểm toán bài test QC: Cấm Shallow Assertion, bắt buộc đối soát CSDL thật
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
WARNINGS=0

echo -e "${BLUE}${BOLD}==============================================================================${NC}"
echo -e "${BLUE}${BOLD}       TC IT AGENT — SHADOW QA SENTINEL & REAL-TIME AUDIT INSPECTION          ${NC}"
echo -e "${BLUE}${BOLD}==============================================================================${NC}\n"

# ------------------------------------------------------------------------------
# 1. CONTEXT TELEMETRY MONITOR (Đo lường dung lượng Token Context)
# ------------------------------------------------------------------------------
echo -e "${YELLOW}[1/4] Kiểm tra Dung lượng Context & Trạng thái Trí nhớ của Agent...${NC}"

# Tìm file transcript.jsonl gần nhất trong thư mục brain của antigravity
TRANSCRIPT_FILE=$(find "${HOME}/.gemini/antigravity/brain" -name "transcript.jsonl" -type f 2>/dev/null | xargs ls -t 2>/dev/null | head -n 1 || true)

if [[ -n "${TRANSCRIPT_FILE}" && -f "${TRANSCRIPT_FILE}" ]]; then
    LAST_LINE=$(tail -n 1 "${TRANSCRIPT_FILE}")
    
    # Trích xuất input_tokens, cache_read_tokens, output_tokens
    INPUT_TOKENS=$(echo "${LAST_LINE}" | grep -o '"input_tokens":[0-9]*' | cut -d':' -f2 || echo 0)
    CACHE_TOKENS=$(echo "${LAST_LINE}" | grep -o '"cache_read_tokens":[0-9]*' | cut -d':' -f2 || echo 0)
    OUTPUT_TOKENS=$(echo "${LAST_LINE}" | grep -o '"output_tokens":[0-9]*' | cut -d':' -f2 || echo 0)
    STEP_INDEX=$(echo "${LAST_LINE}" | grep -o '"step_index":[0-9]*' | cut -d':' -f2 || echo 0)
    
    TOTAL_TOKENS=$((INPUT_TOKENS + CACHE_TOKENS + OUTPUT_TOKENS))
    
    echo -e "  -> Bước hội thoại: ${BOLD}Step #${STEP_INDEX}${NC}"
    echo -e "  -> Tổng Token Context: ${BOLD}${TOTAL_TOKENS}${NC} (Cache: ${CACHE_TOKENS}, Input: ${INPUT_TOKENS}, Output: ${OUTPUT_TOKENS})"
    
    # Đánh giá 3 ngưỡng
    if [[ ${TOTAL_TOKENS} -ge 120000 ]]; then
        echo -e "${RED}${BOLD}  [BÁO ĐỘNG ĐỎ] Context đạt ngưỡng ${TOTAL_TOKENS} tokens (>= 80% dung lượng)!${NC}"
        echo -e "${RED}  ✗ NGUY CƠ CAO: Agent bắt đầu suy thoái trí nhớ, có dấu hiệu làm ẩu hoặc bỏ bước.${NC}"
        echo -e "${YELLOW}  -> HÀNH ĐỘNG BẮT BUỘC:${NC}"
        echo -e "     1. Yêu cầu Agent ghi điểm lưu: specs/<epic>/.session_checkpoint.md"
        echo -e "     2. Gõ lệnh /compact để thu gọn ngữ cảnh, hoặc mở Clean Session mới!"
        ERRORS=$((ERRORS + 1))
    elif [[ ${TOTAL_TOKENS} -ge 80000 ]]; then
        echo -e "${YELLOW}${BOLD}  [CẢNH BÁO SỚM] Context đã chạm ngưỡng ${TOTAL_TOKENS} tokens (>= 60% dung lượng).${NC}"
        echo -e "${YELLOW}  ⚠ Khuyến nghị: Tập trung dứt điểm task hiện tại, không kéo thêm file tài liệu lớn vào chat.${NC}"
        WARNINGS=$((WARNINGS + 1))
    else
        echo -e "${GREEN}  ✓ Context an toàn (${TOTAL_TOKENS} tokens < 60%). Trí nhớ Agent đang ở trạng thái tối ưu.${NC}"
    fi
else
    echo -e "  -> Không tìm thấy file transcript log local, bỏ qua bước đo token."
fi

# ------------------------------------------------------------------------------
# 2. BẮT QUẢ TANG VI PHẠM GATE 2 (Code trước khi Design)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[2/4] Kiểm toán Gate 2: Rà soát hành vi 'Code chay' khi chưa có Detail Design...${NC}"

# Lấy danh sách file source code đang bị sửa đổi (unstaged hoặc staged)
MODIFIED_SOURCE=$(git status --porcelain 2>/dev/null | grep -E '\.(cs|tsx|ts|jsx|js|py|go|java)$' || true)

if [[ -n "${MODIFIED_SOURCE}" ]]; then
    # Kiểm tra xem có epic nào đang được triển khai trong specs/ hoặc SourceCode/specs/
    SPECS_DIR="${PROJECT_ROOT}/specs"
    [[ ! -d "${SPECS_DIR}" && -d "${PROJECT_ROOT}/SourceCode/specs" ]] && SPECS_DIR="${PROJECT_ROOT}/SourceCode/specs"
    
    if [[ -d "${SPECS_DIR}" ]]; then
        ACTIVE_EPICS=$(find "${SPECS_DIR}" -mindepth 1 -maxdepth 1 -type d 2>/dev/null || true)
        for ep in ${ACTIVE_EPICS}; do
            EPIC_NAME=$(basename "${ep}")
            PLAN_FILE="${ep}/plan.md"
            TASKS_FILE="${ep}/tasks.md"
            
            if [[ ! -f "${PLAN_FILE}" ]]; then
                echo -e "${RED}  ✗ VI PHẠM GATE 2: Phát hiện sửa mã nguồn nhưng Epic ${EPIC_NAME} CHƯA CÓ plan.md!${NC}"
                echo -e "    File code bị sửa: $(echo "${MODIFIED_SOURCE}" | head -n 3 | tr '\n' ' ')"
                echo -e "${RED}    -> CẮT LUỒNG DEV! Bắt buộc phải hoàn tất sa-plan trước khi viết code.${NC}"
                ERRORS=$((ERRORS + 1))
            fi
            
            if [[ ! -f "${TASKS_FILE}" ]]; then
                echo -e "${RED}  ✗ VI PHẠM GATE 2: Epic ${EPIC_NAME} CHƯA CÓ tasks.md phân rã công việc!${NC}"
                echo -e "${RED}    -> CẮT LUỒNG DEV! Bắt buộc phải hoàn tất dev-tasks trước khi viết code.${NC}"
                ERRORS=$((ERRORS + 1))
            fi
        done
    fi
    
    if [[ ${ERRORS} -eq 0 ]]; then
        echo -e "${GREEN}  ✓ Mã nguồn sửa đổi tuân thủ nghiêm ngặt: Đã có đầy đủ plan.md và tasks.md.${NC}"
    fi
else
    echo -e "${GREEN}  ✓ Workspace sạch sẽ, không có file code nào bị sửa chay.${NC}"
fi

# ------------------------------------------------------------------------------
# 3. SĂN TÌM MOCK NGẦM (ZERO-MOCK DETECTOR)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[3/4] Quét triệt tiêu dữ liệu giả & Mock ngầm (Zero-Mock Audit)...${NC}"

DIFF_CONTENT=$(git diff HEAD 2>/dev/null || true)
MOCK_PATTERNS=("fakeItem" "fakeCode" "fakeUser" "mockData" "dummyData" "fakeList")

FOUND_MOCK=false
for pat in "${MOCK_PATTERNS[@]}"; do
    if echo "${DIFF_CONTENT}" | grep -q "${pat}"; then
        echo -e "${RED}  ✗ PHÁT HIỆN MOCK NGẦM: Tìm thấy pattern '${pat}' trong Git Diff!${NC}"
        FOUND_MOCK=true
    fi
done

if [[ "${FOUND_MOCK}" = true ]]; then
    echo -e "${RED}  -> ĐÁNH FAIL GATE 3/4! Dự án nghiêm cấm dùng mock ngầm để lấy kết quả pass ảo.${NC}"
    echo -e "${YELLOW}  -> Yêu cầu Dev/QC: Xóa bỏ toàn bộ dữ liệu giả và kết nối trực tiếp API/DB thật.${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}  ✓ Không phát hiện mock ngầm trong mã nguồn mới.${NC}"
fi

# ------------------------------------------------------------------------------
# 4. KIỂM TOÁN TÍNH CHÂN THỰC BÀI TEST CỦA QC (QC INTEGRITY AUDIT)
# ------------------------------------------------------------------------------
echo -e "\n${YELLOW}[4/4] Thẩm định chất lượng bài test của QC (Deep DB Assertion Audit)...${NC}"

TEST_FILES=$(find "${PROJECT_ROOT}" -name "*.spec.ts" -o -name "*.e2e.ts" -o -name "*.spec.js" 2>/dev/null | grep -v "node_modules" || true)

if [[ -n "${TEST_FILES}" ]]; then
    for tf in ${TEST_FILES}; do
        # Nếu file test có mutation (submit, click nút Lưu/Tạo/Xác nhận) mà không có lệnh query DB hoặc API verify
        if grep -qE "(click\(['\"].*submit|click\(['\"].*Lưu|click\(['\"].*Tạo|click\(['\"].*Confirm)" "${tf}" 2>/dev/null; then
            if ! grep -qE "(psql|SELECT|docker exec|prisma|dbContext|api/v1|sqlite|mysql)" "${tf}" 2>/dev/null; then
                echo -e "${YELLOW}  ⚠ Cảnh báo bài test tại ${tf}:${NC}"
                echo -e "    Có thao tác Submit/Lưu nhưng thiếu bước đối soát CSDL thật (Deep DB Assertion)!"
                WARNINGS=$((WARNINGS + 1))
            fi
        fi
        
        # Bắt page.route mớm data
        if grep -qE "(page\.route|route\.fulfill|mock_auth_token|mock_token)" "${tf}" 2>/dev/null; then
            echo -e "${RED}  ✗ VI PHẠM ZERO-MOCK TRONG TEST: File ${tf} sử dụng page.route() hoặc inject token giả!${NC}"
            ERRORS=$((ERRORS + 1))
        fi
    done
    
    if [[ ${ERRORS} -eq 0 && ${WARNINGS} -eq 0 ]]; then
        echo -e "${GREEN}  ✓ Các file test đạt chuẩn kiểm thử thật, không mớm token/data ảo.${NC}"
    fi
else
    echo -e "  -> Chưa có file E2E test mới trong workspace."
fi

# ------------------------------------------------------------------------------
# TỔNG KẾT KIỂM TOÁN SHADOW QA
# ------------------------------------------------------------------------------
echo -e "\n${BLUE}${BOLD}==============================================================================${NC}"
if [[ ${ERRORS} -gt 0 ]]; then
    echo -e "${RED}${BOLD}  ✗ SHADOW QA PHÁT HIỆN ${ERRORS} LỖI VI PHẠM NGHIÊM TRỌNG! ĐÌNH CHỈ TIẾN TRÌNH.${NC}"
    echo -e "${RED}  Vui lòng xử lý các vi phạm nêu trên trước khi tiếp tục chu trình!${NC}"
    echo -e "${BLUE}${BOLD}==============================================================================${NC}\n"
    exit 1
elif [[ ${WARNINGS} -gt 0 ]]; then
    echo -e "${YELLOW}${BOLD}  ⚠ SHADOW QA: CẢNH BÁO ${WARNINGS} ĐIỂM CẦN LƯU Ý (XEM CHI TIẾT BÊN TRÊN).${NC}"
    echo -e "${BLUE}${BOLD}==============================================================================${NC}\n"
    exit 0
else
    echo -e "${GREEN}${BOLD}  ✓ SHADOW QA: 100% TUÂN THỦ QUY TRÌNH. WORKSPACE AN TOÀN, SẴN SÀNG LÀM VIỆC!${NC}"
    echo -e "${BLUE}${BOLD}==============================================================================${NC}\n"
    exit 0
fi
