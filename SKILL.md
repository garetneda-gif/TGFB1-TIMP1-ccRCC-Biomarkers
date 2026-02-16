---
name: journal-typesetting
description: |
  将Word学术论文转换为MedBA Medicine期刊HTML格式。支持双栏分页(PDF下载)和单栏连续(在线预览)两种输出。
  自动为参考文献添加验证后的元数据链接(PubMed | Google Scholar | Crossref)。
  使用场景：当用户提供Word格式的学术论文并要求排版为期刊HTML格式时使用。
  触发词：期刊排版
mcp:
  pubmed:
    command: npx
    args: ["@cyanheads/pubmed-mcp-server"]
  crossref:
    command: npx
    args: ["-y", "@botanicastudios/crossref-mcp"]
---
# 期刊排版技能 (Journal Typesetting) 

## 概述
1. 本技能将 Word 格式的学术论文转换为 MedBA Medicine 期刊规定的 HTML 格式，生成两个版本：
	1. **双栏分页版** - 供 PDF 下载，A 4分页，双栏布局
	2. **单栏连续版** - 供在线预览，连续滚动，包含参考文献元数据链接
2. 期刊默认配置
	- **期刊名称**: MedBA Medicine
	- **Logo URL**: https://medbam.org/assets/logo.png
	- **DOI 前缀**: 10.65079/xxx
	- **网址**: https://medbam.org
	- **主题色**: #005a8c
3. 资源文件
	
	| 目录 | 文件 | 说明 |
	|------|------|------|
	| 根目录 | `README.md` | Skill 使用说明和快速开始指南 |
	|  | `SKILL.md` | 完整技能文档（本文档） |
	| Assets/ | `template-two-column.html` | **双栏分页 HTML 模板**（含分页修复） |
	|  | `template-single-column.html` | **单栏连续 HTML 模板**（连续滚动） |
	| Scripts/ | `layout_validator.py` | 自动布局验证器（检测溢出/留白） |
	|  | `verify_links.py` | 参考文献链接验证工具 |
	|  | `html_generator.py` | HTML 生成核心模块（内部） |
	|  | `style_validator.py` | 样式一致性验证器 |
	| References/ | `html-structure.md` | HTML 结构和 CSS 类说明 |
	|  | `reference-links.md` | 参考文献链接生成指南 |
	|  | `style-mapping.md` | 样式映射表（元素与CSS对应关系） |
	|  | `pagination-rules.md` | **MANDATORY**: 分页规则（内容分析、HTML模板、CP3验证） |
	|  | `troubleshooting.md` | 常见问题排查指南 |

## ⚠️ 大文件写入规则（全局约束）

当 HTML 文件超过30 KB 时，**禁止使用 write 工具**，必须使用 Python 分段写入：

```python
python3 << 'PYEOF'
content = '''<!DOCTYPE html>…'''
with open('/path/to/output.html', 'w', encoding='utf-8') as f:
    f.write(content)
PYEOF

# 追加模式
python3 << 'PYEOF'
content = '''…更多内容…'''
with open('/path/to/output.html', 'a', encoding='utf-8') as f:
    f.write(content)
PYEOF
```

---

## 🔄 工作流程总览

```
[预检] 确认前置条件 → [步骤0] 依赖检查 → [步骤1] 解析文档 → [步骤2] 收集图片URL →
[步骤3] 生成双栏HTML → [步骤4] 生成单栏HTML → [步骤5] 添加参考文献链接 →
[步骤6] 输出文件 → [步骤7] 强制验证 ✅
```

## 📊 进度追踪方式

所有进度追踪通过 **标准输出（print）** 以 **Markdown 格式** 输出，Claude 会在对话中实时展示：

### 输出格式示例

```python
# 步骤进度
print("📋 步骤3/7: 生成双栏分页HTML...")
print("   ├─ 模板加载: ✅")
print("   ├─ 封面页生成: ✅")
print("   ├─ 正文分页: 📄 第2-6页")
print("   └─ 文件写入: ✅ (38.5 KB)")

# 检查点状态
print("\n### ✅ CP3检查点")
print("- [x] HTML文件已生成")
print("- [x] 文件大小合理（20-50KB）")
print("- [ ] 图片数量一致（待验证）")

# 最终报告
print("\n## 📋 最终验证报告")
print("### ✅ 必检项（全部通过）")
print("| 检查项 | 状态 | 详情 |")
print("|--------|------|------|")
print("| 输出文件夹 | ✅ PASS | /Users/.../ |")
```

---

## 📍 检查点系统

| 检查点      | 位置   | 验证内容           | 失败操作                   |
| -------- | ---- | -------------- | ---------------------- |
| **CP 0** | 步骤0后 | MCP 可用性        | 询问用户：继续 (fallback) 或中止 |
| **CP 1** | 步骤1后 | 标题、作者、摘要已提取    | 重新解析或手动输入              |
| **CP 2** | 步骤2后 | 所有图片 URL 格式正确  | 重新收集                   |
| **CP 3** | 步骤3后 | 双栏 HTML 无溢出/留白 | 调整分页重新生成               |
| **CP 4** | 步骤5后 | 参考文献链接数量符合预期   | 记录警告但继续                |
| **CP 5** | 步骤7  | 通过各项检查         | ❌ 阻止交付                 |

---
 
## 第0步：依赖检查（MANDATORY - 阻塞性）

### ⚠️ 硬约束：docx skill 必须可用，MCP 检查不可跳过

**检查顺序**：

```
┌─────────────────────────────────────────────────────────────┐
│ 步骤0: 依赖检查                                             │
├─────────────────────────────────────────────────────────────┤
│ 1️⃣ docx skill（阻塞性 - 必须可用）                         │
│    └─ ❌ 失败 → 立即中止，提示用户安装                      │
├─────────────────────────────────────────────────────────────┤
│ 2️⃣ PubMed MCP（非阻塞 - 记录状态）                         │
│    └─ ❌ 失败 → 降级为仅用Google Scholar                   │
├─────────────────────────────────────────────────────────────┤
│ 3️⃣ Crossref MCP（非阻塞 - 记录状态）                       │
│    └─ ❌ 失败 → 降级为仅用DOI提取+Google Scholar           │
└─────────────────────────────────────────────────────────────┘
```

### 0.1 docx skill 检查（阻塞性）

```python
# 检查docx skill是否可用
try:
    # 尝试调用docx相关功能
    result = skill('docx')
    docx_skill_available = True
    print("✅ docx skill 可用")
except Exception as e:
    docx_skill_available = False
    print(f"❌ docx skill 不可用: {e}")
    print("\n请安装docx skill后重试：")
    print("  opencode skill add docx")
    raise Exception("缺少必要依赖：docx skill")
```

**失败处理**：docx skill 是核心依赖，不可用则立即中止流程。

### 0.2 MCP 可用性检查

```python
# 测试PubMed MCP
pubmed_test_passed = False
try:
    result = pubmed_search_pubmed_key_words(key_words="test", num_results=1)
    pubmed_test_passed = True
    print("✅ PubMed MCP 可用")
except Exception as e:
    print(f"⚠️ PubMed MCP 不可用: {e}")

# 测试Crossref MCP  
crossref_test_passed = False
try:
    result = crossref_search_works_by_query(query="test", limit=1)
    crossref_test_passed = True
    print("✅ Crossref MCP 可用")
except Exception as e:
    print(f"⚠️ Crossref MCP 不可用: {e}")
```

### 0.3 根据结果决定流程

| MCP 状态         | docx 状态  | 处理方式           | 参考文献策略                             |
| --------------- | --------- | ------------------ | ---------------------------------------- |
| ✅ 两者都可用   | ✅ 可用   | **完整流程** | DOI + PubMed + Crossref + Google Scholar |
| ⚠️ 仅一个可用 | ✅ 可用   | **部分流程** | DOI + 可用 MCP + Google Scholar           |
| ❌ 都不可用     | ✅ 可用   | **降级流程** | 仅 DOI 提取 + Google Scholar               |
| 任意            | ❌ 不可用 | **中止**     | 无法继续                                 |

### 0.4 MCP 不可用时的用户提示

```
⚠️ MCP服务不可用

检测结果：
- docx skill: ✅ 可用（核心功能正常）
- PubMed MCP: ❌ 不可用
- Crossref MCP: ❌ 不可用

影响：参考文献将只包含Google Scholar链接（无PubMed和Crossref链接）

选项：
1. 继续（使用fallback方案，仅Google Scholar链接）
2. 中止（我先安装MCP）

安装命令：
  claude mcp add pubmed -- npx -y @cyanheads/pubmed-mcp-server
  claude mcp add crossref -- npx -y @botanicastudios/crossref-mcp
```

### 📊 进度追踪

> 进度输出格式同上方「📊 进度追踪方式」

### ✅ CP 0检查点

- [ ] Docx skill 可用性已确认（阻塞性）
- [ ] PubMed MCP 状态已记录到变量
- [ ] Crossref MCP 状态已记录到变量
- [ ] 流程模式已确定（完整/部分/降级）

---

## 第1步：解析 Word 文档并确定简短标题

### 1.1 解析 Word 文档

使用 `skill('docx')` 加载 docx 技能，然后读取 Word 文档内容，提取以下结构化信息：

| 元素     | 识别方法                                 |
| -------- | ---------------------------------------- |
| 标题     | 第一个"Title"样式段落或前3段中最大字号   |
| 作者     | 标题后、单位前的逗号分隔姓名             |
| 单位     | 带上标编号的机构名称列表                 |
| 通讯作者 | 包含"Corresponding author: "或 Email 的段落 |
| 摘要     | "Abstract"标签后的结构化内容             |
| 关键词   | "Keywords: "开头的行                      |
| 正文章节 | 编号标题（1 INTRODUCTION, 2 METHODS 等）  |
| 图片     | 图片对象或 `[Figure N]` 占位符          |
| 表格     | Word 表格对象                             |
| 参考文献 | "REFERENCES"后的编号列表                 |

### 1.2 确定简短标题

**简化规则：**

| 规则     | 要求                                               |
| -------- | -------------------------------------------------- |
| 最大长度 | ≤ 50 字符                                         |
| 简化方法 | 提取核心关键词（疾病+研究主题+类型）               |
| 禁止字符 | 不要使用 `/ \ : * ? " < >                          |
| 格式     | 使用连字符分隔，如 `Ferroptosis-Cervical-Cancer` |

**示例：**

| 原标题                                                                                                                       | 简化后                          |
| ------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| Based on transcriptome analysis of novel prognosis and targeted therapy-related genes with ferroptosis in cervical cancer | Ferroptosis-Cervical-Cancer  |
| A comprehensive review of machine learning approaches in cardiovascular disease prediction                                | ML-Cardiovascular-Prediction |

### 1.3 用户确认

```javascript
question(questions=[{
  header: "简短标题",
  question: "请确认用于文件夹和图片URL的简短标题",
  options: [
    {label: "Ferroptosis-Cervical-Cancer", description: "推荐的简短标题（基于关键词提取）"},
    {label: "自定义", description: "手动输入其他名称"}
  ]
}])
```

### 📊 进度追踪

> 进度输出格式同上方「📊 进度追踪方式」

### ✅ CP 1检查点

- [ ] 标题已提取
- [ ] 作者已提取
- [ ] 摘要已提取
- [ ] 图片数量已统计
- [ ] 参考文献已提取

---

## 第2步：收集图片 URL

### 2.1 列出检测到的图片

**输出格式**：

```
检测到 4 张图片：
1. Figure 1 - The flowchart of the study
2. Figure 2 - Venny Plot
3. Figure 3 - Comprehensive analysis of gene expression signatures
4. Figure 4 - Enrichment analysis of key biological pathways
```

### 2.2 提供清晰的 URL 配置选项

```javascript
question(questions=[{
  header: "图片URL配置",
  question: "文档中共有 4 张图片，请选择URL配置方式",
  options: [
    {
      label: "使用默认URL格式（推荐）", 
      description: "https://medbam.org/assets/Ferroptosis-Cervical-Cancer（此前确定的简短标题）/Figure 1.png（注意：有空格）"
    },
    {
      label: "自定义基础路径", 
      description: "指定基础URL，图片文件名保持为 Figure 1.png, Figure 2.png 等"
    },
    {
      label: "逐一输入每张图片URL", 
      description: "完全自定义每张图片的URL"
    }
  ]
}])
```

### 2.3 根据用户选择收集 URL

**选项1：默认格式**

```
自动生成：
- https://medbam.org/assets/Ferroptosis-Cervical-Cancer（此前确定的简短标题）/Figure 1.png
……
```

**选项2：自定义基础路径**

```javascript
question(questions=[{
  header: "基础URL",
  question: "请输入图片基础URL（末尾不要加/）",
  options: [
    {label: "https://your-cdn.com/papers/2024", description: "示例格式"},
    {label: "自定义", description: "输入其他URL"}
  ]
}])

// 然后自动生成：
// {base_url}/Figure 1.png
// {base_url}/Figure 2.png
// ...
```

**选项3：逐一输入**

```
依次询问每张图片的完整URL（显示图片说明作为参考）
```

### 📊 进度追踪

> 进度输出格式同上方「📊 进度追踪方式」

### ✅ CP 2检查点

- [ ] 所有图片都有 URL
- [ ] URL 格式正确（包含协议、扩展名）
- [ ] 没有明显错误（如双斜杠、缺少扩展名等）

---

## 第3步：生成双栏分页 HTML

参考模板: `assets/template-two-column.html`
参考文档: `references/html-structure.md`

### ⚠️ 样式一致性规则 (MANDATORY - 最高优先级)

**核心原则：100%复制模板样式，杜绝随机性**

❌ **禁止推测或生成 CSS** - 不允许根据内容"推测"合适的样式
❌ **禁止美化样式** - 不允许使用 AI 生成的"优化"或"美化"样式
❌ **禁止修改模板** - 不允许修改 `template-two-column.html` 中的任何 CSS 属性

✅ **完全复制 `<style>` 标签** - 从 `template-two-column.html` 第7-280行完整复制整个 `<style>...</style>` 块
✅ **严格使用模板 class** - 所有元素必须使用模板中定义的 class 名称（如 `.section-title`, `.two-column`, `.side-by-side-figures`）
✅ **保留所有 inline style** - 模板中的所有 `style="..."` 属性必须原样保留

> 完整样式规则和CSS变量清单 参见 references/style-mapping.md § 全局样式变量 和 § 页面容器样式

---

### 分页核心原则 (CRITICAL - 必须严格执行)

> **分页时绝对不能溢出，也绝对不能留白！**

**分页规则:**

- 封面页：固定结构（期刊信息、标题、作者、摘要）
- 正文页：每页约800-1000字
- **禁止溢出**：内容绝不能超出页面边界
- **禁止留白**：页底空白不超过30 mm
- **表格溢出处理**：先压缩间距（参见步骤3.4 Phase 1），压缩不够再跨页分割（参见步骤3.4 Phase 2）

#### 🤖 人机协同流程（降本增效）

**目标：减少手动逐页复核的成本，用结构化摘要替代盲审**

```
Phase 1: AI生成初版 → 同时输出"分页摘要表"
Phase 2: 用户浏览器打开 → 仅检查摘要中标⚠️的页面（每页2秒）
Phase 3: 用户反馈问题页码（如"P5表格溢出"、"P8留白"）
Phase 4: AI精准修复 → 仅调整问题页及后续级联页
```

**AI 必须在生成双栏 HTML 后输出分页摘要表：**

```
📄 分页摘要：
| 页码 | 内容 | 表格行数 | 预估填充率 | 风险 |
|------|------|----------|-----------|------|
| P1 | 封面 | - | 固定 | ✅ |
| P2 | Introduction (550词) | - | 92% | ✅ |
| P3 | Methods + Table 1 (4行) | 4 | 88% | ✅ |
| P4 | Results 3.1 + Table 2 (25行) | 25 | 98% | ⚠️ 紧凑 |
| P5 | Table 2续 + 3.2 + Table 3 (15行) | 15 | 90% | ✅ |
| P6 | Table 3续 + 3.3 + Table 4 (10行) | 10 | 85% | ✅ |
| P7 | Table 4续 (28行, 压缩) | 28 | 95% | ⚠️ 已压缩 |
| ... | ... | ... | ... | ... |
```

**风险标注规则：**
- ✅ 填充率 ≤ 90% → 安全
- ⚠️ 填充率 90-98% → 紧凑，需用户目视确认
- ❌ 填充率 > 98% → 高风险，大概率溢出

这让用户只需关注标⚠️和❌的页面，而非逐页复核。

#### ⚠️ 分页失败的根本原因

**❌ 错误做法：让内容跨页面自动流动**

```html
<!-- ❌ 错误：多个页面共用一个连续容器 -->
<body>
    <div class="two-column">
        <!-- 内容从第1页一直延伸到第N页 -->
        <h1>INTRODUCTION</h1>
        <p>第1段...</p>
        ...
        <p>第50段...</p>  <!-- CSS会自动分页，但无法控制每页内容量 -->
    </div>
</body>
```

**问题所在：**

- CSS `column-count: 2` 会让内容在左右栏之间自动流动
- 当内容跨越多个页面时，CSS 无法控制每页包含多少内容
- 结果导致某些页面留白过多，某些页面内容溢出

**✅ 正确做法：每页独立生成，精确控制内容**

```html
<!-- ✅ 正确：每个<div class="page">独立，包含精确计算的内容 -->
<body>
    <!-- 第1页：封面 -->
    <div class="page">
        <div class="page-content">
            <h1>Title</h1>
            <div class="abstract">...</div>
        </div>
    </div>

    <!-- 第2页：INTRODUCTION（约550词） -->
    <div class="page">
        <div class="page-header">WANG ET AL.</div>
        <div class="page-content two-column">
            <h1 class="section-title">1 INTRODUCTION</h1>
            <p>第1段...</p>
            <p>第2段...</p>
            <p>第3段...</p>
            <p>第4段...</p>
            <!-- 内容经过计算，刚好填满页面，不溢出也不留白 -->
        </div>
        <div class="page-footer">2</div>
    </div>

    <!-- 第3页：METHODS开头 + 图片（约350词 + 2图） -->
    <div class="page">
        <div class="page-header">WANG ET AL.</div>
        <div class="page-content two-column">
            <h1 class="section-title">2 MATERIALS AND METHODS</h1>
            <h2 class="subsection-title">2.1 ...</h2>
            <p>...</p>

            <!-- 跨栏图片 -->
            <div class="side-by-side-figures">
                <figure>Figure 1</figure>
                <figure>Figure 2</figure>
            </div>

            <h2 class="subsection-title">2.2 ...</h2>
            <p>...</p>
            <!-- 同样经过精确计算 -->
        </div>
        <div class="page-footer">3</div>
    </div>

    <!-- 继续生成第4、5、6...页 -->
</body>
```

**关键区别：**

| 对比项              | ❌ 错误做法            | ✅ 正确做法                         |
| ------------------- | ---------------------- | ----------------------------------- |
| **页面结构**  | 所有内容在一个连续容器 | 每页一个独立 `<div class="page">` |
| **内容控制**  | CSS 自动分配            | 手动计算并分配每页内容              |
| **分页点**    | CSS 随机决定            | 根据字数精确规划                    |
| **留白/溢出** | 无法避免               | 可以精确控制                        |

**可以使用 CSS column，但必须满足：**

```css
/* ✅ 可以继续使用CSS column分栏 */
.two-column {
    column-count: 2;           /* 这个没问题 */
    column-gap: var(--column-gap);
    text-align: justify;
}
```

**但是 HTML 结构必须是：**

```html
<!-- ✅ 每页独立，内容经过精确计算 -->
<div class="page">
    <div class="page-content two-column">
        <!-- 这一页包含的内容必须经过字数计算 -->
        <!-- 确保既不溢出（超过252mm），也不留白（低于222mm） -->
    </div>
</div>

<div class="page">
    <div class="page-content two-column">
        <!-- 下一页的内容同样经过精确计算 -->
    </div>
</div>
```

**核心要点：**

1. ✅ **CSS `column-count: 2` 可以用** - 这不是问题所在
2. ✅ **关键是每页独立** - 每个 `<div class="page">` 必须手动创建
3. ✅ **内容必须精确计算** - 每页包含多少段落/图表必须事先规划
4. ✅ **禁止跨页连续容器** - 不能让一个 `.two-column` 容器跨越多个页面

### 步骤3.1：内容分析和分页规划

**CRITICAL** - 在生成 HTML 之前，必须先分析内容并规划分页，确保每页约600-900词（纯文字）或300-500词（含图表）。

> 完整分页规划流程（内容字数分析、页面计划数据结构、验证算法）参见 references/pagination-rules.md § 内容分析和分页规划

### 步骤3.2：手动创建每个页面

**CRITICAL** - 为每页手动创建独立的 `<div class="page">`，每页包含精确计算的内容（约600-900词纯文字或300-500词含图表）。

**⚠️ 禁止追加模式** - 必须一次性生成完整 HTML 字符串再写入文件，禁止多次调用 Edit/Write 逐页追加。

> 页面 HTML 构建模板和完整实施流程 参见 references/pagination-rules.md § 手动创建每个页面

> HTML 模板文件 参见 assets/template-two-column.html

### 步骤3.3：内容分割策略

**每页约600-800单词（纯文字）或300-400词（含图表）**

> 详细内容分割策略（高度计算、文字估算、图表空间、分页点选择）参见 references/pagination-rules.md § 内容分割策略

---

## 第4步：生成单栏连续 HTML

参考模板: `assets/template-single-column.html`

### ⚠️ 样式一致性规则 (MANDATORY - 最高优先级)

**与第3步相同，必须100%复制模板样式**

✅ **完全复制 `<style>` 标签** - 从 `template-single-column.html` 第7-124行完整复制整个 `<style>...</style>` 块
✅ **使用模板 inline style** - 所有元素的 `style="..."` 属性必须与模板完全一致
✅ **图片并排布局** - 连续出现的图片必须使用模板第251-260行的并排布局 CSS

> 样式规则同第3步，参见 references/style-mapping.md § 全局样式变量 和 § 图片样式

---

### 特点

- 单栏布局，**连续滚动，绝对不分页**
- 支持 `single-page-pdf` 类用于长页 PDF 生成
- **禁止任何分页符、page-break 或分页 CSS**

### 输出文件

`单栏连续-{简短标题}.html`

### 📊 进度追踪

> 进度输出格式同上方「📊 进度追踪方式」

---

## 第5步：添加参考文献链接（双栏+单栏均执行）

### 5.0 选择验证模式（新增优化）

**💡 让用户根据需求选择验证深度，平衡速度和完整性**

```javascript
AskUserQuestion({
  questions: [{
    question: `参考文献验证模式选择（共${ref_count}条文献）`,
    header: "验证模式",
    multiSelect: false,
    options: [
      {
        label: "⚡ 快速模式（推荐）",
        description: `仅Google Scholar链接 + DOI提取 | 预计<10秒`
      },
      {
        label: "⚖️ 标准模式",
        description: `DOI提取 + Crossref验证 + Scholar | 预计30-60秒`
      },
      {
        label: "🔬 完整模式",
        description: `PubMed + Crossref + Scholar完整验证 | 预计2-5分钟`
      }
    ]
  }]
})
```

**模式对比**：

| 模式      | DOI 提取 | PubMed  | Crossref   | Google Scholar | 耗时    | MCP 调用 |
| --------- | ------- | ------- | ---------- | -------------- | ------- | ------- |
| ⚡ 快速   | ✅ 本地 | ❌      | ❌         | ✅ 总是        | <10秒   | 0次     |
| ⚖️ 标准 | ✅ 本地 | ❌      | ✅ 无 DOI 时 | ✅ 总是        | 30-60秒 | ~15次   |
| 🔬 完整   | ✅ 本地 | ✅ 全部 | ✅ 无 DOI 时 | ✅ 总是        | 2-5分钟 | ~40次   |

### 执行策略（严格遵守优先级）

```
优先级1: DOI提取（本地，0 MCP调用）
   ↓
优先级2: PubMed查询（优先使用DOI）
   ↓
优先级3: Crossref查询（仅无DOI时）
   ↓
优先级4: Google Scholar（总是生成）
```

### 步骤5.1-5.5：参考文献链接验证

**执行策略**：
- ✅ 提取已有 DOI → 生成 Crossref 链接
- ✅ PubMed MCP 查询（有 DOI 用 term，无 DOI 用 title+author）
- ✅ Crossref MCP 查询（仅无 DOI 文献，80%标题匹配阈值）
- ✅ Google Scholar 链接（总是生成）
- ❌ 禁止臆造 DOI/PMID
- ❌ 低置信度匹配（<80%）必须跳过

**输出格式**：
- 双栏版：DOI 蓝色链接（`#005a8c`），无元数据行
- 单栏版：DOI 蓝色链接 + 元数据行（PubMed | Scholar | Crossref）

> 完整实现逻辑（DOI提取正则、PubMed策略A/B、Crossref查询、Scholar链接生成、verify_links.py脚本用法）参见 references/reference-links.md § 详细实现逻辑

### 📊 进度追踪（实时更新）

> 进度输出格式同上方「📊 进度追踪方式」

### ✅ CP 4检查点

- [ ] Google Scholar 链接 = 参考文献总数（30条）
- [ ] PubMed 链接 >= 0（记录实际数量）
- [ ] Crossref 链接 >= DOI 提取数量
- [ ] 已尝试验证所有文献（有记录）

---

## 第6步：输出最终文件

### 输出目录

`/Users/jikunren/Documents/期刊排版/{简短标题}/`

### 输出结构

```
/Users/jikunren/Documents/期刊排版/Ferroptosis-Cervical-Cancer/
├── 双栏分页-Ferroptosis-Cervical-Cancer.html
└── 单栏连续-Ferroptosis-Cervical-Cancer.html
```

### 📊 进度追踪

> 进度输出格式同上方「📊 进度追踪方式」

---

## 第7步：最终验证（BLOCKING - 门控机制）

### 强制检查项-源文件比对验证

**此步骤必须重新读取源 DOCX 文件，逐项比对确保没有内容丢失或新增：**

```
验证流程：
1. 重新读取源DOCX文件（使用docx skill）
2. 提取关键计数并与HTML对比：
   ├─ 各章节段落数（逐章对比）
   ├─ 每个表格的行数（逐表对比）
   ├─ 参考文献总条数
   ├─ 图片总数
   └─ back matter各小节（Acknowledgments, Author Contribution等）
3. 差异项标红报告
4. 如有差异 → 阻止交付，修复后重新验证
```

**比对输出格式示例：**

```
📋 源文件比对结果：
| 内容项 | 源DOCX | 双栏HTML | 单栏HTML | 状态 |
|--------|--------|----------|----------|------|
| Introduction段落数 | 5 | 5 | 5 | ✅ |
| Methods段落数 | 8 | 8 | 8 | ✅ |
| Table 2行数 | 26 | 26 | 26 | ✅ |
| Table 3行数 | 21 | 21 | 21 | ✅ |
| 参考文献条数 | 33 | 33 | 33 | ✅ |
| 图片数 | 0 | 0 | 0 | ✅ |
| back matter小节 | 6 | 6 | 6 | ✅ |
→ ✅ 全部一致，可交付
```

### 其他检查项

| 检查项          | 通过标准               | 失败处理                   |
| --------------- | ---------------------- | -------------------------- |
| PubMed 链接      | 已尝试验证（有记录）   | WARN: 未执行 PubMed 验证     |
| Crossref 链接    | 链接数 >= DOI 提取数    | WARN: Crossref 链接少于预期 |
| 图片 URL 可访问性 | 随机抽取3张验证200状态 | WARN: 部分图片不可访问     |

