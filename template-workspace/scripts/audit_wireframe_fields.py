#!/usr/bin/env python3
"""
AUDIT WIREFRAME FIELDS — Chốt chặn cơ học kiểm tra độ phủ trường biểu mẫu (Wireframe HTML vs Component Code)
Framework: TC IT Agent Enterprise
Mục tiêu: Ngăn chặn Agent cắt xén trường form, làm ẩu để qua bài test API.
Quy tắc: So sánh số lượng interactive controls (input, select, textarea) giữa file HTML Basic Design gốc
và file Component Frontend tương ứng. Nếu tỷ lệ bao phủ < 80%, trả về mã lỗi 1 để chặn Gate 3 & Gate 4.
"""

import sys
import os
import re
import argparse

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

def count_wireframe_fields(html_path):
    if not os.path.isfile(html_path):
        return None, f"File wireframe không tồn tại: {html_path}"
    
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if BeautifulSoup:
        soup = BeautifulSoup(content, 'html.parser')
        inputs = soup.find_all('input')
        selects = soup.find_all('select')
        textareas = soup.find_all('textarea')
        active_inputs = [inp for inp in inputs if inp.get('type') != 'hidden']
        total = len(active_inputs) + len(selects) + len(textareas)
        return total, []
    else:
        # Fallback regex nếu chưa cài bs4
        inputs = re.findall(r'<input\b(?![^>]*type=[\'"]hidden[\'"])', content, re.IGNORECASE)
        selects = re.findall(r'<select\b', content, re.IGNORECASE)
        textareas = re.findall(r'<textarea\b', content, re.IGNORECASE)
        total = len(inputs) + len(selects) + len(textareas)
        return total, []

def count_component_fields(comp_path):
    if not os.path.isfile(comp_path):
        return None, f"File component không tồn tại: {comp_path}"
    
    with open(comp_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    patterns = [
        r'<input\b',
        r'<select\b',
        r'<textarea\b',
        r'<FormField\b',
        r'<TextInput\b',
        r'<Select\b',
        r'<Textarea\b',
        r'<Radio\b',
        r'<Checkbox\b',
        r'<Switch\b'
    ]
    
    matches = 0
    for p in patterns:
        found = re.findall(p, content, re.IGNORECASE)
        matches += len(found)
    
    return matches, content

def audit_pair(html_path, comp_path, min_coverage=80.0):
    print(f"\n======================================================================")
    print(f"🔍 KIỂM TOÁN ĐỘ PHỦ TRƯỜNG BIỂU MẪU: WIREFRAME vs FRONTEND COMPONENT")
    print(f"======================================================================")
    print(f"📄 Wireframe HTML:    {html_path}")
    print(f"⚛️  Frontend Component: {comp_path}")
    
    wf_count, wf_err = count_wireframe_fields(html_path)
    if wf_count is None:
        print(f"❌ LỖI: {wf_err}")
        return False
        
    comp_count, comp_err = count_component_fields(comp_path)
    if comp_count is None:
        print(f"❌ LỖI: {comp_err}")
        return False
        
    if wf_count == 0:
        print(f"ℹ️  Wireframe không có trường input/select/textarea tương tác.")
        return True
        
    coverage = (comp_count / wf_count) * 100.0
    print(f"📊 Thống kê:")
    print(f"   - Số controls trên Wireframe gốc: {wf_count}")
    print(f"   - Số controls trên Component:      {comp_count}")
    print(f"   - Tỷ lệ bao phủ (Coverage):        {coverage:.1f}% (Ngưỡng tối thiểu: {min_coverage}%)")
    
    if coverage < min_coverage:
        print(f"❌ [GATE FAIL] Tỷ lệ bao phủ trường không đạt yêu cầu (< {min_coverage}%)!")
        print(f"   CẢNH BÁO: Phát hiện biểu mẫu bị cắt xén, thiếu trường so với Wireframe gốc.")
        print(f"   Dev bắt buộc phải hoàn thiện đầy đủ các trường trước khi bàn giao sang QC.")
        return False
    else:
        print(f"✅ [GATE PASS] Biểu mẫu đáp ứng chuẩn độ phủ trường (>= {min_coverage}%).")
        return True

def main():
    parser = argparse.ArgumentParser(description="Audit interactive fields coverage between Wireframe HTML and Component code.")
    parser.add_argument("--wireframe", help="Đường dẫn file HTML Wireframe")
    parser.add_argument("--component", "--tsx", dest="component", help="Đường dẫn file Component (TSX, JSX, Vue, v.v.)")
    parser.add_argument("--min-coverage", type=float, default=80.0, help="Tỷ lệ bao phủ tối thiểu (%)")
    
    args = parser.parse_args()
    
    if args.wireframe and args.component:
        success = audit_pair(args.wireframe, args.component, args.min_coverage)
        sys.exit(0 if success else 1)
        
    print("ℹ️  Chạy audit_wireframe_fields với tham số --wireframe <file.html> --component <file.tsx> để kiểm tra cụ thể.")
    sys.exit(0)

if __name__ == "__main__":
    main()
