# HTML元素样式映射表 (Style Mapping Reference)

## 概述

本文档提供了MedBA Medicine期刊HTML排版中所有元素的精确样式映射，确保生成的HTML与模板100%一致。

**强制规则**:
- ❌ 禁止推测或修改任何样式值
- ✅ 必须使用本文档中列出的精确样式
- ✅ 所有数值必须带单位（mm, pt, px等）
- ✅ 颜色值必须使用十六进制格式（如 `#005a8c`）

---

## 🎨 全局样式变量

### 双栏版 (template-two-column.html)

```css
:root {
    --page-width: 210mm;           /* A4纸宽度 */
    --page-height: 297mm;          /* A4纸高度 */
    --margin-top: 25mm;            /* 页面上边距 */
    --margin-bottom: 20mm;         /* 页面下边距 */
    --margin-left: 20mm;           /* 页面左边距 */
    --margin-right: 20mm;          /* 页面右边距 */
    --content-width: calc(var(--page-width) - var(--margin-left) - var(--margin-right));
    --content-height: calc(var(--page-height) - var(--margin-top) - var(--margin-bottom));
    --column-gap: 7.48mm;          /* 双栏之间的间距 */
}
```

### 单栏版 (template-single-column.html)

单栏版不使用CSS变量，直接在元素中定义样式。

---

## 📄 页面容器样式

### 双栏版

| 元素 | Class | Inline Style |
|------|-------|--------------|
| `<body>` | - | `margin: 0; padding: 20px 0; background: #525659; font-family: 'Times New Roman', Times, serif; font-size: 9pt; line-height: 1.35; color: #000;` |
| `.page` | `page` | `width: var(--page-width); height: var(--page-height); margin: 0 auto 20px; padding: var(--margin-top) var(--margin-right) var(--margin-bottom) var(--margin-left); background: #fff; box-shadow: 0 4px 20px rgba(0,0,0,0.3); position: relative; overflow: hidden;` |
| `.page-content` | `page-content` | `height: var(--content-height); overflow: hidden;` |
| `.two-column` | `two-column` | `column-count: 2; column-gap: var(--column-gap); text-align: justify;` |

### 单栏版

| 元素 | ID/Class | Inline Style |
|------|----------|--------------|
| `<body>` | - | `margin:0; background:#e8e9ea; font-family:'Times New Roman',Times,serif; font-size:10pt; line-height:1.38; color:#000;` |
| `#page` | `page` | `max-width:210mm; margin:24px auto; padding:26mm 20mm; background:#fff; box-shadow:0 14px 50px rgba(0,0,0,0.12);` |

---

## 📰 页眉页脚样式

### 双栏版

| 元素 | Class | Inline Style |
|------|-------|--------------|
| `.page-header` | `page-header` | `position: absolute; top: 10mm; left: var(--margin-left); right: var(--margin-right); font-size: 8pt; text-transform: uppercase; text-align: right; color: #000; border-bottom: 0.5pt solid #ccc; padding-bottom: 2mm;` |
| `.page-footer` | `page-footer` | `position: absolute; bottom: 8mm; left: var(--margin-left); right: var(--margin-right); font-size: 9pt; text-align: center; color: #000; border-top: 0.5pt solid #000; padding-top: 2mm;` |
| `.page-num` | `page-num` | `position: absolute; right: 0; top: 2mm;` |

### 单栏版

单栏版使用固定定位的页眉页脚（仅在打印时显示）：

```css
#running-header {
    position: fixed;
    top: 8mm;
    left: 0;
    right: 0;
    padding: 0 20mm;
}

#running-footer {
    position: fixed;
    bottom: 8mm;
    left: 0;
    right: 0;
    padding: 0 20mm;
    display: none;  /* 首页不显示 */
    border-top: 0.5pt solid #ccc;
    padding-top: 2mm;
}
```

---

## 📝 标题样式

### 一级标题 (h1)

**双栏版**:
```css
h1.section-title {
    column-span: all;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11pt;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    text-align: left;
    margin: 6mm 0 3mm 0;
}
```

**单栏版**:
```html
<h1 style="column-span:all; font-family:Arial,Helvetica,sans-serif; font-size:11pt; font-weight:600; letter-spacing:0.04em; text-transform:uppercase; text-align:left; margin-top:0; margin-bottom:6mm; border-top:0; padding-top:0;">
    1 INTRODUCTION
</h1>
```

### 二级标题 (h2)

**双栏版**:
```css
h2.subsection-title {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 9.5pt;
    font-weight: bold;
    text-align: left;
    margin: 3mm 0 2mm 0;
}
```

**单栏版**:
```html
<h2 style="font-family:Arial,Helvetica,sans-serif; font-size:9.5pt; font-weight:bold; text-align:left; margin-top:5mm; margin-bottom:2.5mm;">
    2.1 TCGA-CESC cohort
</h2>
```

---

## 📄 段落样式

### 正文段落

**双栏版**:
```css
p {
    margin: 0 0 2mm 0;
    text-indent: 1em;
}
```

**单栏版**:
```html
<p style="margin:0 0 2mm 0; text-indent:1em; text-align:justify;">
    段落内容...
</p>
```

### 无缩进段落

**双栏版**:
```css
p.no-indent {
    text-indent: 0;
}
```

**单栏版**:
```html
<p style="margin:0 0 3mm 0; text-indent:0; text-align:left;">
    机构信息、通讯作者等
</p>
```

---

## 🖼️ 图片样式

### 单独图片

**双栏版**:
```css
figure {
    column-span: all;
    margin: 5mm 0;
    width: 100%;
    break-inside: avoid;
    page-break-inside: avoid;
}

figure img {
    width: 100%;
    height: auto;
    display: block;
}

figcaption {
    font-size: 8.5pt;
    margin-top: 2mm;
    text-align: left;
    line-height: 1.3;
    color: #222;
}

figcaption .fig-label {
    font-weight: bold;
    color: #005a8c;
}
```

**单栏版**:
```html
<figure id="fig-1" style="margin:5mm 0; break-inside:avoid; page-break-inside:avoid;">
    <img src="..." alt="Figure 1" style="width:100%; height:auto; display:block;">
    <figcaption style="font-size:8.5pt; margin-top:2mm; text-align:left; line-height:1.3; color:#222;">
        <span style="font-weight:bold; color:#005a8c;">Figure 1.</span> The flowchart of the study.
    </figcaption>
</figure>
```

### 并排图片 (Side-by-Side)

**双栏版**:
```css
.side-by-side-figures {
    column-span: all;
    display: flex;
    gap: 4mm;
    margin: 5mm 0;
    break-inside: avoid;
    page-break-inside: avoid;
}

.side-by-side-figures figure {
    flex: 1;
    margin: 0;
    min-width: 0;
}
```

**单栏版** (⚠️ 关键 - 这是用户反馈的问题所在):
```html
<div style="display:flex; gap:5mm; margin:5mm 0; align-items:flex-end; break-inside:avoid; page-break-inside:avoid;">
    <figure id="fig-1" style="flex:1.2; margin:0; display:flex; flex-direction:column;">
        <img src="..." alt="Figure 1" style="width:100%; height:auto; display:block;">
        <figcaption style="font-size:8.5pt; margin-top:2mm; text-align:left; line-height:1.3; color:#222;">
            <span style="font-weight:bold; color:#005a8c;">Figure 1.</span> Caption text
        </figcaption>
    </figure>
    <figure id="fig-2" style="flex:0.8; margin:0; display:flex; flex-direction:column;">
        <img src="..." alt="Figure 2" style="width:100%; height:auto; display:block;">
        <figcaption style="font-size:8.5pt; margin-top:2mm; text-align:left; line-height:1.3; color:#222;">
            <span style="font-weight:bold; color:#005a8c;">Figure 2.</span> Caption text
        </figcaption>
    </figure>
</div>
```

**并排比例规则**:
- 等分：`flex:1` + `flex:1`
- 主辅图：`flex:1.2` + `flex:0.8`
- 不并排：单张高度 > 120mm 或数量 >= 3

---

## 📊 表格样式

### 表格容器

**双栏版**:
```css
.table-wrapper {
    column-span: all;
    margin: 5mm 0 6mm;
    width: 100%;
    break-inside: avoid;
    page-break-inside: avoid;
}

.table-caption {
    font-size: 8.5pt;
    margin-bottom: 2mm;
    text-align: left;
    color: #222;
}

.table-caption .tbl-label {
    font-weight: bold;
    color: #005a8c;
}
```

**单栏版**:
```html
<div style="margin:5mm 0 6mm; break-inside:avoid; page-break-inside:avoid; width:100%;" id="tbl-1">
    <div style="font-size:8.5pt; margin-bottom:2mm; text-align:left; font-weight:normal; color:#222;">
        <span style="font-weight:bold; color:#005a8c;">Table 1.</span> Patient clinical information statistics.
    </div>
    <table>...</table>
</div>
```

### 表格主体

**通用样式**:
```css
table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    line-height: 1.3;
    border-top: 1.5pt solid #000;
    border-bottom: 1.5pt solid #000;
}

th {
    border-bottom: 0.5pt solid #000;
    font-weight: bold;
    text-align: left;
    padding: 1.5mm 2mm;
    vertical-align: bottom;
}

td {
    padding: 1mm 2mm;
    vertical-align: top;
}
```

---

## 📚 参考文献样式

### 双栏版

```css
.references {
    font-size: 8pt;
    line-height: 1.3;
}

.references div {
    margin-bottom: 2mm;
    padding-left: 1.5em;
    text-indent: -1.5em;
}
```

### 单栏版

```html
<div style="font-size:8pt; line-height:1.35;">
    <div style="margin-bottom:2.5mm; padding-left:1.5em; text-indent:-1.5em;">
        [1] 文献内容...<br>
        <a href="..." target="_blank" style="color:#005a8c; text-decoration:none;">PubMed</a> |
        <a href="..." target="_blank" style="color:#005a8c; text-decoration:none;">Google Scholar</a> |
        <a href="..." target="_blank" style="color:#005a8c; text-decoration:none;">Crossref</a>
    </div>
</div>
```

**链接样式规则**:
- 颜色：`#005a8c`
- 无下划线：`text-decoration:none`
- 分隔符：` | ` (空格+竖线+空格)

---

## 🎨 摘要盒子样式

### 双栏版 (首页布局：左侧信息 + 右侧摘要)

```html
<div id="front-matter" style="display:flex; margin-bottom:8mm; align-items:stretch;">
    <!-- 左栏：机构信息等 (30%) -->
    <div style="width:30%; font-size:8pt; line-height:1.3; padding:4mm 4mm 4mm 0; border-right:2px solid #005a8c;">
        <p>...</p>
    </div>

    <!-- 右栏：摘要盒子 (70%) -->
    <div id="abstract-box" style="width:70%; padding:4mm 0 4mm 4mm; position:relative; background-color:#f8f9fa;">
        <div style="font-size:10pt; font-weight:bold; font-variant:small-caps; letter-spacing:0.05em; margin-bottom:3mm; color:#000;">Abstract</div>
        <div id="abstract-body" style="font-size:9pt; line-height:1.3;">
            <p style="margin:0 0 3mm 0; text-indent:0; text-align:justify;">
                <span style="font-weight:bold;">Background:</span> ...
            </p>
        </div>
    </div>
</div>
```

### 单栏版 (全宽，无左侧栏)

```html
<div id="abstract-box" style="width:100%; border:1pt solid #b8b8b8; border-left:3pt solid #005a8c; padding:6mm 7mm; position:relative; box-sizing:border-box; overflow-wrap:break-word; word-wrap:break-word; box-shadow:0 0 15px rgba(0,0,0,0.15); background-color:#f8f9fa;">
    <!-- 同上 -->
</div>
```

---

## 🔗 链接样式

**全局链接**:
```css
a {
    overflow-wrap: anywhere;
    word-break: break-word;
    color: #005a8c;
    text-decoration: none;
}
```

---

## ✅ 样式检查清单

生成HTML后，必须验证以下项目：

### 必检项

- [ ] `<style>` 标签完全复制自模板（行数一致）
- [ ] 主题色 `#005a8c` 出现在所有应有位置
- [ ] 字体family为 `'Times New Roman', Times, serif`
- [ ] 数值单位为 `mm`（不是 `px` 或 `pt`）
- [ ] 并排图片使用 `display:flex; gap:5mm`
- [ ] 图片标题使用 `font-size:8.5pt; color:#222;`
- [ ] 图号使用 `font-weight:bold; color:#005a8c;`
- [ ] 参考文献链接颜色为 `#005a8c`
- [ ] 表格边框为 `1.5pt solid #000`

### 双栏版额外检查

- [ ] CSS变量 `--column-gap: 7.48mm` 已定义
- [ ] `.two-column` class的 `column-count: 2`
- [ ] 标题使用 `column-span: all`
- [ ] `.page` 的高度为 `var(--page-height)`

### 单栏版额外检查

- [ ] `#page` 的 `max-width: 210mm`
- [ ] 无任何分页CSS（`page-break`, `break-before`等）
- [ ] 背景色为 `#e8e9ea`
- [ ] 内边距为 `26mm 20mm`

---

## 🚫 常见错误示例

### ❌ 错误：使用像素单位
```css
/* 错误 */
margin: 20px 0;

/* 正确 */
margin: 5mm 0;
```

### ❌ 错误：近似颜色值
```css
/* 错误 */
color: #0059ab;  /* 接近但不等于 #005a8c */
color: rgb(0, 90, 140);  /* 应该用十六进制 */

/* 正确 */
color: #005a8c;
```

### ❌ 错误：修改模板字体大小
```css
/* 错误 - 模板是8.5pt */
figcaption { font-size: 9pt; }

/* 正确 */
figcaption { font-size: 8.5pt; }
```

### ❌ 错误：自定义flex比例
```html
<!-- 错误 -->
<figure style="flex:1.5; margin:0;">

<!-- 正确 - 只能使用1, 1.2, 0.8这三个值 -->
<figure style="flex:1.2; margin:0;">
```

---

## 📖 快速查询索引

| 元素类型 | 双栏版关键样式 | 单栏版关键样式 | 模板行号 |
|---------|--------------|--------------|----------|
| 一级标题 | `font-size:11pt; text-transform:uppercase` | 同左 | 双:109-124, 单:234 |
| 二级标题 | `font-size:9.5pt; font-weight:bold` | 同左 | 双:127-133, 单:246 |
| 正文段落 | `text-indent:1em; margin:0 0 2mm 0` | 同左 | 双:136-139, 单:237 |
| 图片容器 | `column-span:all; margin:5mm 0` | `margin:5mm 0` | 双:147-172, 单:251-260 |
| 并排图片 | `.side-by-side-figures` class | inline `display:flex` | 双:232-244, 单:251-260 |
| 表格 | `border-top:1.5pt solid #000` | 同左 | 双:196-218, 单:267-280 |
| 参考文献 | `font-size:8pt; padding-left:1.5em` | 同左 | 双:220-230, 单:286-314 |

---

## 版本历史

- **v1.1** (2026-02-16): 更新首页布局（双栏Flex分栏）、页脚样式及Abstract样式优化
- **v1.0** (2026-01-31): 初始版本，配合 SKILL v3.1

---

## 🚨 图片溢出防护规则

### 图片高度限制（防止单张图片占据整页）

**所有图片必须添加高度限制**，确保不会超出页面可用高度的一半：

#### 双栏版完整CSS

```css
/* 单张图片 */
figure img {
    width: 100%;
    height: auto;
    max-height: 120mm;        /* ⚠️ 防止高度溢出：限制为页面高度的一半 */
    object-fit: contain;      /* 保持比例，避免变形 */
    display: block;
}

/* 并排图片 */
.side-by-side-figures figure img {
    width: 100%;
    height: auto;
    max-height: 120mm;        /* ⚠️ 防止高度溢出 */
    object-fit: contain;
    display: block;
}
```

#### 单栏版完整inline style

**单张图片**:
```html
<img src="..." alt="Figure 3" style="width:100%;height:auto;max-width:100%;max-height:120mm;object-fit:contain;display:block;">
```

**并排图片**:
```html
<div style="display:flex;gap:5mm;margin:5mm 0;align-items:flex-end;break-inside:avoid;page-break-inside:avoid;">
    <figure id="fig-1" style="flex:1.2;margin:0;display:flex;flex-direction:column;">
        <img src="..." alt="Figure 1" style="width:100%;height:auto;max-width:100%;max-height:120mm;object-fit:contain;display:block;">
        <figcaption style="font-size:8.5pt;margin-top:2mm;text-align:left;line-height:1.3;color:#222;">
            <span style="font-weight:bold;color:#005a8c;">Figure 1.</span> Caption text
        </figcaption>
    </figure>
    <figure id="fig-2" style="flex:0.8;margin:0;display:flex;flex-direction:column;">
        <img src="..." alt="Figure 2" style="width:100%;height:auto;max-width:100%;max-height:120mm;object-fit:contain;display:block;">
        <figcaption style="font-size:8.5pt;margin-top:2mm;text-align:left;line-height:1.3;color:#222;">
            <span style="font-weight:bold;color:#005a8c;">Figure 2.</span> Caption text
        </figcaption>
    </figure>
</div>
```

### 分页控制规则

防止图片、表格跨页分割：

```css
/* 防止元素跨页分割 */
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

## 版本历史

- **v1.2** (2026-02-16): 新增图片溢出防护规则（max-height, object-fit）及分页控制CSS
- **v1.1** (2026-02-16): 更新首页布局（双栏Flex分栏）、页脚样式及Abstract样式优化
- **v1.0** (2026-01-31): 初始版本，配合 SKILL v3.1
