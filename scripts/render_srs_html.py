import re
import markdown

input_path = "Specification/SRS/SRS-001-CORE-IAM.md"
output_path = "Specification/SRS/SRS-001-CORE-IAM.html"

with open(input_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# Replace mermaid code blocks with <div class="mermaid">...</div>
def replace_mermaid(match):
    code = match.group(1).strip()
    return f'\n<div class="mermaid bg-slate-900/90 p-6 rounded-2xl border border-slate-700/80 my-6 shadow-inner text-center overflow-x-auto">\n{code}\n</div>\n'

md_processed = re.sub(r"```mermaid\s*\n(.*?)```", replace_mermaid, md_content, flags=re.DOTALL)

# Convert Markdown to HTML
html_body = markdown.markdown(
    md_processed,
    extensions=["tables", "fenced_code", "toc", "nl2br", "sane_lists"]
)

# Badge highlighter for tags like [VERIFIED], [CONFIRMED], [PROPOSAL], [REQ-*], [BR-*], etc.
def highlight_tags(html):
    html = re.sub(
        r'\[(VERIFIED|CONFIRMED|PROPOSAL|MỚI THIẾT KẾ[^\]]*)\]',
        r'<span class="badge bg-blue-500/15 text-blue-300 border border-blue-500/30 px-2 py-0.5 rounded text-xs font-semibold">\1</span>',
        html
    )
    html = re.sub(
        r'\[(REQ-[A-Z0-9-]+)\]',
        r'<span class="badge bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded text-xs font-semibold">\1</span>',
        html
    )
    html = re.sub(
        r'\[(BR-[A-Z0-9-]+)\]',
        r'<span class="badge bg-amber-500/15 text-amber-300 border border-amber-500/30 px-2 py-0.5 rounded text-xs font-semibold">\1</span>',
        html
    )
    html = re.sub(
        r'\[(DB-[A-Z0-9-]+)\]',
        r'<span class="badge bg-purple-500/15 text-purple-300 border border-purple-500/30 px-2 py-0.5 rounded text-xs font-semibold">\1</span>',
        html
    )
    html = re.sub(
        r'\[(UI-[A-Z0-9-]+)\]',
        r'<span class="badge bg-cyan-500/15 text-cyan-300 border border-cyan-500/30 px-2 py-0.5 rounded text-xs font-semibold">\1</span>',
        html
    )
    html = re.sub(
        r'\[(API-[A-Z0-9-]+)\]',
        r'<span class="badge bg-rose-500/15 text-rose-300 border border-rose-500/30 px-2 py-0.5 rounded text-xs font-semibold">\1</span>',
        html
    )
    html = re.sub(
        r'\[(NFR-[A-Z0-9-]+)\]',
        r'<span class="badge bg-teal-500/15 text-teal-300 border border-teal-500/30 px-2 py-0.5 rounded text-xs font-semibold">\1</span>',
        html
    )
    return html

html_body = highlight_tags(html_body)

html_template = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SRS-001-CORE-IAM: Nền Tảng Quản Trị Định Danh & Phân Quyền Đa Tầng</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", function() {{
      mermaid.initialize({{
        startOnLoad: true,
        theme: 'dark',
        themeVariables: {{
          darkMode: true,
          background: '#0f172a',
          primaryColor: '#2563eb',
          primaryTextColor: '#f8fafc',
          primaryBorderColor: '#3b82f6',
          lineColor: '#60a5fa',
          secondaryColor: '#059669',
          tertiaryColor: '#1e293b'
        }}
      }});
    }});
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    body {{ font-family: 'Inter', sans-serif; }}
    code, pre {{ font-family: 'JetBrains Mono', monospace; }}
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #020617; }}
    ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
    
    table {{ width: 100%; border-collapse: separate; border-spacing: 0; margin: 1.5rem 0; font-size: 0.875rem; border: 1px solid #334155; border-radius: 0.75rem; overflow: hidden; }}
    th, td {{ padding: 0.75rem 1rem; text-align: left; vertical-align: top; border-bottom: 1px solid #1e293b; border-right: 1px solid #1e293b; }}
    th:last-child, td:last-child {{ border-right: none; }}
    tr:last-child td {{ border-bottom: none; }}
    th {{ background-color: #0f172a; color: #93c5fd; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em; }}
    tr:nth-child(even) {{ background-color: rgba(15, 23, 42, 0.4); }}
    tr:hover {{ background-color: rgba(30, 41, 59, 0.6); transition: background-color 0.15s ease; }}
    
    code {{ background-color: #1e293b; color: #38bdf8; padding: 0.15rem 0.4rem; border-radius: 0.35rem; font-size: 0.85em; }}
    pre {{ background-color: #020617 !important; border: 1px solid #334155; border-radius: 0.75rem; padding: 1.25rem; overflow-x: auto; }}
    pre code {{ background: transparent; padding: 0; color: #e2e8f0; }}
    
    h1 {{ font-size: 2rem; font-weight: 800; color: #f8fafc; margin-top: 1.5rem; margin-bottom: 0.75rem; border-bottom: 2px solid #3b82f6; padding-bottom: 0.75rem; letter-spacing: -0.025em; }}
    h2 {{ font-size: 1.5rem; font-weight: 700; color: #60a5fa; margin-top: 2.5rem; margin-bottom: 1rem; border-bottom: 1px solid #334155; padding-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }}
    h3 {{ font-size: 1.2rem; font-weight: 600; color: #34d399; margin-top: 1.75rem; margin-bottom: 0.75rem; }}
    h4 {{ font-size: 1.05rem; font-weight: 600; color: #fbbf24; margin-top: 1.25rem; margin-bottom: 0.5rem; }}
    
    blockquote {{ border-left: 4px solid #3b82f6; background-color: rgba(15, 23, 42, 0.7); padding: 1rem 1.25rem; border-radius: 0 0.5rem 0.5rem 0; margin: 1.25rem 0; color: #cbd5e1; }}
    ul, ol {{ padding-left: 1.5rem; margin: 0.75rem 0; }}
    li {{ margin: 0.35rem 0; color: #cbd5e1; }}
    p {{ line-height: 1.7; margin: 0.75rem 0; color: #cbd5e1; }}
    strong {{ color: #f8fafc; font-weight: 600; }}
    hr {{ border-color: #1e293b; margin: 2.5rem 0; }}
    
    @media print {{
      body {{ background: #fff !important; color: #000 !important; }}
      main {{ box-shadow: none !important; border: none !important; max-width: 100% !important; padding: 0 !important; }}
      .sticky {{ display: none !important; }}
      table {{ border-color: #999 !important; }}
      th, td {{ border-color: #999 !important; color: #000 !important; }}
      th {{ background: #eee !important; }}
    }}
  </style>
</head>
<body class="bg-[#020617] text-slate-100 min-h-screen p-4 md:p-8 antialiased">

  <!-- Floating Sticky Navigation & Control Bar -->
  <div class="max-w-6xl mx-auto mb-6 flex flex-col md:flex-row items-center justify-between bg-slate-900/90 backdrop-blur-md border border-slate-800 p-4 rounded-2xl sticky top-3 z-50 shadow-2xl">
    <div class="flex items-center gap-3">
      <span class="flex h-3 w-3 relative">
        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
        <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
      </span>
      <div>
        <div class="text-[11px] text-blue-400 font-semibold uppercase tracking-wider">Hệ Thống NacenTech • Báo Cáo SRS 7 Mục</div>
        <div class="text-sm md:text-base font-bold text-white flex items-center gap-2">
          SRS-001-CORE-IAM: Nền Tảng Quản Trị Định Danh & Phân Quyền Đa Tầng
        </div>
      </div>
    </div>
    
    <div class="flex items-center gap-2 mt-3 md:mt-0">
      <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1.5">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
        HỘI TỤ (CONVERGED 100%)
      </span>
      <span class="bg-blue-500/10 text-blue-400 border border-blue-500/30 px-2.5 py-1 rounded-full text-xs font-bold">
        v1.0.0
      </span>
      <button onclick="window.print()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold px-3 py-1.5 rounded-xl border border-slate-700 transition flex items-center gap-1.5 shadow-sm">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H7a2 2 0 00-2 2v4h10z"></path></svg>
        In / Xuất PDF
      </button>
    </div>
  </div>

  <!-- Document Card Container -->
  <main class="max-w-6xl mx-auto bg-slate-900/80 border border-slate-800 rounded-3xl p-6 md:p-14 shadow-2xl relative overflow-hidden">
    <div class="absolute -right-32 -top-32 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute -left-32 -bottom-32 w-[500px] h-[500px] bg-emerald-600/10 rounded-full blur-3xl pointer-events-none"></div>

    <div class="relative z-10">
      {html_body}
    </div>

    <footer class="mt-20 pt-8 border-t border-slate-800/80 text-center text-xs text-slate-500 flex flex-col md:flex-row justify-between items-center gap-3 relative z-10">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-blue-500"></span>
        Hệ sinh thái Quản trị Công nghệ & E-Learning NacenTech • Viện NacenTech
      </div>
      <div>Bản quyền tài liệu nghiệp vụ © 2026 • Biên soạn bởi BA SRS Copilot (BMad Method)</div>
    </footer>
  </main>

</body>
</html>
"""

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print("SUCCESS: Rendered", output_path)
