#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TC IT AGENT FRAMEWORK — PO/PM PROGRESS REPORT & EMAIL DISPATCHER
Đóng vai trò Product Owner & Project Manager (po-pm) tự động tổng hợp
tiến độ toàn diện của dự án và gửi email/thông báo báo cáo tiến độ.
"""

import os
import sys
import glob
import re
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
SPECS_DIR = ROOT_DIR / "specs"
if not SPECS_DIR.exists() and (ROOT_DIR / "SourceCode" / "specs").exists():
    SPECS_DIR = ROOT_DIR / "SourceCode" / "specs"

ROADMAP_FILE = SPECS_DIR / "ROADMAP.md"
if not ROADMAP_FILE.exists() and (ROOT_DIR / "backlog" / "ROADMAP.md").exists():
    ROADMAP_FILE = ROOT_DIR / "backlog" / "ROADMAP.md"

ENV_EMAIL_FILE = ROOT_DIR / ".env.email"
DEFAULT_RECIPIENT = os.environ.get("MAIL_TO", "admin@example.com")

def load_email_env():
    """Đọc cấu hình email từ .env.email hoặc biến môi trường."""
    env_config = {
        "SMTP_HOST": os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        "SMTP_PORT": int(os.environ.get("SMTP_PORT", "587")),
        "SMTP_USER": os.environ.get("SMTP_USER", ""),
        "SMTP_PASSWORD": os.environ.get("SMTP_PASSWORD", os.environ.get("GMAIL_APP_PASSWORD", "")),
        "SMTP_FROM": os.environ.get("SMTP_FROM", ""),
        "SMTP_FROM_NAME": os.environ.get("SMTP_FROM_NAME", "TC IT Agent PO/PM"),
        "MAIL_TO": os.environ.get("MAIL_TO", DEFAULT_RECIPIENT)
    }

    if ENV_EMAIL_FILE.exists():
        with open(ENV_EMAIL_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key == "SMTP_PORT":
                        env_config[key] = int(val)
                    else:
                        env_config[key] = val

    if not env_config["SMTP_FROM"] and env_config["SMTP_USER"]:
        env_config["SMTP_FROM"] = env_config["SMTP_USER"]

    return env_config

def get_task_statistics():
    """Quét toàn bộ tasks.md trong thư mục specs để lấy số liệu thực."""
    stats = {}
    total_done = 0
    total_tasks = 0

    if SPECS_DIR.exists():
        epic_folders = sorted(glob.glob(str(SPECS_DIR / "*")))
        for folder in epic_folders:
            folder_path = Path(folder)
            if not folder_path.is_dir() or folder_path.name.startswith("."):
                continue
            epic_name = folder_path.name
            tasks_file = folder_path / "tasks.md"
            if tasks_file.exists():
                try:
                    content = tasks_file.read_text(encoding="utf-8", errors="ignore")
                    done = len(re.findall(r'- \[[xX]\]', content))
                    all_t = len(re.findall(r'- \[[ xX]\]', content))
                    pct = (done / all_t * 100) if all_t > 0 else 0
                    stats[epic_name] = {
                        "done": done,
                        "total": all_t,
                        "percent": round(pct, 1),
                        "status": "Hoàn tất (100%)" if done == all_t and all_t > 0 else f"Đang thực hiện ({pct:.1f}%)"
                    }
                    total_done += done
                    total_tasks += all_t
                except Exception as e:
                    stats[epic_name] = {"done": 0, "total": 0, "percent": 0, "status": f"Lỗi đọc file: {e}"}

    overall_pct = (total_done / total_tasks * 100) if total_tasks > 0 else 0
    return {
        "epics": stats,
        "total_done": total_done,
        "total_tasks": total_tasks,
        "overall_percent": round(overall_pct, 1)
    }

def generate_report_html(stats):
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    overall = stats["overall_percent"]
    total_done = stats["total_done"]
    total_tasks = stats["total_tasks"]

    rows = ""
    for epic, data in stats["epics"].items():
        done = data["done"]
        total = data["total"]
        pct = data["percent"]
        color = "#10b981" if pct == 100 else ("#3b82f6" if pct >= 50 else "#f59e0b")
        rows += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-weight: 600;">{epic}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: center;">{done}/{total}</td>
            <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; text-align: right; color: {color}; font-weight: 700;">{pct}%</td>
            <td style="padding: 10px; border-bottom: 1px solid #e5e7eb; font-size: 13px;">{data['status']}</td>
        </tr>
        """

    html = f"""
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f9fafb; padding: 20px;">
        <div style="max-width: 650px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e5e7eb; padding: 24px;">
            <h2 style="color: #1e293b; margin-top: 0;">📊 Báo Cáo Tiến Độ Dự Án — PO/PM Agent</h2>
            <p style="color: #64748b; font-size: 14px;">Thời gian tạo: {now_str}</p>
            
            <div style="background: #f1f5f9; padding: 16px; border-radius: 6px; margin: 20px 0;">
                <div style="font-size: 14px; color: #475569;">Tiến độ tổng thể:</div>
                <div style="font-size: 28px; font-weight: 800; color: #0f172a; margin: 4px 0;">{overall}%</div>
                <div style="font-size: 13px; color: #64748b;">Đã hoàn thành {total_done} trên tổng số {total_tasks} công việc.</div>
            </div>

            <table style="width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 14px;">
                <thead>
                    <tr style="background-color: #f8fafc; color: #475569; text-align: left;">
                        <th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">Phân Hệ / Epic</th>
                        <th style="padding: 10px; border-bottom: 2px solid #e2e8f0; text-align: center;">Tasks</th>
                        <th style="padding: 10px; border-bottom: 2px solid #e2e8f0; text-align: right;">%</th>
                        <th style="padding: 10px; border-bottom: 2px solid #e2e8f0;">Trạng Thái</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
            
            <p style="margin-top: 25px; font-size: 12px; color: #94a3b8; text-align: center;">
                Báo cáo tự động được tạo bởi TC IT Agent Enterprise Framework.
            </p>
        </div>
    </body>
    </html>
    """
    return html

def send_email(html_content, env_config):
    if not env_config.get("SMTP_USER") or not env_config.get("SMTP_PASSWORD"):
        print("⚠️ Chưa cấu hình SMTP_USER/SMTP_PASSWORD trong .env.email. Bỏ qua gửi email.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📊 [TC IT Agent] Báo Cáo Tiến Độ Dự Án - {datetime.now().strftime('%d/%m/%Y')}"
    msg["From"] = f"{env_config['SMTP_FROM_NAME']} <{env_config['SMTP_FROM']}>"
    msg["To"] = env_config["MAIL_TO"]

    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP(env_config["SMTP_HOST"], env_config["SMTP_PORT"])
        server.starttls()
        server.login(env_config["SMTP_USER"], env_config["SMTP_PASSWORD"])
        server.sendmail(env_config["SMTP_FROM"], [env_config["MAIL_TO"]], msg.as_string())
        server.quit()
        print(f"✅ Đã gửi báo cáo tiến độ thành công tới: {env_config['MAIL_TO']}")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi gửi email: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Send PO/PM Progress Report.")
    parser.add_argument("--dry-run", action="store_true", help="Chỉ in báo cáo ra màn hình, không gửi email")
    args = parser.parse_args()

    stats = get_task_statistics()
    print(f"\n==================================================")
    print(f"📊 TỔNG HỢP TIẾN ĐỘ DỰ ÁN: {stats['overall_percent']}% ({stats['total_done']}/{stats['total_tasks']} tasks)")
    print(f"==================================================")
    for epic, d in stats["epics"].items():
        print(f" - {epic:25}: {d['done']:2}/{d['total']:2} tasks ({d['percent']:5.1f}%) -> {d['status']}")
    print(f"==================================================\n")

    html = generate_report_html(stats)
    if args.dry_run:
        print("ℹ️  Chế độ dry-run: Đã tạo báo cáo HTML thành công.")
        return

    env_config = load_email_env()
    send_email(html, env_config)

if __name__ == "__main__":
    main()
