# 参考文献链接生成指南

本文档说明如何为参考文献添加元数据链接（PubMed | Google Scholar | Crossref）。

## 链接类型

### 1. PubMed 链接

**URL格式**: `https://pubmed.ncbi.nlm.nih.gov/{PMID}/`

**获取方法**:
1. 使用 NCBI E-utilities API 通过标题搜索
2. API端点: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
3. 参数: `db=pubmed&term={title}[Title]&retmode=json`

**示例**:
```
原始参考文献: Ferlay J, et al. Estimates of worldwide burden of cancer in 2008...
搜索查询: Estimates of worldwide burden of cancer in 2008[Title]
返回PMID: 21351269
最终URL: https://pubmed.ncbi.nlm.nih.gov/21351269/
```

**特殊处理**:
- 如果搜索返回多个结果，比较标题相似度（>80%才使用）
- 如果没有找到匹配，不添加PubMed链接
- 中文参考文献可能没有PubMed记录

### 2. Google Scholar 链接

**URL格式**: `https://scholar.google.com/scholar?q={encoded_title}`

**生成方法**:
1. 提取参考文献标题
2. URL编码标题
3. 构造搜索URL

**示例**:
```
标题: Estimates of worldwide burden of cancer in 2008
编码后: Estimates+of+worldwide+burden+of+cancer+in+2008
URL: https://scholar.google.com/scholar?q=Estimates+of+worldwide+burden+of+cancer+in+2008
```

**注意**: 
- Google Scholar链接总是可以生成（搜索链接）
- 不需要验证，因为是搜索而非直接链接
- 中文标题也支持

### 3. Crossref/DOI 链接

**URL格式**: `https://doi.org/{DOI}`

**获取方法**:

**方式A - 参考文献中已有DOI**:
1. 使用正则表达式提取: `10\.\d{4,}/[^\s]+`
2. 直接构造URL

**方式B - 通过Crossref API搜索**:
1. API端点: `https://api.crossref.org/works`
2. 参数: `?query.title={title}&rows=1`
3. 从返回结果中提取DOI

**示例**:
```
参考文献中DOI: 10.1002/ijc.25516
最终URL: https://doi.org/10.1002/ijc.25516
```

## 链接验证协议

### HTTP响应处理

| 响应码 | 分类 | 处理 |
|--------|------|------|
| 200 OK | 有效 | 使用链接 |
| 301/302 重定向 | 有效 | 跟随重定向，使用最终URL |
| 403 Forbidden | 无效 | 跳过此链接类型 |
| 404 Not Found | 无效 | 跳过此链接类型 |
| 429 Too Many Requests | 重试 | 等待2秒后重试一次 |
| 超时(>5秒) | 无效 | 跳过此链接类型 |

### 速率限制

- 最大并发请求: 3个
- 请求批次间隔: 500ms
- User-Agent: `MedBA-Journal-Typesetter/1.0`

## HTML输出格式

```html
<div style="margin-bottom:2mm;padding-left:1.5em;text-indent:-1.5em;font-size:8pt;line-height:1.3;">
  [1] Author Name, et al. Article Title[J]. Journal Name, Year,Volume(Issue):Pages.<br>
  <a href="https://pubmed.ncbi.nlm.nih.gov/12345678/" target="_blank" style="color:#005a8c;text-decoration:none;">PubMed</a> | 
  <a href="https://scholar.google.com/scholar?q=Article+Title" target="_blank" style="color:#005a8c;text-decoration:none;">Google Scholar</a> | 
  <a href="https://doi.org/10.xxxx/xxxxx" target="_blank" style="color:#005a8c;text-decoration:none;">Crossref</a>
</div>
```

## 缺失链接处理

只显示可用的链接，缺失的不显示分隔符:

```html
<!-- 只有PubMed和Google Scholar -->
<a href="...">PubMed</a> | <a href="...">Google Scholar</a>

<!-- 只有Google Scholar -->
<a href="...">Google Scholar</a>

<!-- 只有Crossref -->
<a href="...">Crossref</a>
```

## 中文参考文献

- PubMed: 中文文献通常无记录，跳过
- Google Scholar: 使用中文标题搜索，正常生成
- Crossref: 如有DOI则使用，否则跳过
---

## 🔧 详细实现逻辑（从 SKILL.md 第5步提取）

以下内容从 SKILL.md 步骤5完整提取，提供参考文献链接生成的具体实现细节。

### 步骤5.1：提取已有 DOI（本地处理）

```python
import re

def extract_doi(reference_text):
    """从参考文献中提取DOI"""
    doi_pattern = r'10\.\d{4,}/[^\s\]\)]+'
    match = re.search(doi_pattern, reference_text)
    return match.group(0) if match else None

# 示例
ref = "Dixon S, et al. Cell, 2012,149(5). DOI:10.1016/j.cell.2012.03.042."
doi = extract_doi(ref)  # "10.1016/j.cell.2012.03.042"
```

**已有 DOI 的参考文献**：

- ✅ 直接生成 Crossref 链接：`https://doi.org/{DOI}`
- ✅ 无需 MCP 验证

### 步骤5.2：PubMed 查询（使用 MCP）

**仅当 `mcp_pubmed_available == True` 时执行**

**策略 A：有 DOI 的文献**

```python
# 通过DOI搜索（精确度高）
result = pubmed_search_pubmed_advanced(
    term=doi,  # 使用DOI作为搜索词
    num_results=1
)
```

**策略 B：无 DOI 的文献**

```python
# 通过标题+作者搜索
result = pubmed_search_pubmed_advanced(
    title=extracted_title,
    author=first_author,  # 可选
    num_results=3  # 返回多个结果进行匹配验证
)

# 验证匹配度
for article in result:
    similarity = calculate_title_similarity(extracted_title, article['title'])
    if similarity > 0.8:  # 80%相似度阈值
        pmid = article['pmid']
        break
```

**超时/失败处理**：

- ⏱️ 超时（>10秒）→ 记录警告，跳过该文献的 PubMed 链接
- ❌ 无结果 → 跳过 PubMed 链接
- ⚠️ 低置信度匹配 → 跳过，不添加链接

### 步骤5.3：Crossref 查询（使用 MCP）

**仅当 `mcp_crossref_available == True` 且文献无 DOI 时执行**

```python
# 通过标题搜索DOI
result = crossref_search_works_by_query(
    query=extracted_title,
    limit=3  # 限制返回结果数
)

# 验证匹配度
for work in result.get("message", {}).get("items", []):
    title_match = calculate_title_similarity(extracted_title, work.get('title', [''])[0])
    year_match = check_year_consistency(reference_year, work.get('published-print', {}).get('date-parts', [[None]])[0][0])
  
    if title_match > 0.8 and year_match:
        doi = work['DOI']
        break
```

**硬约束**：

- ❌ 禁止臆造 DOI/PMID
- ❌ 低置信度匹配（<80%）必须跳过
- 📝 每次 MCP 调用失败必须记录日志

### 步骤5.4：生成 Google Scholar 链接（总是执行）

```python
import urllib.parse

def generate_scholar_link(reference_text):
    """生成Google Scholar搜索链接"""
    # 提取标题或使用全文
    title = extract_title(reference_text) or reference_text[:100]
    encoded = urllib.parse.quote(title)
    return f"https://scholar.google.com/scholar?q={encoded}"
```

**无需验证，总是可以生成**

### 链接输出格式

#### 双栏分页版（DOI 蓝色链接，无元数据行）

```html
<!-- 有DOI的参考文献 -->
<div>[1] Ferlay J, Shin HR, Bray F, et al. Estimates of worldwide burden of cancer in 2008: GLOBOCAN 2008[J]. Int J Cancer, 2010,127(12):2893-917. DOI: <a href="https://doi.org/10.1002/ijc.25516" target="_blank" style="color:#005a8c;text-decoration:none;">10.1002/ijc.25516</a>.</div>

<!-- 无DOI的参考文献（不附加DOI文本） -->
<div>[16] Wikipedia contributors. Adverse event. 2025. Available from: https://en.wikipedia.org/wiki/Adverse_event.</div>
```

**规则：**
- ✅ 每条有 DOI 的参考文献末尾添加 `DOI: <a href="..." style="color:#005a8c;text-decoration:none;">10.xxxx/xxxxx</a>.`
- ✅ DOI 链接文本为蓝色（`#005a8c`），无下划线
- ❌ 双栏版不添加 PubMed/Scholar/Crossref 元数据行（分页空间有限）
- ❌ 无 DOI 的参考文献不附加 DOI 文本

#### 单栏连续版（DOI 蓝色链接 + 元数据行）

```html
<div style="margin-bottom:2.5mm;padding-left:1.5em;text-indent:-1.5em;">
  [1] Ferlay J, Shin HR, Bray F, et al. Estimates of worldwide burden of cancer in 2008: GLOBOCAN 2008[J]. Int J Cancer, 2010,127(12):2893-917. DOI: <a href="https://doi.org/10.1002/ijc.25516" target="_blank" style="color:#005a8c;text-decoration:none;">10.1002/ijc.25516</a>.<br>
  <a href="https://pubmed.ncbi.nlm.nih.gov/21351269/" target="_blank" style="color:#005a8c;text-decoration:none;">PubMed</a> |
  <a href="https://scholar.google.com/scholar?q=Ferlay+GLOBOCAN+cancer+2008" target="_blank" style="color:#005a8c;text-decoration:none;">Google Scholar</a> |
  <a href="https://doi.org/10.1002/ijc.25516" target="_blank" style="color:#005a8c;text-decoration:none;">Crossref</a>
</div>
```

**规则：**
- ✅ DOI 同样以蓝色链接显示在参考文献正文末尾
- ✅ 元数据链接（PubMed | Scholar | Crossref）在下一行显示
- ✅ 只显示可用的链接，缺失的不显示

### 第5.5步：链接批量验证（使用 verify_links. Py 脚本）

#### 脚本位置

`scripts/verify_links.py`

#### 使用场景

- 批量验证生成的所有参考文献链接是否可访问
- 调试链接验证失败问题
- 手动验证特定 DOI 或 PMID

#### 命令示例

```bash
# 验证特定PubMed ID是否有效
python scripts/verify_links.py --test-pubmed 21351269

# 验证特定DOI是否有效
python scripts/verify_links.py --test-doi "10.1002/ijc.25516"

# 通过标题搜索PubMed获取PMID
python scripts/verify_links.py --search-pubmed "Estimates of worldwide burden of cancer"

# 生成Google Scholar搜索URL
python scripts/verify_links.py --generate-scholar "Ferroptosis cell death mechanisms"

# 以JSON格式输出（便于程序处理）
python scripts/verify_links.py --test-pubmed 21351269 --json
```

#### 输出格式

```
PubMed 21351269: VALID (valid, HTTP 200)
URL: https://pubmed.ncbi.nlm.nih.gov/21351269/

DOI 10.1002/ijc.25516: VALID (valid, HTTP 200)
URL: https://doi.org/10.1002/ijc.25516
Title: Estimates of worldwide burden of cancer in 2008

Found PMID: 21351269
URL: https://pubmed.ncbi.nlm.nih.gov/21351269/

Google Scholar URL: https://scholar.google.com/scholar?q=Ferroptosis+cell+death+mechanisms
```

#### 批量验证所有生成的链接：

```python
# 示例：批量验证所有PubMed链接
for pmid in collected_pmids:
    result = bash(command=f"python scripts/verify_links.py --test-pubmed {pmid} --json")
    data = json.loads(result)
    if not data[0]["valid"]:
        print(f"⚠️ PubMed {pmid} 验证失败: {data[0]['status']}")
```
