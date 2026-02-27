# Learnings - MCP Integration for journal-typesetting skill

## [2026-01-30T08:05:34Z] Task: MCP Integration

### Successful Approaches

1. **MCP Configuration in YAML Frontmatter**
   - MCP configuration goes in skill frontmatter under `mcp:` key
   - Each MCP server has `command` and `args` fields
   - Format:
     ```yaml
     mcp:
       server_name:
         command: npx
         args: ["package-name"]
     ```

2. **Skill MCP Function Calls**
   - Use `skill_mcp()` function to call MCP tools
   - Syntax:
     ```javascript
     skill_mcp({
       mcp_name: "server_name",
       tool_name: "tool_function",
       arguments: { ... }
     })
     ```

3. **Documentation Structure for MCP Integration**
   - Provide concrete code examples, not just descriptions
   - Include both search and validation workflows
   - Specify exact tool names and argument structures
   - Keep original workflow context while adding MCP calls

### Patterns That Work

- **PubMed MCP workflow**: Search → Fetch → Validate
  - `pubmed_search_articles` for initial search
  - `pubmed_fetch_contents` for detailed validation
  
- **Crossref MCP workflow**: DOI-first, fallback to title search
  - `get_work_by_doi` when DOI available
  - `search_works_by_title` when no DOI

- **Playwright Integration**: Specify evidence paths upfront
  - Screenshots saved to `.sisyphus/evidence/`
  - Clear file naming: `two-column.png`, `single-column.png`

### Conventions Established

- MCP configs use npx for zero-install execution
- Keep Google Scholar without MCP (simple URL encoding sufficient)
- Validation checklists updated to reference MCP tools instead of raw APIs
- Evaluation systems should include visual QA via Playwright for HTML outputs
