# Decisions - MCP Integration

## [2026-01-30T08:05:34Z] MCP Package Selection

### Decision
Use `@cyanheads/pubmed-mcp-server` and `@botanicastudios/crossref-mcp`

### Rationale
- Both packages already installed by user
- Both support npx for zero-install execution
- PubMed MCP provides comprehensive search and fetch capabilities
- Crossref MCP supports both DOI validation and title search

### Alternatives Considered
- Direct API calls (original approach) - rejected because MCP provides better abstraction
- Other MCP implementations - rejected because these are already installed

---

## [2026-01-30T08:05:34Z] Keep Google Scholar Without MCP

### Decision
Do not add MCP for Google Scholar, keep URL encoding approach

### Rationale
- Google Scholar doesn't have an official API
- URL construction via encoding is simple and reliable
- No MCP server available for Google Scholar
- Current approach works well

---

## [2026-01-30T08:05:34Z] Add Playwright to Evaluation System

### Decision
Add Playwright-based HTML rendering check as part of evaluation workflow

### Rationale
- Visual bugs can't be caught by static analysis
- Need to verify actual browser rendering
- Screenshots provide evidence for QA
- Aligns with hands-on verification best practices
