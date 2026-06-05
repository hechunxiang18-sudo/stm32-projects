#!/usr/bin/env python3
"""
拆分所有项目详情页为多页结构。
每个项目变成文件夹，内含 index.html(导航页) + 各板块独立页面。
"""
import os, re, glob

BASE = "E:/STM32/stm32-projects"

# 板块映射：section_id → (文件名, 显示名称, 图标)
SECTION_MAP = [
    ("overview",   "overview.html",   "项目概述",   "&#128196;"),
    ("features",   "features.html",   "功能特性",   "&#9889;"),
    ("block",      "block.html",      "系统框图",   "&#128200;"),
    ("bom",        "bom.html",        "元器件清单", "&#128221;"),
    ("pinout",     "pinout.html",     "引脚连接",   "&#128279;"),
    ("schematic",  "schematic.html",  "电路原理图", "&#9881;"),
    ("code",       "code.html",       "核心代码",   "&#128187;"),
]

def extract_section(content, section_id):
    """提取指定 section 块的内容"""
    pattern = rf'<section id="{section_id}"[^>]*>.*?</section>'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(0) if match else None

def extract_meta(content):
    """提取 Hero 区域的元数据"""
    title_m = re.search(r'<h1>(.*?)</h1>', content)
    title = title_m.group(1) if title_m else "项目"

    desc_m = re.search(r'class="detail-hero-sub">(.*?)</p>', content)
    desc = desc_m.group(1) if desc_m else ""

    icon_m = re.search(r'class="detail-hero-icon">(.*?)</div>', content)
    icon = icon_m.group(1) if icon_m else "&#9726;"

    hero_style_m = re.search(r'<header class="detail-hero" style="(.*?)">', content)
    hero_style = hero_style_m.group(1) if hero_style_m else "background:linear-gradient(135deg, #0a1628 0%, #1a3a6b 40%, #2d1b69 100%);"

    tags_m = re.findall(r'<span>(.*?)</span>', content.split('class="detail-hero-tags"')[1].split('</div>')[0]) if 'class="detail-hero-tags"' in content else []
    tags = tags_m

    nav_title_m = re.search(r'class="detail-nav-title">(.*?)</span>', content)
    nav_title = nav_title_m.group(1) if nav_title_m else title

    return {"title": title, "desc": desc, "icon": icon, "hero_style": hero_style, "tags": tags, "nav_title": nav_title}

def create_section_page(project_dir, section_id, section_html, meta, back_path):
    """生成板块独立页面"""
    # 板块名称查找
    section_name = section_id
    for sid, fn, name, _ in SECTION_MAP:
        if sid == section_id:
            section_name = name
            break

    # 板块导航链接
    nav_links = ""
    for sid, fn, name, _ in SECTION_MAP:
        if sid == section_id:
            nav_links += f'              <span class="sec-nav-item active">{name}</span>\n'
        else:
            nav_links += f'              <a href="{fn}" class="sec-nav-item">{name}</a>\n'

    page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{section_name} - {meta['title']}</title>
  <meta name="description" content="{meta['desc']}">
  <link rel="stylesheet" href="{back_path}style.css">
</head>
<body class="detail-page">
  <nav class="detail-nav">
    <a href="{back_path}index.html" class="back-link">&larr; 返回项目列表</a>
    <span class="detail-nav-title">{meta['nav_title']} / {section_name}</span>
  </nav>

  <header class="detail-hero" style="{meta['hero_style']}">
    <div class="detail-hero-content">
      <div class="detail-hero-icon">{meta['icon']}</div>
      <h1>{meta['title']}</h1>
      <p class="detail-hero-sub">{meta['desc']}</p>
      <div class="detail-hero-tags">
""" + '\n'.join(f'        <span>{t}</span>' for t in meta['tags']) + """
      </div>
    </div>
  </header>

  <div class="container detail-container">
    <!-- ===== 板块导航 ===== -->
    <nav class="sec-nav">
""" + nav_links + """
    </nav>

    <!-- ===== 内容 ===== -->
    """ + section_html + """
  </div>

  <footer class="footer">
    <p><a href="{back_path}index.html" style="color:var(--text-muted);">&larr; 返回项目列表</a> &nbsp;|&nbsp; <strong>{meta['nav_title']}</strong></p>
  </footer>
</body>
</html>"""
    filepath = os.path.join(project_dir, f"{section_id}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page)
    return f"{section_id}.html"

def create_project_index(project_dir, meta, available_sections, back_path):
    """生成项目首页（导航卡片式）"""
    cards = ""
    for sid, fn, name, icon in SECTION_MAP:
        if sid in available_sections:
            cards += f"""      <a href="{fn}" class="proj-nav-card">
        <div class="pnc-icon">{icon}</div>
        <h3>{name}</h3>
        <span class="pnc-arrow">&rarr;</span>
      </a>
"""

    index = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['desc']}">
  <link rel="stylesheet" href="{back_path}style.css">
</head>
<body class="detail-page">
  <nav class="detail-nav">
    <a href="{back_path}index.html" class="back-link">&larr; 返回项目列表</a>
    <span class="detail-nav-title">{meta['nav_title']}</span>
  </nav>

  <header class="detail-hero" style="{meta['hero_style']}">
    <div class="detail-hero-content">
      <div class="detail-hero-icon">{meta['icon']}</div>
      <h1>{meta['title']}</h1>
      <p class="detail-hero-sub">{meta['desc']}</p>
      <div class="detail-hero-tags">
""" + '\n'.join(f'        <span>{t}</span>' for t in meta['tags']) + """
      </div>
    </div>
  </header>

  <div class="container detail-container">
    <div class="proj-nav-section">
      <h2 class="proj-nav-heading">选择查看板块</h2>
      <div class="proj-nav-grid">
""" + cards + """      </div>
    </div>
  </div>

  <footer class="footer">
    <p><a href="{back_path}index.html" style="color:var(--text-muted);">&larr; 返回项目列表</a> &nbsp;|&nbsp; <strong>{meta['nav_title']}</strong></p>
  </footer>
</body>
</html>"""
    with open(os.path.join(project_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index)

def process_project(filepath, category):
    """处理单个项目文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    name_noext = filename.replace('.html', '')
    meta = extract_meta(content)

    # 计算 back_path
    if category:
        back_path = "../../"
    else:
        back_path = "../"

    # 创建项目文件夹
    if category:
        project_dir = os.path.join(BASE, category, name_noext)
    else:
        project_dir = os.path.join(BASE, name_noext)
    os.makedirs(project_dir, exist_ok=True)

    # 提取各板块
    available = []
    for sid, fn, name, _ in SECTION_MAP:
        sec_html = extract_section(content, sid)
        if sec_html:
            create_section_page(project_dir, sid, sec_html, meta, back_path)
            available.append(sid)

    # 生成项目首页
    create_project_index(project_dir, meta, available, back_path)

    # 返回新旧路径映射（用于更新首页链接）
    old_path = f"{category}/{filename}" if category else filename
    new_path = f"{category}/{name_noext}/index.html" if category else f"{name_noext}/index.html"
    return old_path, new_path

def main():
    # 处理所有项目
    category_dirs = ["iot", "security", "robot", "sensor", "health", "vehicle", "life"]
    mappings = []

    for cat in category_dirs:
        cat_dir = os.path.join(BASE, cat)
        if not os.path.isdir(cat_dir):
            continue
        for f in sorted(glob.glob(os.path.join(cat_dir, "*.html"))):
            print(f"Processing: {f}")
            old, new = process_project(f, cat)
            mappings.append((old, new))
            print(f"  {old} -> {new}")

    # 更新首页链接
    index_path = os.path.join(BASE, "index.html")
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    for old, new in mappings:
        # 只替换 href 中的路径
        index_content = index_content.replace(f'href="{old}"', f'href="{new}"')

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

    print(f"\nDone! {len(mappings)} projects processed.")

if __name__ == '__main__':
    main()
