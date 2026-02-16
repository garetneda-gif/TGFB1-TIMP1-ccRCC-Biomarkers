# HTML 结构参考文档

本文档说明期刊排版HTML的结构和CSS类使用方法。

## 页面尺寸规格

### A4 纸张
- **尺寸**: 210mm × 297mm
- **页边距**: 
  - 顶部: 25mm
  - 底部: 20mm
  - 左右: 20mm
- **内容区域**: 170mm × 252mm

### 双栏布局
- **栏宽**: 每栏约81.26mm (计算: (170mm - 7.48mm) / 2)
- **栏间距**: 7.48mm
- **每页容量**: 约800-1000字

## 核心CSS类

### 页面结构

| 类名 | 用途 | 说明 |
|------|------|------|
| `.page` | 页面容器 | 固定A4尺寸，每个代表一页 |
| `.page-header` | 页眉 | 绝对定位在顶部 |
| `.page-footer` | 页脚 | 绝对定位在底部 |
| `.page-content` | 内容区 | 主要文本区域 |
| `.two-column` | 双栏布局 | 添加到.page-content启用双栏 |
| `.page-num` | 页码 | 绝对定位 (right:0, top:2mm) |

### 封面元素

| 类名 | 用途 |
|------|------|
| `#cover` | 封面容器 |
| `#article-title` | 文章标题 |
| `#article-authors` | 作者列表 |
| `#front-matter` | 前置信息区（单位+摘要） |
| `#abstract-box` | 摘要框 |
| `#abstract-body` | 摘要正文 |

### 正文元素

| 类名 | 用途 |
|------|------|
| `.section-title` | 一级标题 (H1) |
| `.subsection-title` | 二级标题 (H2) |
| `.no-indent` | 无缩进段落（首段） |
| `.side-by-side-figures` | 并排图片容器 |
| `.table-wrapper` | 表格容器 |
| `.table-caption` | 表格标题 |
| `.references` | 参考文献区域 |

## 封面页结构

```
div.page
├── div.page-content
│   └── div#cover
│       ├── [Row 1] Flex容器 (border-bottom: black)
│       │   ├── 日期 + DOI
│       │   └── MedBA Medicine
│       ├── [Row 2] Flex容器
│       │   ├── ORIGINAL ARTICLE (Blue #005a8c / Black)
│       │   └── MedBA Logo
│       ├── div#article-title - 标题
│       ├── div#article-authors - 作者列表
│       └── div#front-matter (Flex, align-items:stretch)
│           ├── [左栏] (30%) - 单位、通讯作者、资助 (border-right: 2px solid #005a8c)
│           └── div#abstract-box (70%) - 摘要框 (Grey #f8f9fa, No Border)
│               ├── [Abstract标题]
│               └── div#abstract-body
│                   ├── Background
│                   ├── Methods
│                   ├── Results
│                   ├── Conclusion
│                   └── Keywords
└── div.page-footer
    ├── 期刊网址
    └── span.page-num (absolute: right 0, top 2mm)
```

## 正文页结构

```
div.page
├── div.page-header - 作者姓名大写
├── div.page-content.two-column
│   ├── h1.section-title - 一级标题
│   ├── h2.subsection-title - 二级标题
│   ├── p - 正文段落
│   ├── div.side-by-side-figures - 并排图片
│   │   ├── figure
│   │   │   ├── img
│   │   │   └── figcaption
│   │   └── figure
│   ├── div.table-wrapper
│   │   ├── p.table-caption
│   │   └── table
│   └── div.references
└── div.page-footer - 页码
```

## 分页控制

### 分页规则

1. **封面页**: 固定结构，不分割
2. **新章节**: 剩余空间<80mm时开新页
3. **图片**: 高度>60%剩余空间时，前置分页
4. **表格**: 优先压缩间距（line-height/padding/font-size/margin）使其在当前页内；压缩仍不够时才跨页分割，续表标注 "Table N. (Continued)" 并重复表头
5. **段落**: 保持至少3行在同一页

### 分页实现

```html
<!-- 结束当前页，开始新页 -->
</div></div>
<div class="page">
    <div class="page-header">AUTHOR ET AL.</div>
    <div class="page-content two-column">
```

### 白空间容忍

- 页底最大留白: 30mm
- 超过30mm时，考虑提前分页或调整内容

## 双栏 vs 单栏

### 双栏分页版（供PDF下载）
- 使用 `.two-column` 类
- 手动 `<div class="page">` 分页
- 页眉显示作者姓名
- 页脚显示页码
- **封面差异**: Abstract框无边框，采用左右分栏布局 (Flex 30%/70%)
- **ORIGINAL ARTICLE**: 蓝色 (#005a8c)

### 单栏连续版（供在线预览）
- 不使用 `.two-column`
- 无手动分页
- 连续滚动
- 参考文献带元数据链接
- **封面差异**: Abstract框保留边框/阴影/装饰，采用上下堆叠布局
- **ORIGINAL ARTICLE**: 黑色 (#000)

## 主题色

```css
:root {
    --primary-color: #005a8c;  /* 期刊主题色 */
    --text-color: #333;
    --text-secondary: #666;
}
```

使用场景:
- 期刊Logo/名称
- 摘要框边框
- 图表标签
- 链接颜色
- 文章类型标签

## 字体规范

| 元素 | 字体 | 大小 | 应用场景 |
|------|------|------|----------|
| 正文 | Times New Roman | 9pt | 双栏分页版 |
| 正文 | Times New Roman | 10pt | 单栏连续版 |
| 一级标题 | Arial | 11pt | 章节标题 (如 1 INTRODUCTION) |
| 二级标题 | Arial | 9.5pt | 小节标题 (如 2.1 Methods) |
| 摘要正文 | Times New Roman | 9pt | Abstract内容 |
| 参考文献 | Times New Roman | 8pt | 参考文献列表 |
| 图表标注 | Times New Roman | 8.5pt | Figure/Table标题 |
| 页眉页脚 | Times New Roman | 8-9pt | 作者名、页码、网址 |

### CSS变量定义

```css
:root {
    --page-width: 210mm;
    --page-height: 297mm;
    --margin-top: 25mm;
    --margin-bottom: 20mm;
    --margin-left: 20mm;
    --margin-right: 20mm;
    --column-gap: 7.48mm;
    --primary-color: #005a8c;
}
```
