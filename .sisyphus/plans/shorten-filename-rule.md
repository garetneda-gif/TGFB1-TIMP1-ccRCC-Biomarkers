# 添加文件夹/文件名长度限制规则

## TL;DR

> **Quick Summary**: 更新 journal-typesetting SKILL.md 第6步，添加文件名长度限制规则，避免JSON解析错误
> 
> **Deliverables**: 
> - 更新 SKILL.md 第6步输出规则
> 
> **Estimated Effort**: Quick
> **Parallel Execution**: NO - sequential
> **Critical Path**: Task 1

---

## Context

### Original Request
用户在执行排版任务时遇到 JSON 解析错误：
```
invalid [tool=write, error=Invalid input for tool write: JSON parsing failed...
```

原因是文章标题过长（超过100字符），导致文件路径过长。

### 问题分析
- 文件路径中包含完整的长标题
- 例如："Based on transcriptome analysis of novel prognosis and targeted therapy-related genes with ferroptosis in cervical cancer"
- 这导致 JSON 字符串解析失败

---

## Work Objectives

### Core Objective
在 SKILL.md 第6步添加文件夹/文件名长度限制规则

### Concrete Deliverables
- 更新 `/Users/jikunren/.config/opencode/skills/journal-typesetting/SKILL.md`

### Definition of Done
- [x] 第6步包含文件名长度限制规则（≤50字符）
- [x] 包含标题简化示例
- [x] 包含询问用户确认的流程

---

## TODOs

- [x] 1. 更新 SKILL.md 第6步输出规则

  **What to do**:
  将第6步的输出规则从：
  ```
  2. **文件夹名称**必须为**文章标题**
  ```
  改为：
  ```
  2. **文件夹名称**使用**简短标题**（≤50字符）
  ```
  
  添加以下内容：
  
  #### 文件夹/文件命名规则（重要！）
  
  **⚠️ 标题过长会导致JSON解析错误，必须缩短！**
  
  | 规则 | 要求 |
  |------|------|
  | **最大长度** | 文件夹名 ≤ 50 字符 |
  | **简化方法** | 提取核心关键词，去除冗余修饰语 |
  | **禁止字符** | 不要使用 `/ \ : * ? " < > |` |
  
  **简化标题示例：**
  
  | 原标题 | 简化后 |
  |--------|--------|
  | Based on transcriptome analysis of novel prognosis and targeted therapy-related genes with ferroptosis in cervical cancer | Ferroptosis-Cervical-Cancer |
  | A comprehensive review of machine learning approaches in cardiovascular disease prediction | ML-Cardiovascular-Prediction |
  
  **简化原则：**
  1. 保留**疾病名称**
  2. 保留**核心研究主题**
  3. 保留**研究类型**
  4. 删除**冗余词汇**（如 based on, comprehensive, novel, related）
  
  **⚠️ 如标题过长，必须先询问用户确认简化后的名称！**

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`journal-typesetting`]

  **References**:
  - `SKILL.md:246-269` - 当前第6步输出规则

  **Acceptance Criteria**:
  - [x] 第6步包含"文件夹名 ≤ 50 字符"规则
  - [x] 包含标题简化示例表格
  - [x] 包含简化原则说明
  - [x] 包含询问用户确认的 question 工具示例

  **Commit**: YES
  - Message: `feat(skill): add filename length limit rule to prevent JSON parsing errors`
  - Files: `SKILL.md`

---

## Success Criteria

### Final Checklist
- [x] 第6步输出规则已更新
- [x] 包含长度限制（≤50字符）
- [x] 包含简化示例和原则
