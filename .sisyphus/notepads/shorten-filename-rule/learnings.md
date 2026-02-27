## [2026-01-30T08:45:00Z] Task: Update SKILL.md Step 6 - Add Filename Length Limit

### Problem Identified
Users encountered JSON parsing errors when article titles exceeded ~100 characters:
```
invalid [tool=write, error=Invalid input for tool write: JSON parsing failed...
```

Example long title:
"Based on transcriptome analysis of novel prognosis and targeted therapy-related genes with ferroptosis in cervical cancer"

### Solution Implemented
Added filename length limit rules to Step 6 of SKILL.md:

1. **Maximum length**: 50 characters for folder names
2. **Simplification principles**:
   - Keep disease names
   - Keep core research topics
   - Keep research types
   - Remove redundant words (based on, comprehensive, novel, related)

3. **Examples added**:
   - Ferroptosis-Cervical-Cancer
   - ML-Cardiovascular-Prediction
   - NSCLC-Immunotherapy-Outcomes

4. **User confirmation flow**: Added `question` tool example to confirm simplified names

### Files Modified
- `/Users/jikunren/.config/opencode/skills/journal-typesetting/SKILL.md`
  - Lines 248-251: Updated output directory rules
  - Added new subsection: "文件夹/文件命名规则（重要！）"
  - Updated all examples to use {简短标题} instead of {文章标题}
  - Added long title example with simplification

### Verification Results
```bash
grep -c "文件夹名 ≤ 50 字符" SKILL.md  # Returns: 1 ✓
grep -c "Ferroptosis-Cervical-Cancer" SKILL.md  # Returns: 7 ✓
grep "question(questions=" SKILL.md  # Found ✓
```

### Key Decision
50 characters limit ensures total path stays under 200 chars even with Chinese prefixes "双栏分页-" (10 chars) or "单栏连续-" (10 chars).

### Lessons Learned
- File path length limits can cause JSON parsing errors in tools
- Always provide simplification guidelines for user-generated content used in file paths
- Confirm simplified names with users to maintain accuracy
