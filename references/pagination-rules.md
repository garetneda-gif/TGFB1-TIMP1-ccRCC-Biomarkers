# 分页规则参考文档

> 从 SKILL.md 提取的分页核心内容（内容分析、HTML模板、分割策略、大图处理、验证检查点）

---

## 内容分析和分页规划

### 步骤3.1：内容分析和分页规划

**在生成 HTML 之前，必须先分析内容并规划分页：**

```python
# 1. 分析内容字数
def analyze_content(markdown_text):
    """分析每个章节的字数"""
    sections = {
        'INTRODUCTION': extract_section(markdown_text, 'INTRODUCTION'),
        'METHODS': extract_section(markdown_text, 'MATERIALS'),
        'RESULTS': extract_section(markdown_text, 'RESULTS'),
        'DISCUSSION': extract_section(markdown_text, 'DISCUSSION'),
    }

    for section, text in sections.items():
        word_count = len(re.findall(r'\b[a-zA-Z]+\b', text))
        print(f"{section}: {word_count} words")

    return sections

# 2. 规划分页（考虑图表占用空间）
# 注意：封面页不必独立成页，若封面/摘要区底部有剩余空间，应将正文接续填入
page_plan = {
    1: {  # 第1页：封面 + 正文流入
        'content': 'cover + Introduction开头（填满剩余空间）',
        'words': 200,  # Introduction开头约200词，视封面高度调整
        'space_used': '封面固定高度 + 剩余空间填入正文',
        'has_figures': False
    },
    2: {  # 第2页
        'content': 'INTRODUCTION续段 + METHODS 2.1开头',
        'words': 400,
        'space_used': '约180mm',  # 双栏，每栏约90mm
        'has_figures': False
    },
    3: {  # 第3页
        'content': 'METHODS 2.1续 + 2.2开头 + Figures 1-2',
        'words': 350,
        'space_used': '约160mm',
        'has_figures': True,  # Figures 1-2并排占约60mm
        'figures': ['Figure 1', 'Figure 2']
    },
    # ... 继续规划每一页
}

# 3. 验证分页计划（零留白容忍）
def validate_page_plan(page_plan):
    """验证每页内容不会溢出或留白（零留白原则：必须填满，不允许空白）"""
    MAX_HEIGHT = 252  # mm (297 - 25 - 20)

    for page_num, plan in page_plan.items():
        text_height = plan['words'] * 0.3  # 粗略估算：每词0.3mm
        fig_height = sum([60 if 'Figure' in f else 0 for f in plan.get('figures', [])])
        total = text_height + fig_height

        if total > MAX_HEIGHT:
            raise ValueError(f"第{page_num}页内容溢出！ ({total}mm > {MAX_HEIGHT}mm)")
        elif total < MAX_HEIGHT - 15:  # 阈值从30mm降低到15mm，更严格的零留白
            print(f"⚠️ 第{page_num}页留白过多！ ({MAX_HEIGHT - total}mm空白，必须填入更多内容)")
```

---

## HTML 模板和构建示例

### 步骤3.2：手动创建每个页面

**为每页手动创建独立的 `<div class="page">`**:

```python
def generate_page_2():
    """生成第2页 - INTRODUCTION前3段"""
    page_html = '''
<div class="page">
    <div class="page-header">WANG ET AL.</div>
    <div class="page-content two-column">
        <h1 class="section-title">1 INTRODUCTION</h1>
        <p>第1段内容...</p>
        <p>第2段内容...</p>
        <p>第3段内容...</p>
    </div>
    <div class="page-footer">2</div>
</div>
'''
    return page_html

def generate_page_3():
    """生成第3页 - INTRODUCTION后2段 + Figures 1-2"""
    page_html = '''
<div class="page">
    <div class="page-header">WANG ET AL.</div>
    <div class="page-content two-column">
        <p>第4段内容...</p>
        <p>第5段内容...</p>

        <!-- 并排图片 -->
        <div class="side-by-side-figures">
            <figure id="fig-1">
                <img src="..." alt="Figure 1">
                <figcaption>...</figcaption>
            </figure>
            <figure id="fig-2">
                <img src="..." alt="Figure 2">
                <figcaption>...</figcaption>
            </figure>
        </div>

        <h1 class="section-title">2 MATERIALS AND METHODS</h1>
        <h2 class="subsection-title">2.1 ...</h2>
        <p>2.1节开头内容...</p>
    </div>
    <div class="page-footer">3</div>
</div>
'''
    return page_html

# 组装所有页面
html_pages = [
    generate_cover_page(),    # 第1页
    generate_page_2(),        # 第2页
    generate_page_3(),        # 第3页
    # ... 继续生成每一页
]

final_html = html_header + '\n'.join(html_pages) + html_footer
```

**⚠️ 完整实施流程（必须按顺序执行）：**

```python
# 第一步：分析内容字数
sections = analyze_content(content)
# 输出示例：INTRODUCTION: 550 words, METHODS: 1200 words, ...

# 第二步：规划分页（根据字数和图表）
page_plan = {
    1: {'type': 'cover+text', 'content': 'title + abstract + metadata + Introduction开头段落（填满剩余空间）'},
    2: {'type': 'text', 'section': 'INTRODUCTION续 + METHODS开头', 'words': 400, 'paragraphs': [2,3,4,5]},
    3: {'type': 'mixed', 'section': 'METHODS 2.1-2.2', 'words': 350, 'figures': [1,2]},
    # ... 继续规划
}

# 第三步：一次性生成完整HTML文件（⚠️ 禁止逐页追加！）
# 第四步：写入文件
# 第五步：验证分页
validate_pagination(output_file)
```

**⚠️ 常见错误和避免方法：**

| 错误                       | 表现                                 | 避免方法                                                  |
| -------------------------- | ------------------------------------ | --------------------------------------------------------- |
| **使用追加模式写入** | 多次调用 Edit/Write 工具逐页追加       | ❌ 禁止 `<br>` ✅ 一次性生成完整 HTML 字符串，然后写入     |
| **让内容跨页流动**   | 所有内容在一个 `.two-column` 容器中 | ❌ 禁止 `<br>` ✅ 每页独立的 `<div class="page">`      |
| **未精确计算字数**   | 随意分配段落到页面                   | ❌ 禁止 `<br>` ✅ 使用 `analyze_content()` 计算每段字数 |
| **图表位置随意**     | 图表与引用文字距离过远               | ❌ 禁止 `<br>` ✅ 图表放在引用段落之后的页面             |

---

## 内容分割策略

### 步骤3.3：内容分割策略

**如何决定每页包含多少内容**:

1. **计算可用高度**:

   - 页面总高度：297 mm
   - 上边距：25 mm，下边距：20 mm
   - 页眉：约12 mm，页脚：约10 mm
   - **可用内容高度：约230 mm**
1. **估算文字高度**:

   - 字体：9 pt，行高：1.35
   - 每行高度：约4.3 mm
   - 双栏，每栏约27 mm 宽
   - **每栏约53行，每页约106行**
   - 每行约10-12个英文单词
   - **每页约600-800单词（纯文字）**
3. **扣除图表空间**:

   - 小图（并排）：约60 mm
   - 大图（跨栏）：约100-120 mm
   - 表格：根据行数估算，约40-80 mm
   - **有图表的页面：文字容量减半（300-400词）**
4. **分页点选择**:

   - 优先在段落之间分页
   - 避免标题单独在页底
   - 图表尽量放在引用它的文字附近

---

## 大图处理原则

### 大图处理原则

> **大图不要单独占一整页！尽可能并排放置，节省空间。**

#### 图片并排判断标准

| 条件                 | 判断标准                           | 处理方式                      |
| -------------------- | ---------------------------------- | ----------------------------- |
| **并排条件**   | 连续出现2张图片，且单张高度 < 80 mm | 使用并排布局                  |
| **等分比例**   | 两张图片内容同等重要               | `flex: 1` 等分              |
| **不等分比例** | 一张主图一张辅图（如流程图+小图）  | `flex: 1.2` + `flex: 0.8` |
| **禁止并排**   | 单张高度 > 120 mm 或图片数量 >=3    | 各自独立放置                  |
| **跨栏要求**   | 所有图片必须跨越双栏               | 使用 `column-span: all`     |

#### 图片并排 CSS 规则（双栏版）

```css
/* 基础并排容器 */
.side-by-side-figures {
  column-span: all;              /* 跨双栏 */
  display: flex;
  gap: 4mm;                      /* 图片间距 */
  margin: 5mm 0;
}

.side-by-side-figures figure {
  flex: 1;                       /* 默认等分 */
  margin: 0;
  min-width: 0;                  /* 允许收缩 */
}

.side-by-side-figures figure img {
  width: 100%;
  height: auto;
  max-height: 120mm;             /* ⚠️ 防止高度溢出：限制为页面高度的一半 */
  object-fit: contain;           /* 保持比例 */
  display: block;
}
```

#### 单张图片 CSS 规则

```css
figure img {
  width: 100%;
  height: auto;
  max-height: 120mm;             /* ⚠️ 防止高度溢出 */
  object-fit: contain;
  display: block;
}
```

#### 图片并排 CSS 规则（单栏版）

```html
<!-- 不等分比例示例：主图占60%，辅图占40% -->
<div style="display:flex;gap:5mm;margin:5mm 0;align-items:flex-end;break-inside:avoid;">
  <figure style="flex:1.2;margin:0;display:flex;flex-direction:column;">
    <img src="..." alt="主图" style="width:100%;height:auto;display:block;">
    <figcaption>...</figcaption>
  </figure>
  <figure style="flex:0.8;margin:0;display:flex;flex-direction:column;">
    <img src="..." alt="辅图" style="width:100%;height:auto;display:block;">
    <figcaption>...</figcaption>
  </figure>
</div>
```

#### 分页控制规则

```css
/* 防止图片跨页分割 */
figure, .side-by-side-figures, .table-wrapper {
  break-inside: avoid;
  page-break-inside: avoid;
}

/* 图片前强制分页条件（剩余空间不足时） */
@media print {
  .force-page-break-before {
    break-before: page;
    page-break-before: always;
  }
}
```

---

## 验证检查点

### ✅ CP 3检查点：验证无溢出/留白

**关键验证项（必须全部通过）：**

```python
def validate_pagination(html_file):
    """验证双栏HTML分页是否正确"""

    # 1. 检查页面数量
    page_count = html_file.count('<div class="page">')
    print(f"📄 总页数: {page_count}")

    # 2. 检查每页独立性
    pages = extract_pages(html_file)
    for i, page in enumerate(pages, 1):
        # 验证每页都有独立的page-content
        if '<div class="page-content' not in page:
            raise ValidationError(f"第{i}页缺少page-content容器")

    # 3. 验证内容分布（关键！）
    for i, page in enumerate(pages[1:], 2):  # 从第2页开始（第1页是封面）
        # 提取页面文本内容
        text_content = extract_text(page)
        word_count = len(text_content.split())

        # 检查是否有图表
        has_figures = '<figure' in page or '.side-by-side-figures' in page
        has_tables = '<table' in page

        # 验证字数范围
        if has_figures or has_tables:
            # 有图表的页面：300-500词
            if word_count < 250 or word_count > 550:
                print(f"⚠️ 第{i}页字数异常: {word_count}词（含图表，建议300-500词）")
        else:
            # 纯文字页面：600-900词
            if word_count < 500 or word_count > 950:
                print(f"⚠️ 第{i}页字数异常: {word_count}词（纯文字，建议600-900词）")

        print(f"✅ 第{i}页: {word_count}词, 图表={has_figures or has_tables}")

    # 4. 检查最后一页是否留白过多
    last_page = pages[-1]
    last_page_words = len(extract_text(last_page).split())
    if last_page_words < 300 and '参考文献' not in last_page and 'REFERENCES' not in last_page:
        print(f"⚠️ 最后一页内容过少({last_page_words}词)，可能留白过多")

    return True

# 执行验证
validate_pagination('双栏分页-XXX.html')
```

**手动验证步骤：**

1. **在浏览器中打开 HTML 文件**

   - 每页应该显示为一张完整的 A 4白色卡片
   - 页面之间有20 px 灰色间距
1. **逐页检查留白**

    ```
    ✅ 合格：页面底部空白 < 15mm
    ⚠️ 警告：页面底部空白 15-30mm（须压缩，拉入后续段落）
    ❌ 失败：页面底部空白 > 30mm（必须调整分页，不允许留白）
    ```
2. **检查溢出**

   - 使用浏览器检查元素，查看 `.page-content` 高度
   - 如果内容超出 `--content-height (252mm)`，则为溢出
   - 所有内容必须完全在白色页面内
4. **验证双栏平衡**

   - 打开浏览器开发者工具
   - 检查每页的左右栏高度是否相近
   - CSS column 会自动平衡，但如果差异过大（>20 mm），说明内容分配不当

**如果验证失败：**

```python
# 失败处理流程
if validation_failed:
    # 1. 重新分析内容
    analyze_content_distribution()

    # 2. 调整分页计划
    # 例如：第3页内容过多，将部分段落移到第4页
    page_plan[3]['content'] = 'METHODS 2.1前2段 + Figure 1-2'
    page_plan[4]['content'] = 'METHODS 2.1后3段 + 2.2开头'

    # 3. 重新生成HTML
    regenerate_html(page_plan)

    # 4. 再次验证
    validate_pagination('双栏分页-XXX.html')
```

**验证通过标准：**

- [ ] HTML 文件已生成
- [ ] 文件大小合理（通常20-50 KB）
- [ ] 包含所有页面（封面+正文+参考文献）
- [ ] 每页字数在合理范围（见上述标准）
- [ ] 无任何页面留白>30 mm（封面页除外：允许正文流入填满）
- [ ] 无任何内容溢出页面边界
- [ ] 在浏览器中打开显示正常
- [ ] 大表格已按步骤3.4处理（压缩或续表）
- [ ] 所有续表包含" (Continued)"标题和重复表头
- [ ] 已输出分页摘要表（含填充率和风险标注）

## Playwright 自动布局验证

此部分描述了使用 Playwright MCP 进行自动化布局验证的完整工作流。

### 1. 前置条件

在运行自动化验证脚本之前，请确保满足以下条件：

1.  **启动本地 HTTP 服务器**：由于 Playwright MCP 不支持 `file://` 协议，需在 HTML 文件所在目录启动临时服务器。
    ```bash
    python3 -m http.server 8080
    ```
2.  **文件结构**：
    - 输出目录应包含生成的 HTML 文件（例如 `output/article.html`）。
    - 确保 CSS 和图片资源路径正确，可以通过 HTTP 访问。

### 2. 视口设置

为了模拟 A4 纸张（210mm x 297mm）在 96 DPI 下的渲染效果，浏览器视口必须严格设置为：

-   **宽度**: 794px
-   **高度**: 1123px
-   **设备缩放因子**: 1.0

### 3. 完整测量 JavaScript

使用以下 JavaScript 代码在 Playwright 的 `browser_evaluate` 中执行，以精确测量每个页面的内容高度和溢出情况。此脚本会临时修改 DOM 样式进行测量，然后恢复原状。

```javascript
(() => {
    const results = [];
    const pages = document.querySelectorAll('.page-content');
    
    // 常量定义: 252mm = 952px (96 DPI)
    const MAX_CONTENT_HEIGHT_PX = 952;

    pages.forEach((page, index) => {
        // 1. 记录原始容器高度
        const originalRect = page.getBoundingClientRect();
        const containerHeight = originalRect.height;
        
        // 2. 临时修改样式以测量实际内容高度
        // 使用 !important 覆盖 CSS 列高度限制，使内容自然展开
        page.style.setProperty('height', 'auto', 'important');
        page.style.setProperty('overflow', 'visible', 'important');
        
        // 3. 测量实际内容高度
        const actualRect = page.getBoundingClientRect();
        const actualHeight = actualRect.height;
        
        // 4. 恢复原始样式
        page.style.removeProperty('height');
        page.style.removeProperty('overflow');
        
        // 5. 计算溢出和留白
        const overflowPx = Math.max(0, actualHeight - MAX_CONTENT_HEIGHT_PX);
        const whitespacePx = Math.max(0, MAX_CONTENT_HEIGHT_PX - actualHeight);
        
        results.push({
            page: index + 1,
            containerHeight: Math.round(containerHeight),
            actualHeight: Math.round(actualHeight),
            overflow: overflowPx > 0,
            overflowPx: Math.round(overflowPx),
            whitespacePx: Math.round(whitespacePx)
        });
    });
    
    return results;
})()
```

### 4. 阈值判定逻辑

基于 96 DPI (1mm ≈ 3.78px) 的换算标准，定义以下判定规则：

-   **基准高度**: `MAX_CONTENT_HEIGHT_PX = 952px` (252mm)
-   **警告阈值**: `WHITESPACE_WARNING_MM = 15mm` (≈ 57px)
-   **失败阈值**: `WHITESPACE_FAILURE_MM = 30mm` (≈ 113px)

**判定规则：**

1.  **❌ 失败 (FAILURE)**:
    -   内容溢出 (`overflowPx > 0`)
    -   留白过大 (`whitespacePx > 113px`)（零留白原则：≥30mm 即视为失败）
2.  **⚠️ 警告 (WARNING)**:
    -   留白处于警告区间 (`57px ≤ whitespacePx ≤ 113px`)
3.  **✅ 通过 (PASS)**:
    -   无溢出且留白在正常范围内 (`whitespacePx < 57px`)

### 5. 截图策略

截图分两类触发条件，**均需执行**：

**条件1：高度异常截图**（原有规则）
-   **触发条件**: 页面状态为 `FAILURE` 或 `WARNING`（即 `overflowPx > 0` 或 `whitespacePx ≥ 57px`）
-   **截图范围**: 截取整个视口（包含页眉页脚）
-   **命名规范**: `screenshots/page-{页码}-{状态}.png`（例如: `page-3-overflow.png`）

**条件2：跨页表格截图**（新增，不依赖高度结果）
-   **触发条件**: 结构检查JS（§7）发现 `crossPageTables` 不为空时，无论高度是否 PASS
-   **截图范围**: 跨页原表所在页 + 续表所在页，各截一张
-   **命名规范**:
    -   `screenshots/page-{页码}-table-cross.png`（原表页，如 `page-6-table-cross.png`）
    -   `screenshots/page-{页码}-table-continued.png`（续表页，如 `page-7-table-continued.png`）
-   **目的**: 即使高度全 PASS，也保留人眼确认跨页表格视觉连续性的截图证据（三线表线条、视觉无断开）

### 6. 结构化报告模板

自动化脚本应输出如下 JSON 格式的验证报告，便于 CI/CD 集成：

```json
{
  "summary": {
    "total_pages": 5,
    "status": "FAILURE",
    "issues_count": 2
  },
  "pages": [
    {
      "page": 1,
      "status": "PASS",
      "details": "Whitespace: 45px (Cover+text page, Introduction已流入填满)"
    },
    {
      "page": 2,
      "status": "PASS",
      "details": "Whitespace: 91px"
    },
    {
      "page": 3,
      "status": "FAILURE",
      "details": "Overflow: 224px",
      "screenshot": "screenshots/page-3-overflow.png"
    }
  ],
  "structure_checks": {
    "status": "PASS",
    "cross_page_tables": [
      {
        "tableNumber": "Table 4.",
        "sourcePage": 6,
        "continuedPage": 7,
        "hasContinuedCaption": true,
        "captionMatch": true,
        "hasThead": true,
        "status": "PASS"
      }
    ],
    "threeLineChecks": [],
    "errors": [],
    "warnings": []
  },
  "action_items": [
    "第3页内容溢出，建议将最后一段移至第4页或调整图片大小。",
    "第7页 Table 4 续表缺少 (Continued) 标题，请添加: <div class=\"table-caption\"><span class=\"tbl-label\">Table 4.</span> (Continued)</div>"
  ]
}
```

### 7. 结构完整性检查

在高度验证（§3）通过后，**必须额外执行**以下结构检查，验证跨页表格格式规范和三线表线条正确性。

> 高度通过 ≠ 排版正确。三线表缺线、续表缺标题/表头等视觉问题不影响高度，但会被用户发现。

```javascript
(() => {
    const pages = Array.from(document.querySelectorAll('.page'));
    const errors = [];
    const warnings = [];
    const crossPageTables = [];
    const threeLineChecks = [];

    // ── 工具函数 ──────────────────────────────────────────
    // 用 getComputedStyle 检测 border（而非 .style，避免 inline/继承差异）
    function borderWidthPx(el, side) {
        return parseFloat(getComputedStyle(el)['border' + side + 'Width']) || 0;
    }
    function isBorderNone(el, side) {
        return borderWidthPx(el, side) < 0.1;
    }
    // 1.5pt ≈ 2px（96dpi），用区间匹配避免浮点误差
    function isHeavyBorder(el, side) {
        const w = borderWidthPx(el, side);
        return w >= 1.9 && w <= 2.1;
    }
    // 从 .table-caption 文字提取 "Table N." 编号
    function extractTableNumber(captionEl) {
        if (!captionEl) return null;
        const m = captionEl.textContent.match(/Table\s+(\d+)\./i);
        return m ? 'Table ' + m[1] + '.' : null;
    }

    // ── 遍历每页 ──────────────────────────────────────────
    pages.forEach((page, pageIdx) => {
        const pageNum = pageIdx + 1;
        const tables = Array.from(page.querySelectorAll('table'));

        tables.forEach(table => {
            const tableId = table.id || '(no id)';
            const isSource = isBorderNone(table, 'Bottom');  // 跨页原表：无底线
            const isContinued = isBorderNone(table, 'Top'); // 续表：无顶线

            // ── 三线表检查（所有表格）────────────────────
            const thead = table.querySelector('thead');
            const firstTbodyTr = table.querySelector('tbody tr');

            const hasTopBorder = isHeavyBorder(table, 'Top');
            const hasBottomBorder = isHeavyBorder(table, 'Bottom');
            const hasHeaderSep = thead
                ? borderWidthPx(thead.querySelector('th, td'), 'Bottom') > 0
                : false;
            const hasSpuriousInner = firstTbodyTr
                ? borderWidthPx(firstTbodyTr, 'Top') > 0.5
                : false;

            const check = {
                page: pageNum,
                tableId,
                isCrossPageSource: isSource,
                isContinued,
                hasTopBorder,
                hasBottomBorder,
                hasHeaderSeparator: hasHeaderSep,
                hasSpuriousInnerBorders: hasSpuriousInner,
                status: 'PASS'
            };

            // 跨页原表：底线为none是合规的，豁免底线检查
            if (!hasTopBorder) {
                check.status = 'WARNING';
                warnings.push('P' + pageNum + ' ' + tableId + ': 三线表缺顶线');
            }
            if (!hasBottomBorder && !isSource) {
                // 非跨页原表才要求底线
                check.status = 'WARNING';
                warnings.push('P' + pageNum + ' ' + tableId + ': 三线表缺底线');
            }
            if (!hasHeaderSep && thead) {
                check.status = 'WARNING';
                warnings.push('P' + pageNum + ' ' + tableId + ': 表头缺分隔线（thead th border-bottom）');
            }
            if (hasSpuriousInner) {
                check.status = 'WARNING';
                warnings.push('P' + pageNum + ' ' + tableId + ': tbody内部行有多余border（非三线表格式）');
            }
            threeLineChecks.push(check);

            // ── 跨页表格匹配检查 ─────────────────────────
            if (isSource) {
                // 找原表编号
                const wrapper = table.closest('.table-wrapper, div');
                const sourceCaption = wrapper
                    ? wrapper.querySelector('.table-caption')
                    : null;
                const tableNumber = extractTableNumber(sourceCaption);

                // 去下一个 .page 找续表
                const nextPage = pages[pageIdx + 1];
                const contResult = {
                    tableNumber: tableNumber || '(unknown)',
                    sourcePage: pageNum,
                    continuedPage: pageNum + 1,
                    hasContinuedCaption: false,
                    captionMatch: false,
                    hasThead: false,
                    status: 'FAILURE'
                };

                if (nextPage) {
                    // 续表：border-top:none 的 table
                    const nextTables = Array.from(nextPage.querySelectorAll('table'));
                    const contTable = nextTables.find(t => isBorderNone(t, 'Top'));

                    if (contTable) {
                        // 检查续表 caption
                        const contWrapper = contTable.closest('.table-wrapper, div');
                        const contCaption = contWrapper
                            ? contWrapper.querySelector('.table-caption')
                            : null;
                        const contText = contCaption ? contCaption.textContent : '';

                        contResult.hasContinuedCaption = contText.toLowerCase().includes('continued');
                        contResult.captionMatch = tableNumber
                            ? contText.includes(tableNumber)
                            : false;
                        contResult.hasThead = !!contTable.querySelector('thead');

                        if (contResult.hasContinuedCaption && contResult.hasThead && contResult.captionMatch) {
                            contResult.status = 'PASS';
                        } else {
                            if (!contResult.hasContinuedCaption)
                                errors.push('P' + (pageNum+1) + ' 续表缺少 "(Continued)" 标题（规范：Table N. (Continued)）');
                            if (!contResult.hasThead)
                                errors.push('P' + (pageNum+1) + ' 续表缺少重复表头 <thead>');
                            if (!contResult.captionMatch && tableNumber)
                                errors.push('P' + (pageNum+1) + ' 续表 caption 编号与原表不匹配（原表：' + tableNumber + '）');
                        }
                    } else {
                        errors.push('P' + pageNum + ' 发现跨页原表（border-bottom:none），但下一页未找到对应续表');
                        contResult.status = 'FAILURE';
                    }
                }
                crossPageTables.push(contResult);
            }
        });
    });

    return {
        crossPageTables,
        threeLineChecks,
        errors,
        warnings,
        summary: {
            status: errors.length > 0 ? 'FAILURE' : warnings.length > 0 ? 'WARNING' : 'PASS',
            errorCount: errors.length,
            warningCount: warnings.length,
            crossPageTableCount: crossPageTables.length
        }
    };
})()
```

**判定规则：**
- `errors[]` 非空 → 结构检查 **FAILURE**（必须修复后才能交付）
  - 续表缺 `(Continued)` 标题
  - 续表缺 `<thead>`
  - caption 编号不匹配
  - 跨页原表找不到对应续表
- `warnings[]` 非空 → 结构检查 **WARNING**（建议修复）
  - 三线表缺线（顶/底/表头分隔线）
  - tbody 内部行有多余 border
- 均为空 → 结构检查 **PASS**
