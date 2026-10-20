#!/usr/bin/env python3
"""Xuất tài liệu nộp ra gốc repo: thay mã backlog `[[E11-I02]]` bằng số issue `#123` (GitHub tự tạo link).

Nguồn: plans/docs-src/*.md · bảng mã → số: plans/github-state.json (do github-backlog-sync.py ghi).
Dừng nếu còn mã chưa có số, để không bao giờ nộp tài liệu trỏ tới issue không tồn tại.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
state = json.load(open(os.path.join(ROOT, "plans", "github-state.json")))["issues"]
missing = set()


def to_number(match):
    key = match.group(1)
    if key not in state:
        missing.add(key)
        return match.group(0)
    return f"#{state[key]['number']}"


for src in sorted(glob.glob(os.path.join(ROOT, "plans", "docs-src", "*.md"))):
    text = re.sub(r"\[\[([A-Z]\d\d(?:-[IC]\d\d(?:-S\d+)?)?)\]\]", to_number, open(src).read())
    open(os.path.join(ROOT, os.path.basename(src)), "w").write(text)
    print(f"xuất {os.path.basename(src)}")

if missing:
    sys.exit(f"Còn {len(missing)} mã chưa có issue: {sorted(missing)[:10]}")
