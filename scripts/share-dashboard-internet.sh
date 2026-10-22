#!/usr/bin/env bash
# ==============================================================================
# TC IT AGENT - SHARE ORCHESTRATOR & CR DASHBOARD TO INTERNET
# Công cụ tạo đường dẫn Internet (HTTPS) công khai để người dùng bên ngoài
# có thể truy cập trực tiếp Web Dashboard và gửi Change Request (CR) vào dự án.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CLOUDFLARED="/opt/homebrew/bin/cloudflared"

if [ ! -f "$CLOUDFLARED" ]; then
  CLOUDFLARED="$(which cloudflared 2>/dev/null || true)"
fi

if [ -z "$CLOUDFLARED" ]; then
  echo "❌ Chưa tìm thấy công cụ cloudflared trên máy."
  echo "👉 Cài đặt nhanh bằng lệnh: brew install cloudflared"
  exit 1
fi

echo "🔍 1. Kiểm tra dịch vụ Agent Dashboard (Port 8420)..."
if ! lsof -i :8420 >/dev/null 2>&1; then
  echo "⚠️ Port 8420 chưa chạy. Đang khởi động Agent Dashboard API Server..."
  python3 "$PROJECT_ROOT/dashboard/api/server.py" >/dev/null 2>&1 &
  sleep 2
fi
echo "   ✅ Port 8420 đang sẵn sàng."

# Kiểm tra nếu có frontend web đang chạy (port 3000 hoặc 5173)
TARGET_PORT=8420
if lsof -i :3000 >/dev/null 2>&1; then
  TARGET_PORT=3000
  echo "   ℹ️ Phát hiện Web Frontend đang chạy tại Port 3000."
fi

echo ""
echo "🚀 2. Đang khởi tạo đường hầm Cloudflare Tunnel (HTTPS) ra Internet cho Port ${TARGET_PORT}..."
LOG_FILE="/tmp/tc_agent_tunnel_$$.log"
"$CLOUDFLARED" tunnel --url "http://127.0.0.1:${TARGET_PORT}" > "$LOG_FILE" 2>&1 &
TUNNEL_PID=$!

trap "echo ''; echo '🛑 Đang đóng tunnel...'; kill $TUNNEL_PID 2>/dev/null || true; rm -f '$LOG_FILE'; exit 0" INT TERM EXIT

# Chờ lấy URL trycloudflare.com
FOUND_URL=""
for i in {1..20}; do
  if grep -E "https://[a-zA-Z0-9-]+\.trycloudflare\.com" "$LOG_FILE" >/dev/null 2>&1; then
    FOUND_URL=$(grep -oE "https://[a-zA-Z0-9-]+\.trycloudflare\.com" "$LOG_FILE" | head -n 1)
    break
  fi
  sleep 1
done

if [ -z "$FOUND_URL" ]; then
  echo "❌ Không lấy được đường dẫn Tunnel. Chi tiết log:"
  cat "$LOG_FILE"
  exit 1
fi

echo ""
echo "=============================================================================="
echo "🎉 ĐÃ KẾT NỐI INTERNET THÀNH CÔNG!"
echo "=============================================================================="
echo ""
if [ "$TARGET_PORT" == "8420" ]; then
  echo "🌐 1. TRUY CẬP TRỰC TIẾP TRANG DASHBOARD & CR PORTAL:"
  echo "👉 ${FOUND_URL}/"
else
  echo "🌐 1. TRUY CẬP TRỰC TIẾP TRANG DASHBOARD TRÊN WEB PORTAL:"
  echo "👉 ${FOUND_URL}/dashboard (hoặc ${FOUND_URL}/)"
fi
echo ""
echo "📋 Người ngoài internet có thể:"
echo "   - Xem đồ thị tiến độ Wave DAG, 3 Cổng Kiểm Duyệt (Human Gates)."
echo "   - Bấm nút '+ Thêm Yêu Cầu / CR' để gửi Change Request trực tiếp (kèm ảnh dán/upload)."
echo "   - Dữ liệu được ghi thẳng vào CSDL/Backlog dự án thời gian thực."
echo ""
echo "⚠️  (Nhấn Ctrl + C để dừng chia sẻ ra Internet bất cứ lúc nào)"
echo "=============================================================================="

# Đưa link vào clipboard nếu trên Mac
if which pbcopy >/dev/null 2>&1; then
  echo "${FOUND_URL}" | pbcopy
  echo "✨ (Đã tự động sao chép link '${FOUND_URL}' vào bộ nhớ tạm của bạn!)"
fi

wait $TUNNEL_PID
