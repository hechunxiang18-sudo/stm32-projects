#!/usr/bin/env python3
"""修复所有 HTML 文件中未渲染的 Python 模板变量"""
import os, re

BASE = "E:/STM32/stm32-projects"
WECHAT = "HE-8473"

html_files = []
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

print(f"共找到 {len(html_files)} 个 HTML 文件")

fixed_count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '{rel}' not in content and '{back_path}' not in content and "meta['nav_title']" not in content and '{WECHAT_QR}' not in content:
        continue  # 无需修复

    rel = os.path.relpath(BASE, os.path.dirname(filepath)).replace("\\", "/")

    # 提取导航标题
    titles = re.findall(r'class="detail-nav-title">(.*?)</span>', content)
    nav_title = titles[0] if titles else "项目"

    content = content.replace('{WECHAT_QR}', WECHAT)
    content = content.replace('{back_path}', rel)
    content = content.replace('{rel}', rel)
    content = content.replace("{meta['nav_title']}", nav_title)
    content = content.replace('{meta["nav_title"]}', nav_title)

    fixed_count += 1
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"已修复 {fixed_count} 个文件")

# 验证还有没有残留
remaining = 0
for root, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith(".html"):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as fh:
                c = fh.read()
            if '{back_path}' in c or '{WECHAT_QR}' in c or "{meta['" in c or '{rel}' in c:
                remaining += 1
                print(f"  残留: {os.path.relpath(fp, BASE)}")

print(f"残留文件: {remaining}")
