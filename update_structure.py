#!/usr/bin/env python3
"""
更新所有项目：
1. 板块排序：概述→功能→框图→BOM→引脚→电路原理图(下载)→核心代码(下载)
2. 电路原理图和核心代码改为点击下载
3. 添加作者微信
"""
import os, re, glob

BASE = "E:/STM32/stm32-projects"
WECHAT_QR = "HE-8473"  # 替换为你的微信号

# 新板块顺序（schematic 和 code 标记为 download）
NEW_SECTIONS = [
    ("overview",   "overview.html",   "项目概述",     "&#128196;", False),
    ("features",   "features.html",   "功能特性",     "&#9889;",   False),
    ("block",      "block.html",      "系统框图",     "&#128200;", False),
    ("bom",        "bom.html",        "元器件清单",   "&#128221;", False),
    ("pinout",     "pinout.html",     "引脚连接",     "&#128279;", False),
    ("schematic",  "schematic.html",  "电路原理图",   "&#9881;",   True),
    ("code",       "code.html",       "核心代码",     "&#128187;", True),
]

SEC_IDS = [s[0] for s in NEW_SECTIONS]

def get_project_dirs():
    """获取所有项目文件夹"""
    dirs = []
    for cat in ["iot", "security", "robot", "sensor", "health", "vehicle", "life"]:
        cat_dir = os.path.join(BASE, cat)
        if not os.path.isdir(cat_dir):
            continue
        for d in sorted(glob.glob(os.path.join(cat_dir, "project-*"))):
            if os.path.isdir(d):
                dirs.append(d)
    return dirs

def extract_meta_from_index(index_html):
    """从项目导航页提取元数据"""
    meta = {}
    m = re.search(r'<h1>(.*?)</h1>', index_html)
    meta['title'] = m.group(1) if m else "项目"
    m = re.search(r'class="detail-hero-sub">(.*?)</p>', index_html)
    meta['desc'] = m.group(1) if m else ""
    m = re.search(r'class="detail-hero-icon">(.*?)</div>', index_html)
    meta['icon'] = m.group(1) if m else "&#9726;"
    m = re.search(r'<header class="detail-hero" style="(.*?)">', index_html)
    meta['hero_style'] = m.group(1) if m else ""
    m = re.search(r'class="detail-nav-title">(.*?)</span>', index_html)
    meta['nav_title'] = m.group(1) if m else meta['title']

    tags_match = re.search(r'class="detail-hero-tags">(.*?)</div>', index_html, re.DOTALL)
    meta['tags'] = re.findall(r'<span>(.*?)</span>', tags_match.group(1)) if tags_match else []
    return meta

def update_project_index(project_dir):
    """重写项目导航页"""
    filepath = os.path.join(project_dir, "index.html")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    meta = extract_meta_from_index(content)

    # 检测哪些板块存在
    available = []
    for sid, fn, name, icon, is_dl in NEW_SECTIONS:
        if os.path.exists(os.path.join(project_dir, fn)):
            available.append((sid, fn, name, icon, is_dl))

    # 拼导航卡片
    cards = ""
    for sid, fn, name, icon, is_dl in available:
        if is_dl:
            cards += f"""      <a href="{fn}" class="proj-nav-card card-download">
        <div class="pnc-icon">{icon}</div>
        <h3>{name}</h3>
        <span class="pnc-badge">&#128229; 下载</span>
      </a>
"""
        else:
            cards += f"""      <a href="{fn}" class="proj-nav-card">
        <div class="pnc-icon">{icon}</div>
        <h3>{name}</h3>
        <span class="pnc-arrow">&rarr;</span>
      </a>
"""

    # 计算 back_path
    rel = os.path.relpath(BASE, project_dir).replace("\\", "/")

    index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta['title']}</title>
  <meta name="description" content="{meta['desc']}">
  <link rel="stylesheet" href="{rel}/style.css">
</head>
<body class="detail-page">
  <nav class="detail-nav">
    <a href="{rel}/index.html" class="back-link">&larr; 返回项目列表</a>
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

    <!-- ===== 作者微信 ===== -->
    <div class="wechat-section">
      <div class="wechat-box">
        <div class="wechat-icon">&#128172;</div>
        <div class="wechat-text">
          <h3>需要技术支持？</h3>
          <p>项目定制、技术咨询、问题解答，欢迎添加作者微信交流</p>
          <div class="wechat-id">
            <span class="wechat-label">微信号：</span>
            <span class="wechat-value">{WECHAT_QR}</span>
            <button class="wechat-copy-btn" onclick="copyWechat()">复制</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <footer class="footer">
    <p><a href="{rel}/index.html" style="color:var(--text-muted);">&larr; 返回项目列表</a> &nbsp;|&nbsp; <strong>{meta['nav_title']}</strong></p>
    <p class="footer-sub" style="margin-top:6px;">作者微信：{WECHAT_QR} &nbsp;|&nbsp; 欢迎交流嵌入式开发</p>
  </footer>

  <script>
  function copyWechat() {{
    navigator.clipboard.writeText('{WECHAT_QR}').then(() => {{
      const btn = document.querySelector('.wechat-copy-btn');
      btn.textContent = '已复制';
      setTimeout(() => {{ btn.textContent = '复制'; }}, 2000);
    }});
  }}
  </script>
</body>
</html>"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"  Updated index: {project_dir}")

def update_section_page(filepath, back_rel):
    """更新板块页面：修正导航排序、添加作者微信"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 获取当前板块ID
    current_id = None
    for sid in SEC_IDS:
        if f'/{sid}.html' in filepath or f'\\{sid}.html' in filepath:
            current_id = sid
            break
    if not current_id:
        return

    # 生成新排序的 sec-nav
    nav_items = ""
    for sid, fn, name, icon, is_dl in NEW_SECTIONS:
        page_exists = os.path.exists(os.path.join(os.path.dirname(filepath), fn))
        if not page_exists:
            continue
        if sid == current_id:
            nav_items += f'              <span class="sec-nav-item active">{name}</span>\n'
        elif is_dl:
            nav_items += f'              <a href="{fn}" class="sec-nav-item item-download">{name} &#128229;</a>\n'
        else:
            nav_items += f'              <a href="{fn}" class="sec-nav-item">{name}</a>\n'

    # 替换 sec-nav
    content = re.sub(
        r'<nav class="sec-nav">.*?</nav>',
        f'<nav class="sec-nav">\n{nav_items}            </nav>',
        content, flags=re.DOTALL
    )

    # 如果是下载板块（schematic/code），添加下载按钮
    is_download = False
    for sid, fn, name, icon, is_dl in NEW_SECTIONS:
        if sid == current_id and is_dl:
            is_download = True
            break

    if is_download:
        # 在内容后插入下载按钮
        dl_type = "原理图" if current_id == "schematic" else "源代码"
        dl_btn = f"""
  <div class="download-section">
    <div class="download-box">
      <div class="download-icon">&#128229;</div>
      <h3>下载{dl_type}</h3>
      <p>点击下方按钮下载本项目的{dl_type}文件</p>
      <button class="download-btn" onclick="triggerDownload('{current_id}')">
        &#128190; 下载{dl_type}
      </button>
    </div>
  </div>"""

        # 在 footer 前插入
        content = content.replace('<footer class="footer">', dl_btn + '\n  <footer class="footer">')

        # 添加下载脚本（在 </body> 前）
        # 从原页面提取内容作为下载内容
        sec_match = re.search(r'<section[^>]*>.*?</section>', content, re.DOTALL)
        dl_content = ""
        if sec_match:
            dl_content = sec_match.group(0)
            dl_content = re.sub(r'<[^>]+>', '', dl_content)
            dl_content = dl_content[:500]  # 截取前500字符

        dl_script_content = dl_content.replace('`', '\\`').replace('$', '\\$')
        dl_script = f"""
  <script>
  function triggerDownload(type) {{
    var content = `{dl_script_content}`;
    var filename = type === 'schematic' ? 'schematic.txt' : 'source-code.c';
    var blob = new Blob([content], {{type: 'text/plain'}});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
  }}
  function copyWechat() {{
    navigator.clipboard.writeText('{WECHAT_QR}').then(function() {{
      var btn = document.querySelector('.wechat-copy-btn');
      if (btn) {{ btn.textContent = '已复制'; setTimeout(function() {{ btn.textContent = '复制'; }}, 2000); }}
    }});
  }}
  </script>"""
        content = content.replace('</body>', dl_script + '\n</body>')

    # 添加作者微信到 footer 前（如果还没有）
    if '作者微信' not in content:
        wechat_block = f"""
  <div class="wechat-section" style="margin-top:0; padding:0 20px;">
    <div class="wechat-box" style="margin-bottom:24px;">
      <div class="wechat-icon">&#128172;</div>
      <div class="wechat-text">
        <h3>需要技术支持？</h3>
        <p>项目定制、技术咨询、问题解答，欢迎添加作者微信交流</p>
        <div class="wechat-id">
          <span class="wechat-label">微信号：</span>
          <span class="wechat-value">{WECHAT_QR}</span>
          <button class="wechat-copy-btn" onclick="copyWechat()">复制</button>
        </div>
      </div>
    </div>
  </div>"""
        content = content.replace('<footer class="footer">', wechat_block + '\n  <footer class="footer">')

    # 修正 footer 中的微信信息
    if '作者微信' not in content:
        content = content.replace(
            '</p>\n    <p class="footer-sub',
            f'</p>\n    <p class="footer-sub" style="margin-top:6px;">作者微信：{WECHAT_QR} &nbsp;|&nbsp; 欢迎交流嵌入式开发</p>\n    <p class="footer-sub'
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # 1. 更新所有项目导航页
    print("=== 更新项目导航页 ===")
    for project_dir in get_project_dirs():
        update_project_index(project_dir)

    # 2. 更新所有板块页面
    print("\n=== 更新板块页面 ===")
    for project_dir in get_project_dirs():
        for sid, fn, name, icon, is_dl in NEW_SECTIONS:
            filepath = os.path.join(project_dir, fn)
            if os.path.exists(filepath):
                update_section_page(filepath, "")
                print(f"  Updated: {os.path.relpath(filepath, BASE)}")

    print(f"\n完成！共处理 {len(get_project_dirs())} 个项目。")

if __name__ == '__main__':
    main()
