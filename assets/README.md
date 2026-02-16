# MedBA Medicine 期刊排版模板使用说明

## 概述

本目录包含两个标准化的HTML模板文件,用于将Word学术论文转换为MedBA Medicine期刊的标准HTML格式。

## 模板文件

### 1. template-single-column.html（单栏模板）

**用途**: 适用于在线预览的连续滚动版本
**特点**:

- 单栏连续布局
- 适合网页浏览
- 便于阅读和复制内容
- 自适应宽度

### 2. template-two-column.html（双栏模板）

**用途**: 适用于PDF下载的分页版本
**特点**:

- 双栏分页布局
- 符合传统期刊排版
- 适合打印和PDF生成
- A4纸张标准

## 样式规范

### 颜色规范

- 主题蓝色: `#005a8c` - 用于标题、链接、装饰元素
- 正文黑色: `#000`
- 灰色边框: `#b8b8b8` / `#ccc`
- 背景灰色: `#e8e9ea` / `#525659`

### 字体规范

- 正文字体: Times New Roman, 9-10pt
- 标题字体: Arial/Helvetica
- 一级标题: 11pt, 加粗, 大写
- 二级标题: 9.5pt, 加粗
- 摘要文字: 9pt
- 参考文献: 8pt

### 间距规范

- 页边距: 上25mm, 下20mm, 左右各20mm
- 段落间距: 2mm
- 段落首行缩进: 1em
- 双栏间距: 7.48mm

## 模板结构

### 首页结构

```
├── 页眉区域
│   ├── 收稿/修订/接收日期
│   ├── DOI编号
│   └── 期刊Logo和名称
├── 文章类型标签
├── 标题和作者
├── 前置信息
│   ├── 作者单位
│   ├── 通讯作者
│   ├── 贡献声明
│   └── 基金资助
└── 摘要盒子
    ├── Background
    ├── Materials and Methods
    ├── Results
    ├── Conclusion
    └── Keywords
```

### 正文结构

```
├── 一级标题（章节）
│   └── 二级标题（小节）
│       ├── 段落
│       ├── 图片
│       └── 表格
└── 参考文献
```

## 使用步骤

### 1. 选择合适的模板

- **在线预览版** → 使用 `template-single-column.html`
- **PDF下载版** → 使用 `template-two-column.html`

### 2. 填充内容

#### 基本信息

```html
<!-- 修改日期 -->
Received: 日期 / Revised: 日期 / Accepted: 日期

<!-- 修改DOI -->
DOI: 10.xxxxx/xxxxx

<!-- 修改文章类型 -->
ORIGINAL ARTICLE / REVIEW / CASE REPORT

<!-- 修改标题 -->
<div id="article-title">您的文章标题</div>

<!-- 修改作者（注意上标编号） -->
<div id="article-authors">
    作者1<span style="vertical-align:super;">1</span>,
    作者2<span style="vertical-align:super;">2</span>
</div>
```

#### 作者单位和联系方式

```html
<!-- 机构列表 -->
<span style="vertical-align:super;">1</span>机构名称<br>
<span style="vertical-align:super;">2</span>机构名称

<!-- 通讯作者 -->
<span style="font-weight:bold;">Correspondence</span>
作者姓名, 单位, 地址<br>
Email: xxx@xxx.com

<!-- 基金资助 -->
<span style="font-weight:bold;">Funding information</span>
资助信息
```

#### 摘要部分

```html
<p><span style="font-weight:bold;">Background:</span> 背景内容</p>
<p><span style="font-weight:bold;">Materials and Methods:</span> 方法内容</p>
<p><span style="font-weight:bold;">Results:</span> 结果内容</p>
<p><span style="font-weight:bold;">Conclusion:</span> 结论内容</p>
<span style="font-weight:bold;">Keywords:</span> 关键词1; 关键词2; 关键词3
```

#### 正文标题

```html
<!-- 一级标题 -->
<h1 class="section-title">1 INTRODUCTION</h1>

<!-- 二级标题 -->
<h2 class="subsection-title">1.1 Background</h2>

<!-- 段落 -->
<p>段落内容...</p>
```

#### 插入图片

```html
<!-- 单张图片 -->
<figure id="fig-1">
    <img src="图片URL" alt="Figure 1">
    <figcaption>
        <span class="fig-label">Figure 1.</span> 图片描述
    </figcaption>
</figure>

<!-- 并排两张图片 -->
<div class="side-by-side-figures">
    <figure id="fig-1">
        <img src="图片1URL" alt="Figure 1">
        <figcaption><span class="fig-label">Figure 1.</span> 描述</figcaption>
    </figure>
    <figure id="fig-2">
        <img src="图片2URL" alt="Figure 2">
        <figcaption><span class="fig-label">Figure 2.</span> 描述</figcaption>
    </figure>
</div>
```

#### 插入表格

```html
<div class="table-wrapper" id="tbl-1">
    <div class="table-caption">
        <span class="tbl-label">Table 1.</span> 表格标题
    </div>
    <table>
        <thead>
            <tr>
                <th>列标题1</th>
                <th>列标题2</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>数据1</td><td>数据2</td></tr>
            <tr><td>数据3</td><td>数据4</td></tr>
        </tbody>
    </table>
</div>
```

#### 参考文献

```html
<div class="references">
    <div>[1] 作者. 标题[J]. 期刊名, 年份, 卷(期):页码.</div>
    <div>[2] 作者. 标题[J]. 期刊名, 年份, 卷(期):页码.</div>
</div>
```

### 3. 参考文献链接

自动为参考文献添加验证后的元数据链接:

- **PubMed**: 用于生物医学文献
- **Google Scholar**: 通用学术搜索
- **Crossref**: DOI解析和引用数据

链接格式:

```html
<a href="PubMed链接" style="color:#005a8c;">PubMed</a> | 
<a href="Google Scholar链接" style="color:#005a8c;">Google Scholar</a> | 
<a href="Crossref链接" style="color:#005a8c;">Crossref</a>
```

## 注意事项

### 1. 图片处理

- 所有图片必须使用绝对URL或相对路径
- 推荐使用CDN或服务器托管图片
- 图片格式: PNG, JPG
- 图片宽度: 自动适应容器宽度

### 2. 特殊符号

- 小于号: `&lt;`
- 大于号: `&gt;`
- 上标: `<sup>文字</sup>` 或 `<span style="vertical-align:super;">文字</span>`
- 下标: `<sub>文字</sub>`

### 3. 链接格式

```html
<a href="#fig-1" style="color:#005a8c;">Figure 1</a>
<a href="#tbl-1" style="color:#005a8c;">Table 1</a>
<a href="URL" style="color:#005a8c;">链接文字</a>
```

### 4. 打印输出

- 使用浏览器的"打印"功能
- 选择"另存为PDF"
- 确保启用"背景图形"选项
- 纸张大小: A4

## 版本控制

建议使用版本控制系统(如Git)管理模板和生成的文件:

```bash
git add template-*.html
git commit -m "更新模板版本"
```

## 常见问题

### Q: 如何调整页边距?

A: 修改CSS中的 `:root`变量:

```css
:root {
    --margin-top: 25mm;
    --margin-bottom: 20mm;
    --margin-left: 20mm;
    --margin-right: 20mm;
}
```

### Q: 如何修改双栏间距?

A: 修改 `--column-gap`变量:

```css
:root {
    --column-gap: 7.48mm;
}
```

### Q: 图片不显示怎么办?

A: 检查:

1. 图片URL是否正确
2. 图片是否可访问
3. 浏览器控制台是否有错误

### Q: 如何添加页码?

A: 修改页脚内容:

```html
<div class="page-footer">1</div>
<div class="page-footer">2</div>
```
