# 更新 Journal-Typesetting Skill - MCP集成

## TL;DR

> **Quick Summary**: 为期刊排版技能添加PubMed和Crossref MCP集成，实现自动化参考文献链接验证
> 
> **Deliverables**:
> - 更新SKILL.md添加MCP配置
> - 更新第5步参考文献链接部分，使用MCP工具
> - 更新评估系统，集成Playwright验证
> 
> **Estimated Effort**: Quick
> **Parallel Execution**: NO - sequential
> **Critical Path**: Task 1 → Task 2 → Task 3

---

## Context

### Original Request
用户要求为journal-typesetting技能添加MCP集成：
1. PubMed MCP - 验证PMID
2. Crossref MCP - 验证DOI
3. Playwright - 检查HTML渲染效果

### Research Findings
- `@cyanheads/pubmed-mcp-server` - 成熟的PubMed MCP，支持搜索和验证
- `@botanicastudios/crossref-mcp` - Crossref MCP，支持DOI验证
- Playwright已在系统中可用

---

## Work Objectives

### Core Objective
将MCP工具集成到期刊排版技能中，实现参考文献链接的自动化验证

### Concrete Deliverables
- 更新后的 `/Users/jikunren/.config/opencode/skills/journal-typesetting/SKILL.md`

### Definition of Done
- [x] SKILL.md包含MCP配置
- [x] 第5步使用MCP工具进行链接验证
- [x] 评估系统使用Playwright进行HTML检查

---

## Verification Strategy

### If Automated Verification Only (NO User Intervention)

**验证方式**: 文件内容检查
```bash
# 检查SKILL.md是否包含MCP配置
grep -q "mcp:" /Users/jikunren/.config/opencode/skills/journal-typesetting/SKILL.md
# 检查是否包含pubmed配置
grep -q "pubmed" /Users/jikunren/.config/opencode/skills/journal-typesetting/SKILL.md
# 检查是否包含crossref配置
grep -q "crossref" /Users/jikunren/.config/opencode/skills/journal-typesetting/SKILL.md
```

---

## TODOs

- [x] 1. 更新SKILL.md frontmatter添加MCP配置

  **What to do**:
  - 在frontmatter中添加mcp配置块
  - 配置pubmed MCP: `npx @cyanheads/pubmed-mcp-server`
  - 配置crossref MCP: `npx -y @botanicastudios/crossref-mcp`

  **Must NOT do**:
  - 不要删除现有配置

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`journal-typesetting`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 2, Task 3
  - **Blocked By**: None

  **References**:
  - `SKILL.md:1-8` - 当前frontmatter结构

  **Acceptance Criteria**:
  - [ ] SKILL.md frontmatter包含mcp配置
  - [ ] `grep -q "mcp:" SKILL.md` 返回成功

  **Commit**: YES
  - Message: `feat(journal-typesetting): add MCP configuration for PubMed and Crossref`
  - Files: `SKILL.md`

---

- [x] 2. 更新第5步参考文献链接验证流程

  **What to do**:
  - 将手动API调用替换为MCP工具调用
  - 添加skill_mcp调用示例
  - 更新PubMed验证：使用pubmed MCP的`pubmed_search_articles`和`pubmed_fetch_contents`
  - 更新Crossref验证：使用crossref MCP的`get_work_by_doi`

  **Must NOT do**:
  - 不要删除Google Scholar链接生成逻辑（无MCP）

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`journal-typesetting`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: Task 3
  - **Blocked By**: Task 1

  **References**:
  - `SKILL.md:118-156` - 当前第5步内容

  **Acceptance Criteria**:
  - [ ] 第5步包含skill_mcp调用示例
  - [ ] PubMed验证使用MCP工具
  - [ ] Crossref验证使用MCP工具

  **New Content for Step 5**:
  ```markdown
  ### 第5步：添加参考文献链接（使用MCP工具）

  **⚠️ 链接验证核心原则（必须严格遵守）:**

  > **每一条参考文献链接都必须通过MCP工具验证，杜绝偷懒或臆造！**

  #### 使用PubMed MCP验证

  ```javascript
  // 1. 搜索文章获取PMID
  skill_mcp({
    mcp_name: "pubmed",
    tool_name: "pubmed_search_articles",
    arguments: {
      query: "文章标题关键词",
      max_results: 3
    }
  })

  // 2. 验证PMID对应的文章信息
  skill_mcp({
    mcp_name: "pubmed",
    tool_name: "pubmed_fetch_contents",
    arguments: {
      pmids: ["12345678"]
    }
  })
  ```

  #### 使用Crossref MCP验证DOI

  ```javascript
  // 通过DOI获取文章详情验证
  skill_mcp({
    mcp_name: "crossref",
    tool_name: "get_work_by_doi",
    arguments: {
      doi: "10.1000/xyz123"
    }
  })

  // 或通过标题搜索
  skill_mcp({
    mcp_name: "crossref",
    tool_name: "search_works_by_title",
    arguments: {
      title: "文章标题",
      rows: 3
    }
  })
  ```

  **验证流程:**
  1. 对每条参考文献，先尝试提取DOI
  2. 如有DOI → 使用Crossref MCP验证
  3. 如无DOI → 使用标题搜索Crossref
  4. 同时使用PubMed MCP搜索验证PMID
  5. 只有MCP返回结果匹配原文献时，才添加链接
  ```

  **Commit**: YES
  - Message: `feat(journal-typesetting): integrate MCP tools for reference link validation`
  - Files: `SKILL.md`

---

- [x] 3. 更新评估系统添加Playwright HTML检查

  **What to do**:
  - 在第7步评估系统中添加Playwright检查
  - 添加HTML渲染验证步骤
  - 添加截图保存功能

  **Must NOT do**:
  - 不要删除现有评估项

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`journal-typesetting`, `playwright`]

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential
  - **Blocks**: None
  - **Blocked By**: Task 2

  **References**:
  - `SKILL.md:261-342` - 当前评估系统

  **Acceptance Criteria**:
  - [ ] 评估系统包含Playwright检查步骤
  - [ ] 包含截图保存指南

  **New Content to Add**:
  ```markdown
  ### 8. HTML渲染检查（使用Playwright）

  **加载playwright skill后执行以下检查:**

  ```javascript
  // 1. 打开双栏分页HTML
  // 使用playwright浏览器打开本地HTML文件

  // 2. 检查页面渲染
  // - 截图保存到 .sisyphus/evidence/
  // - 检查是否有内容溢出
  // - 检查页面高度是否符合A4比例

  // 3. 打开单栏连续HTML
  // - 滚动到底部确认无分页
  // - 截图保存
  ```

  | 检查项 | 状态 | 备注 |
  |--------|------|------|
  | 双栏版渲染正常 | ✅/❌ | 截图: evidence/two-column.png |
  | 单栏版渲染正常 | ✅/❌ | 截图: evidence/single-column.png |
  | 无视觉溢出 | ✅/❌ | |
  | 图片加载正常 | ✅/❌ | |
  ```

  **Commit**: YES
  - Message: `feat(journal-typesetting): add Playwright HTML rendering validation to evaluation`
  - Files: `SKILL.md`

---

## Commit Strategy

| After Task | Message | Files | Verification |
|------------|---------|-------|--------------|
| 1 | `feat(journal-typesetting): add MCP configuration` | SKILL.md | grep mcp |
| 2 | `feat(journal-typesetting): integrate MCP tools` | SKILL.md | grep skill_mcp |
| 3 | `feat(journal-typesetting): add Playwright validation` | SKILL.md | grep playwright |

---

## Success Criteria

### Verification Commands
```bash
# 检查MCP配置
grep -A5 "mcp:" ~/.config/opencode/skills/journal-typesetting/SKILL.md

# 检查skill_mcp调用
grep "skill_mcp" ~/.config/opencode/skills/journal-typesetting/SKILL.md

# 检查Playwright集成
grep -i "playwright" ~/.config/opencode/skills/journal-typesetting/SKILL.md
```

### Final Checklist
- [x] MCP配置已添加到frontmatter
- [x] 第5步使用skill_mcp进行链接验证
- [x] 评估系统包含Playwright HTML检查
- [x] 所有更新与现有内容兼容
