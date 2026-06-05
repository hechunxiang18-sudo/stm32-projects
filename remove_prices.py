#!/usr/bin/env python3
"""移除所有项目中的成本信息和价格"""
import os, re

BASE = "E:/STM32/stm32-projects"
stats = {"overview_cost": 0, "bom_price": 0, "bom_total": 0}

for root, dirs, files in os.walk(BASE):
    for f in files:
        if not f.endswith(".html"):
            continue
        filepath = os.path.join(root, f)
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()

        original = content

        # 1. 移除所有"成本XX元"、"约XX元"这样的成本描述（在概述段落中）
        cost_patterns = [
            r'，全套硬件成本可控在[^。]*。',
            r'，全套硬件成本[^。]*。',
            r'，成本可控[^。]*。',
            r'，全套自制成本约[^。]*。',
            r'成本控制在[^。]*。',
            r'，一套系统可管理[^。]*。',
        ]
        for p in cost_patterns:
            content = re.sub(p, '。', content)

        # 2. BOM 表中移除价格列
        # 查找 BOM 表格
        if '<th>参考价</th>' in content:
            # 移除 thead 中的参考价 th
            content = content.replace('<th>参考价</th>', '')
            # 移除 tbody 中每行的最后一个 td（价格）
            # 匹配 <tr>...5个td...<td>价格</td></tr> → <tr>...5个td...</tr>
            content = re.sub(
                r'(<tr>\s*(?:<td>[^<]*</td>\s*){5})<td>[^<]*</td>\s*</tr>',
                r'\1</tr>',
                content
            )
            stats["bom_price"] += 1

        # 3. 移除 BOM 总计行
        if 'bom-total' in content:
            content = re.sub(r'<p class="bom-total">[^<]*<strong>[^<]*</strong>[^<]*</p>\s*', '', content)
            stats["bom_total"] += 1

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as fh:
                fh.write(content)
            stats["overview_cost"] += 1

print(f"处理完成！")
print(f"  - 移除成本描述的页面: {stats['overview_cost']} 个")
print(f"  - 移除价格列的 BOM 表: {stats['bom_price']} 个")
print(f"  - 移除总计行的页面: {stats['bom_total']} 个")
