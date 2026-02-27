# 期刊排版技能 (journal-typesetting) 创建计划

## TL;DR

> **Quick Summary**: 创建一个将Word学术论文转换为MedBA Medicine期刊HTML格式的skill，输出双栏分页版(PDF)和单栏连续版(在线预览，含参考文献元数据链接)。
> 
> **唯一权威安装路径**: `~/.config/opencode/skills/journal-typesetting/`
> **打包输出**: `/Users/jikunren/Documents/期刊排版/journal-typesetting.skill`
> 
> **Deliverables** (所有相对路径基于上述安装路径):
> - `SKILL.md` - 主技能文件
> - `assets/template-two-column.html` - 双栏分页模板
> - `assets/template-single-column.html` - 单栏连续模板
> - `references/html-structure.md` - HTML结构参考
> - `references/reference-links.md` - 参考文献链接生成指南
> - `scripts/verify_links.py` - 链接验证脚本
> 
> **Estimated Effort**: Large
> **Parallel Execution**: YES - 3 waves
> **Critical Path**: Task 1 → Task 3 → Task 5 → Task 6 → Task 7
> 
> **注意**: 当前工作目录非git repo，所有"Commit"操作改为"本地保存验证"，不执行git命令

---

## Context

### Original Request
用户要求创建一个skill，将Word文档转换为期刊规定的HTML格式。需要：
1. 解析用户上传的Word文档
2. 向用户询问图片URL
3. 生成双栏分页HTML (供PDF下载)
4. 生成单栏连续HTML (供在线预览)
5. 为单栏版本添加参考文献元数据链接 (PubMed | Google Scholar | Crossref)
6. 所有链接必须经过验证确保有效

### Interview Summary
**Key Discussions**:
- 参考文献链接处理: 只添加可用链接，缺失则不显示
- 语言支持: 中英文双语
- 链接验证: 必须100%验证每个链接可访问
- 期刊信息: 使用MedBA Medicine默认配置
- 图片URL: 批量询问所有图片URL
- 分页控制: A4规格，智能分页，不溢出不大幅留白

**Research Findings**:
- 模板使用内联CSS，主题色 #005a8c
- 字体: Times New Roman (正文), Arial (标题)
- 参考文献链接格式已从`单栏连续-供在线预览.html`提取
- 部分参考文献可能缺少PubMed或Crossref链接

### Metis Review
**Identified Gaps** (addressed):
- Word文档结构变化 → 使用docx skill的robust解析
- 链接验证超时 → 添加5秒超时和并行请求
- 分页算法 → 基于内容量估算，保留20mm底部边距
- 图片URL数量不匹配 → 验证数量并要求确认
- 中文参考文献搜索 → 使用标题搜索Google Scholar

---

## DOCX to HTML Mapping Rules (Momus Gap Fix)

> **Critical**: This section defines concrete extraction logic for transforming Word document elements to HTML structure.

### Document Structure Detection

| Word Element | Detection Method | HTML Output |
|--------------|------------------|-------------|
| **Title** | First paragraph styled "Title" OR largest font size in first 3 paragraphs | `<h1 class="article-title">` |
| **Authors** | Paragraphs between title and first numbered superscript, comma-separated names | `<p class="authors"><span class="author">Name<sup>1</sup></span>` |
| **Affiliations** | Numbered paragraphs (1, 2, 3...) following author list, smaller font | `<div class="affiliations"><p><sup>1</sup>Institution...</p>` |
| **Corresponding Author** | Contains "Corresponding author:" or "*" marker with email | `<div class="corresponding-author">` |
| **Abstract** | Section labeled "Abstract" (case-insensitive) | `<div class="abstract-box">` |
| **Abstract Subsections** | Bold text followed by colon (Background:, Methods:, Results:, Conclusion:) | `<h3>Background</h3><p>content</p>` |
| **Keywords** | Line starting with "Keywords:" or "Key words:" | `<p class="keywords"><strong>Keywords:</strong>...` |
| **Section Headings** | Numbered patterns: "1 INTRODUCTION", "2 METHODS", "2.1 Subheading" | `<h1>` for level 1, `<h2>` for level 2 |
| **Figures** | Image objects OR `[Figure N]` placeholder text | Collect placeholders, ask user for URLs |
| **Figure Captions** | "Figure N." or "Fig. N." followed by description | `<p class="figure-caption"><strong>Figure 1.</strong>...` |
| **Tables** | Word table objects | `<table class="three-line-table">` |
| **Table Captions** | "Table N." followed by description (above table) | `<p class="table-caption"><strong>Table 1.</strong>...` |
| **References** | Section "REFERENCES" followed by numbered list [1], [2]... | `<div class="references"><p class="reference">...` |

### Reference Parsing Rules

Each reference must be parsed to extract:
```
[Reference Number] Authors. Title. Journal. Year;Volume(Issue):Pages. DOI if present.
```

**Extraction Pattern**:
1. **Number**: Leading `[N]` or `N.` 
2. **Authors**: Text until first period after number
3. **Title**: Text between first period and journal name (detect by: italics, or pattern like "J Xyz" or known journal names)
4. **DOI**: Pattern `10.\d{4,}/[^\s]+` anywhere in reference
5. **PMID**: Pattern `PMID:\s*(\d+)` if present

### Image Placeholder Format

When images detected but not embeddable:
```
[Figure 1: original_filename.png - NEED URL]
[Figure 2: chart.jpg - NEED URL]
```

User will be asked:
```
请提供以下图片的URL链接:
- Figure 1 (original_filename.png): ___
- Figure 2 (chart.jpg): ___
```

---

## Pagination Algorithm (Momus Gap Fix)

> **Critical**: Concrete rules for A4 page breaking in two-column layout.

### Page Dimensions
- **Paper**: A4 (210mm × 297mm)
- **Margins**: Top 20mm, Bottom 20mm, Left 15mm, Right 15mm
- **Content Area**: 180mm × 257mm
- **Column Width**: 87mm each (with 6mm gutter)

### Content Estimation Rules

| Element | Estimated Height |
|---------|------------------|
| Paragraph (per 100 chars) | ~8mm |
| Section Heading (H1) | 12mm (including spacing) |
| Subsection Heading (H2) | 8mm (including spacing) |
| Figure (standard) | 80-120mm (varies) |
| Table (per row) | 6mm |
| Reference (per item) | 10mm |

### Page Break Decision Rules

```
RULE 1: Cover Page
- Cover page (封面) is FIXED structure - never split
- Contains: header, title, authors, affiliations, abstract
- If abstract exceeds page, break AFTER abstract-box closes

RULE 2: Section Start
- New H1 section always starts new page IF less than 80mm remaining
- New H1 section can start mid-page IF > 80mm remaining

RULE 3: Figures
- IF figure height > 60% remaining page height → page break BEFORE figure
- Figures stay with their captions (never separate)
- Side-by-side figures (flex layout) treated as single unit

RULE 4: Tables
- Tables NEVER split across pages
- IF table height > remaining page height → page break BEFORE table
- Table caption stays with table

RULE 5: Paragraphs
- Prefer breaking at paragraph boundaries
- NEVER break mid-sentence
- Keep at least 3 lines of paragraph on each page (no orphans/widows)

RULE 6: References
- References section can flow across pages
- Break between reference items, never mid-reference

RULE 7: Whitespace Tolerance
- Maximum allowed whitespace at page bottom: 30mm
- If whitespace > 30mm, try pulling next element up
```

### Implementation Strategy

Since templates use manual `<div class="page">` structure:
1. Generate all content first
2. Estimate cumulative height per element
3. Insert `</div><div class="page">` when threshold reached
4. Adjust based on element type rules above

---

## Work Objectives

### Core Objective
创建一个完整的OpenCode skill，使Claude能够将Word学术论文自动转换为MedBA Medicine期刊格式的HTML文件。

### Concrete Deliverables
1. `~/.config/opencode/skills/journal-typesetting/` 目录及完整内容
2. 可打包的`.skill`文件

### Definition of Done
- [x] `ls ~/.config/opencode/skills/journal-typesetting/SKILL.md` → 文件存在
- [x] `grep "name: journal-typesetting" ~/.config/opencode/skills/journal-typesetting/SKILL.md` → 匹配成功
- [x] `ls ~/.config/opencode/skills/journal-typesetting/assets/*.html | wc -l` → 输出 2
- [x] `ls ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py` → 文件存在
- [ ] 使用skill处理示例Word文档成功生成两个HTML文件

### Functional Acceptance Criteria (End-to-End Verification)

> **CRITICAL**: These are agent-executable steps to verify the skill works with real documents.

**Step 1: Skill Installation Verification**
```bash
# Verify skill is discoverable by OpenCode
ls ~/.config/opencode/skills/journal-typesetting/SKILL.md
# Assert: File exists, exit code 0

# Verify YAML frontmatter is valid
head -20 ~/.config/opencode/skills/journal-typesetting/SKILL.md | grep -E "^name:|^description:"
# Assert: Both name and description present
```

**Step 2: Link Verification Script Functional Test**
```bash
# Test with known valid PubMed ID
python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --test-pubmed 21351269
# Assert: Output contains "valid" or "VALID" or "200", exit code 0

# Test with known valid DOI
python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --test-doi "10.1002/ijc.25516"
# Assert: Output contains "valid" or "VALID" or "200", exit code 0

# Test with invalid PMID (should report invalid)
python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --test-pubmed 99999999999
# Assert: Output contains "invalid" or "not_found", exit code 0 (graceful failure)
```

**Step 3: Template Integrity Check**
```bash
# Verify two-column template has page structure
grep -c 'class="page"' ~/.config/opencode/skills/journal-typesetting/assets/template-two-column.html
# Assert: Output >= 1

# Verify single-column template has reference link format
grep -E "PubMed.*Google Scholar|Google Scholar.*PubMed" ~/.config/opencode/skills/journal-typesetting/assets/template-single-column.html
# Assert: Match found (reference link format example exists)
```

**Step 4: Skill Invocation Test (Manual but Structured)**
```
After skill is installed, invoke via OpenCode with test document:
1. Load skill: /journal-typesetting
2. Provide: /Users/jikunren/Documents/期刊排版/Yan Wang Proof1.docx
3. Follow prompts to provide image URLs (or skip if no images)
4. Verify outputs:
   - ls /Users/jikunren/Documents/期刊排版/双栏分页-*.html | wc -l → 1
   - ls /Users/jikunren/Documents/期刊排版/单栏连续-*.html | wc -l → 1
5. Verify reference links in single-column output:
   - grep -c "pubmed.ncbi.nlm.nih.gov" /Users/jikunren/Documents/期刊排版/单栏连续-*.html → >= 1
   - grep -c "scholar.google.com" /Users/jikunren/Documents/期刊排版/单栏连续-*.html → >= 1
```

### Must Have
- SKILL.md包含完整的YAML frontmatter和工作流程指导
- 双栏分页和单栏连续两个HTML模板
- 参考文献链接验证脚本
- 图片URL批量收集流程
- 分页控制逻辑说明

### Must NOT Have (Guardrails)
- NO 自动DOI生成 - 只使用参考文献中明确的DOI或API查找的DOI
- NO 图片下载/处理 - 只使用用户提供的URL
- NO 参考文献格式修改 - 只添加链接，不改变原文
- NO 自动翻译 - 不翻译章节标题或内容
- NO 其他数据库链接 - 只支持PubMed, Google Scholar, Crossref
- NO 嵌入式图片处理 - 必须使用外部URL
- NO ORCID自动查找 - 只使用Word文档中明确的ORCID

---

## Verification Strategy (MANDATORY)

### Test Decision
- **Infrastructure exists**: NO (创建新skill)
- **User wants tests**: Manual-only (skill通过实际使用验证)
- **Framework**: N/A

### Automated Verification (Agent-Executable)

**Skill文件验证**:
```bash
# 验证SKILL.md存在且格式正确
head -20 ~/.config/opencode/skills/journal-typesetting/SKILL.md | grep -E "^name:|^description:"
# Assert: 输出包含 "name: journal-typesetting" 和 description 行

# 验证模板文件存在
ls ~/.config/opencode/skills/journal-typesetting/assets/
# Assert: 输出包含 template-two-column.html 和 template-single-column.html

# 验证脚本存在且可执行
python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --help
# Assert: 输出帮助信息，无错误
```

**链接验证脚本测试**:
```bash
# 测试PubMed链接验证
python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --test-pubmed 21351269
# Assert: 输出 "VALID" 或类似成功信息

# 测试Crossref链接验证
python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --test-doi "10.1002/ijc.25516"
# Assert: 输出 "VALID" 或类似成功信息
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately):
├── Task 1: 创建skill目录结构和SKILL.md框架
├── Task 2: 创建双栏分页模板
└── Task 3: 创建单栏连续模板

Wave 2 (After Wave 1):
├── Task 4: 创建参考文献链接指南
├── Task 5: 创建链接验证脚本
└── Task 6: 创建HTML结构参考文档

Wave 3 (After Wave 2):
└── Task 7: 完善SKILL.md主体内容，整合所有资源

Final:
└── Task 8: 测试并打包skill
```

### Dependency Matrix

| Task | Depends On | Blocks | Can Parallelize With |
|------|------------|--------|---------------------|
| 1 | None | 7, 8 | 2, 3 |
| 2 | None | 7 | 1, 3 |
| 3 | None | 7 | 1, 2 |
| 4 | None | 7 | 5, 6 |
| 5 | None | 7, 8 | 4, 6 |
| 6 | None | 7 | 4, 5 |
| 7 | 1, 2, 3, 4, 5, 6 | 8 | None |
| 8 | 7 | None | None |

### Agent Dispatch Summary

| Wave | Tasks | Recommended Agents |
|------|-------|-------------------|
| 1 | 1, 2, 3 | delegate_task(category="quick", load_skills=["skill-creator"], run_in_background=true) |
| 2 | 4, 5, 6 | dispatch parallel after Wave 1 completes |
| 3 | 7 | sequential, requires all previous |
| Final | 8 | sequential, final verification |

---

## TODOs

- [x] 1. 创建skill目录结构和SKILL.md框架

  **What to do**:
  - 运行 `scripts/init_skill.py journal-typesetting --path ~/.config/opencode/skills/` 初始化skill目录
  - 编辑SKILL.md的YAML frontmatter:
    ```yaml
    ---
    name: journal-typesetting
    description: |
      将Word学术论文转换为MedBA Medicine期刊HTML格式。支持双栏分页(PDF下载)和单栏连续(在线预览)两种输出。
      自动为参考文献添加验证后的元数据链接(PubMed | Google Scholar | Crossref)。
      使用场景：当用户提供Word格式的学术论文并要求排版为期刊HTML格式时使用。
      触发词：排版、期刊、MedBA、Word转HTML、论文格式化、学术论文排版
    ---
    ```
  - 保留SKILL.md body为占位符，等待后续任务填充

  **Must NOT do**:
  - 不要填写SKILL.md的完整body内容（留给Task 7）
  - 不要创建assets/scripts/references目录外的文件

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 简单的目录创建和文件初始化
  - **Skills**: [`skill-creator`]
    - `skill-creator`: 包含init_skill.py脚本和skill创建指南

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Tasks 7, 8
  - **Blocked By**: None

  **References**:
  - `skill-creator` skill中的 `scripts/init_skill.py` - 初始化脚本位置
  - skill-creator skill文档 - YAML frontmatter格式要求

  **Acceptance Criteria**:
  ```bash
  ls ~/.config/opencode/skills/journal-typesetting/
  # Assert: 输出包含 SKILL.md, assets/, scripts/, references/
  
  head -10 ~/.config/opencode/skills/journal-typesetting/SKILL.md
  # Assert: 输出包含 "name: journal-typesetting"
  ```

  **Commit**: YES
  - Message: `feat(skill): initialize journal-typesetting skill structure`
  - Files: `~/.config/opencode/skills/journal-typesetting/*`

---

- [x] 2. 创建双栏分页HTML模板

  **What to do**:
  - 将 `/Users/jikunren/Documents/期刊排版/双栏分页-模板.html` 复制为 `assets/template-two-column.html`
  - 保留所有CSS变量和类定义
  - 添加清晰的TODO注释标记需要替换的内容:
    - `<!-- TODO: 替换为文章标题 -->`
    - `<!-- TODO: 替换作者信息 -->`
    - 等等
  - 确保所有样式内联，无外部引用

  **Must NOT do**:
  - 不要修改CSS样式值
  - 不要删除任何HTML注释说明
  - 不要添加外部CSS/JS引用

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 文件复制和简单编辑
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - `/Users/jikunren/Documents/期刊排版/双栏分页-模板.html` - 源模板文件
  - `/Users/jikunren/Documents/期刊排版/双栏分页-供pdf下载.html` - 工作示例

  **Acceptance Criteria**:
  ```bash
  ls ~/.config/opencode/skills/journal-typesetting/assets/template-two-column.html
  # Assert: 文件存在

  grep -c "class=\"page\"" ~/.config/opencode/skills/journal-typesetting/assets/template-two-column.html
  # Assert: 输出 >= 1 (至少有一个page div)

  grep -c "TODO:" ~/.config/opencode/skills/journal-typesetting/assets/template-two-column.html
  # Assert: 输出 >= 5 (有多个TODO占位符)
  ```

  **Commit**: NO (groups with Task 1)

---

- [x] 3. 创建单栏连续HTML模板

  **What to do**:
  - 将 `/Users/jikunren/Documents/期刊排版/单栏连续-模板.html` 复制为 `assets/template-single-column.html`
  - 保留参考文献链接格式示例（作为注释）
  - 添加TODO注释标记
  - 确保包含single-page-pdf类支持

  **Must NOT do**:
  - 不要修改CSS样式
  - 不要删除参考文献链接格式注释

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 文件复制和简单编辑
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - `/Users/jikunren/Documents/期刊排版/单栏连续-模板.html` - 源模板文件
  - `/Users/jikunren/Documents/期刊排版/单栏连续-供在线预览.html:370-399` - 参考文献链接示例

  **Acceptance Criteria**:
  ```bash
  ls ~/.config/opencode/skills/journal-typesetting/assets/template-single-column.html
  # Assert: 文件存在

  grep -c "single-page-pdf" ~/.config/opencode/skills/journal-typesetting/assets/template-single-column.html
  # Assert: 输出 >= 1

  grep "PubMed.*Google Scholar.*Crossref" ~/.config/opencode/skills/journal-typesetting/assets/template-single-column.html
  # Assert: 匹配成功 (包含链接格式示例)
  ```

  **Commit**: NO (groups with Task 1)

---

- [x] 4. 创建参考文献链接生成指南

  **What to do**:
  - 创建 `references/reference-links.md`
  - 内容包括:
    - PubMed API使用说明 (通过标题搜索获取PMID)
    - Google Scholar URL构造方法
    - Crossref DOI提取和URL构造
    - 链接格式示例
    - 处理缺失链接的策略
    - 中文参考文献特殊处理

  **Must NOT do**:
  - 不要包含实际的API密钥
  - 不要包含过时的API端点

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 文档编写
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5, 6)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - `/Users/jikunren/Documents/期刊排版/单栏连续-供在线预览.html:370-399` - 现有链接格式
  - PubMed E-utilities API文档: https://www.ncbi.nlm.nih.gov/books/NBK25499/
  - Crossref API: https://api.crossref.org/

  **Acceptance Criteria**:
  ```bash
  ls ~/.config/opencode/skills/journal-typesetting/references/reference-links.md
  # Assert: 文件存在

  grep -c "PubMed" ~/.config/opencode/skills/journal-typesetting/references/reference-links.md
  # Assert: 输出 >= 3

  grep -c "Google Scholar" ~/.config/opencode/skills/journal-typesetting/references/reference-links.md
  # Assert: 输出 >= 2
  ```

  **Commit**: NO (groups with Task 1)

---

- [x] 5. 创建链接验证脚本

  **What to do**:
  - 创建 `scripts/verify_links.py`
  - 功能:
    - 验证PubMed链接 (HTTP HEAD请求)
    - 验证Crossref/DOI链接 (HTTP HEAD请求)
    - 验证Google Scholar链接构造正确性
    - 支持批量验证
    - 5秒超时
    - 返回JSON格式结果
  - 添加命令行参数支持 `--test-pubmed`, `--test-doi`

  **Link Verification Protocol (CRITICAL)**:
  
  | HTTP Response | Classification | Action |
  |---------------|----------------|--------|
  | 200 OK | VALID | Use link |
  | 301/302 Redirect | VALID (follow) | Follow up to 3 redirects, use final URL |
  | 403 Forbidden | INVALID | Skip this link type |
  | 404 Not Found | INVALID | Skip this link type |
  | 429 Too Many Requests | RETRY | Wait 2s, retry once, then skip |
  | Timeout (>5s) | INVALID | Skip this link type |
  | Connection Error | INVALID | Skip this link type |

  **Rate Limiting Protocol**:
  - Max 3 concurrent HTTP requests
  - 500ms delay between request batches
  - Respect Retry-After header if present
  - Use User-Agent: "MedBA-Journal-Typesetter/1.0"

  **Search Disambiguation Rules**:
  - **PubMed Search**: Use title search via E-utilities API
    - If 1 result: Use that PMID
    - If multiple results: Compare titles, use if >80% string similarity (Levenshtein ratio)
    - If 0 results or no good match: Skip PubMed link
  - **Crossref Search**: Use title search via API
    - If DOI in reference: Validate directly
    - If searching by title: Use first result if title match >80%
    - If no match: Skip Crossref link
  - **Google Scholar**: Always generate (search URL, no validation needed)
    - URL encode title: `https://scholar.google.com/scholar?q={urlencode(title)}`

  **Output Format**:
  ```json
  {
    "reference_number": 1,
    "original_text": "Author et al. Title...",
    "links": {
      "pubmed": {"url": "https://pubmed.ncbi.nlm.nih.gov/12345/", "status": "valid"},
      "crossref": {"url": null, "status": "not_found"},
      "google_scholar": {"url": "https://scholar.google.com/scholar?q=...", "status": "generated"}
    }
  }
  ```

  **Must NOT do**:
  - 不要使用需要API密钥的端点
  - 不要阻塞超过5秒/链接
  - 不要使用未验证的链接

  **Recommended Agent Profile**:
  - **Category**: `unspecified-low`
    - Reason: 简单Python脚本编写
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 6)
  - **Blocks**: Tasks 7, 8
  - **Blocked By**: None

  **References**:
  - PubMed链接格式: `https://pubmed.ncbi.nlm.nih.gov/{PMID}/`
  - Crossref链接格式: `https://doi.org/{DOI}`
  - Google Scholar格式: `https://scholar.google.com/scholar?q={encoded_title}`

  **Acceptance Criteria**:
  ```bash
  python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --help
  # Assert: 输出帮助信息，退出码0

  python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --test-pubmed 21351269
  # Assert: 输出包含 "valid" 或 "200"

  python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --test-doi "10.1002/ijc.25516"
  # Assert: 输出包含 "valid" 或 "200"
  ```

  **Commit**: NO (groups with Task 1)

---

- [x] 6. 创建HTML结构参考文档

  **What to do**:
  - 创建 `references/html-structure.md`
  - 内容包括:
    - 封面页元素结构 (日期、DOI、标题、作者、摘要等)
    - 正文页元素结构 (章节、图表、表格)
    - CSS类说明
    - 分页控制策略 (A4规格，内容量估算)
    - 双栏vs单栏差异

  **Must NOT do**:
  - 不要重复模板文件中的完整CSS
  - 不要包含具体示例数据

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 文档编写
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 4, 5)
  - **Blocks**: Task 7
  - **Blocked By**: None

  **References**:
  - `/Users/jikunren/Documents/期刊排版/双栏分页-模板.html` - 双栏结构
  - `/Users/jikunren/Documents/期刊排版/单栏连续-模板.html` - 单栏结构

  **Acceptance Criteria**:
  ```bash
  ls ~/.config/opencode/skills/journal-typesetting/references/html-structure.md
  # Assert: 文件存在

  wc -l ~/.config/opencode/skills/journal-typesetting/references/html-structure.md
  # Assert: 输出 >= 50 (足够详细)
  ```

  **Commit**: NO (groups with Task 1)

---

- [x] 7. 完善SKILL.md主体内容

  **What to do**:
  - 编写完整的SKILL.md body内容
  - 包含工作流程:
    1. 使用docx skill解析Word文档
    2. 提取所有结构化内容
    3. 列出所有图片，批量询问URL
    4. 生成双栏分页HTML
    5. 生成单栏连续HTML
    6. 为参考文献搜索并验证元数据链接
    7. 添加验证后的链接到单栏版本
  - 引用资源文件:
    - `assets/template-two-column.html`
    - `assets/template-single-column.html`
    - `references/html-structure.md`
    - `references/reference-links.md`
    - `scripts/verify_links.py`
  - 包含关键guardrails和错误处理

  **Must NOT do**:
  - 不要超过500行
  - 不要重复references文件中的详细内容
  - 不要添加"When to Use"部分（已在description中）

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: 技术文档编写，需要整合多个资源
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (Wave 3)
  - **Blocks**: Task 8
  - **Blocked By**: Tasks 1, 2, 3, 4, 5, 6

  **References**:
  - 所有之前创建的资源文件
  - `/Users/jikunren/Documents/期刊排版/Yan Wang Proof1.docx` - 示例Word文档
  - docx skill文档 - Word解析方法

  **Acceptance Criteria**:
  ```bash
  wc -l ~/.config/opencode/skills/journal-typesetting/SKILL.md
  # Assert: 输出 < 500 且 > 100

  grep -c "docx" ~/.config/opencode/skills/journal-typesetting/SKILL.md
  # Assert: 输出 >= 2 (提到docx skill)

  grep -c "template-two-column.html" ~/.config/opencode/skills/journal-typesetting/SKILL.md
  # Assert: 输出 >= 1 (引用模板)

  grep -c "verify_links.py" ~/.config/opencode/skills/journal-typesetting/SKILL.md
  # Assert: 输出 >= 1 (引用脚本)
  ```

  **Commit**: YES
  - Message: `feat(skill): complete journal-typesetting skill content`
  - Files: `~/.config/opencode/skills/journal-typesetting/SKILL.md`

---

- [x] 8. 测试并打包skill

  **What to do**:
  - 验证所有文件存在且格式正确
  - 运行链接验证脚本测试
  - 运行 `scripts/package_skill.py ~/.config/opencode/skills/journal-typesetting`
  - 确认生成 `journal-typesetting.skill` 文件

  **Must NOT do**:
  - 不要跳过验证步骤
  - 不要强制打包忽略错误

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 运行脚本和验证
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Final
  - **Blocks**: None
  - **Blocked By**: Task 7

  **References**:
  - skill-creator中的 `scripts/package_skill.py` - 打包脚本

  **Acceptance Criteria**:
  ```bash
  python3 /Users/jikunren/.config/opencode/skills/skill-creator/scripts/package_skill.py ~/.config/opencode/skills/journal-typesetting
  # Assert: 输出 "Package created" 或类似成功信息

  ls *.skill 2>/dev/null || ls ~/.config/opencode/skills/journal-typesetting.skill
  # Assert: .skill文件存在
  ```

  **Commit**: YES
  - Message: `feat(skill): package journal-typesetting skill v1.0`
  - Files: `journal-typesetting.skill`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `feat(skill): initialize journal-typesetting skill structure` | SKILL.md, dirs | ls验证 |
| 7 | `feat(skill): complete journal-typesetting skill content` | SKILL.md | wc验证 |
| 8 | `feat(skill): package journal-typesetting skill v1.0` | .skill | 文件存在 |

---

## Success Criteria

### Verification Commands
```bash
# 1. Skill目录完整
ls -la ~/.config/opencode/skills/journal-typesetting/
# Expected: SKILL.md, assets/, scripts/, references/

# 2. 模板文件存在
ls ~/.config/opencode/skills/journal-typesetting/assets/
# Expected: template-two-column.html, template-single-column.html

# 3. 验证脚本可运行
python3 ~/.config/opencode/skills/journal-typesetting/scripts/verify_links.py --test-pubmed 21351269
# Expected: 输出包含有效性确认

# 4. Skill可打包
# (由Task 8执行)
```

### Final Checklist
- [x] SKILL.md有完整的name和description
- [x] 两个HTML模板包含所有必需元素
- [x] 参考文献链接指南覆盖PubMed/Google Scholar/Crossref
- [x] 验证脚本可正常运行
- [x] 所有资源文件被SKILL.md正确引用
- [x] Skill可成功打包
