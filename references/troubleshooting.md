# 故障排除指南

## 常见问题与解决方案

### 1. MCP服务问题

#### 问题：PubMed MCP连接失败
**错误信息**：`PubMed MCP 不可用: Connection refused`

**解决方案**：
```bash
# 1. 检查MCP是否已安装
claude mcp list

# 2. 如果未安装，执行安装
claude mcp add pubmed -- npx -y @cyanheads/pubmed-mcp-server

# 3. 重启Claude Code
# 退出并重新启动CLI
```

**替代方案**：
- 选择"快速模式"跳过PubMed验证
- 仅使用Google Scholar链接

---

#### 问题：Crossref MCP超时
**错误信息**：`Crossref查询超时 (>10秒)`

**解决方案**：
```bash
# 1. 检查网络连接
ping api.crossref.org

# 2. 重新安装MCP
claude mcp remove crossref
claude mcp add crossref -- npx -y @botanicastudios/crossref-mcp

# 3. 如果问题持续，选择"标准模式"减少查询次数
```

---

### 2. docx skill问题

#### 问题：docx skill未安装
**错误信息**：`缺少必要依赖：docx skill`

**解决方案**：
```bash
# 安装docx skill
opencode skill add docx

# 验证安装
opencode skill list | grep docx
```

---

#### 问题：Word文档解析失败
**错误信息**：`Word解析失败: 无法读取文档`

**可能原因**：
1. 文档损坏或密码保护
2. 文档格式不支持（.doc而非.docx）
3. 文件路径包含特殊字符

**解决方案**：
```bash
# 1. 检查文档是否可用pandoc打开
pandoc your-document.docx -o test.md

# 2. 如果失败，尝试用Word重新保存为.docx
# 3. 确保文件路径不含中文或特殊字符
```

---

### 3. 图片URL问题

#### 问题：图片URL验证失败
**错误信息**：`Figure 1: ❌ 404 Not Found`

**检查清单**：
- [ ] 图片是否已上传至服务器？
- [ ] URL是否拼写正确？
- [ ] 服务器是否允许外部访问？
- [ ] URL中的空格是否正确处理？

**解决方案**：
```bash
# 1. 手动验证URL可访问性
curl -I "https://medbam.org/assets/Figure 1.png"

# 2. 如果URL中有空格，浏览器会自动处理为%20
# 直接使用 "Figure 1.png" 即可，无需手动编码

# 3. 检查服务器CORS设置
```

---

#### 问题：图片在HTML中不显示
**可能原因**：相对路径错误

**解决方案**：
- 确保使用绝对URL（以`https://`开头）
- 不要使用相对路径如`./images/figure1.png`

---

### 4. HTML生成问题

#### 问题：双栏HTML内容溢出
**现象**：文字超出页面边界

**解决方案**：
1. 检查图片是否过大（建议宽度<180mm）
2. 检查表格是否过宽
3. 手动调整分页位置（在问题段落前添加分页符）

```css
/* 临时修复：在HTML中添加强制分页 */
<div style="break-before: page;"></div>
```

---

#### 问题：HTML文件写入失败
**错误信息**：`文件大小检测 ERROR`

**可能原因**：
- 文件超过30KB但使用了write工具
- 磁盘空间不足
- 权限问题

**解决方案**：
```bash
# 1. 检查磁盘空间
df -h ~/Documents/期刊排版/

# 2. 检查目录权限
ls -la ~/Documents/期刊排版/

# 3. 手动创建目录
mkdir -p ~/Documents/期刊排版/Test-Article/
```

---

### 5. 参考文献问题

#### 问题：参考文献格式无法识别
**现象**：DOI提取失败，无法生成链接

**支持的格式**：
```
✅ [1] Author. Title[J]. Journal, 2020,10(1):1-10. DOI:10.xxxx/xxxx
✅ [2] Author. Title. Journal. 2020;10(1):1-10. https://doi.org/10.xxxx/xxxx
❌ [3] Author (2020). Title. Journal 10(1), 1-10.
```

**解决方案**：
- 使用编号格式 [1], [2], [3]...
- DOI应在文献末尾
- 如果格式不规范，只会生成Google Scholar链接

---

#### 问题：参考文献链接验证太慢
**现象**：步骤5耗时超过5分钟

**解决方案**：
```bash
# 1. 切换到"快速模式"或"标准模式"
# 2. 减少参考文献数量（>100条会很慢）
# 3. 检查网络连接速度
```

---

### 6. 验证失败

#### 问题：CP5检查点失败 - 图片数量不匹配
**错误信息**：`图片数量 ❌ FAIL | 3张（预期4张）`

**排查步骤**：
1. 检查原Word文档中实际图片数量
2. 确认所有图片URL都已配置
3. 搜索HTML中的`<img>`标签数量

```bash
# 统计HTML中的图片数量
grep -o '<img' output.html | wc -l
```

**解决方案**：
- 重新收集图片URL（步骤2）
- 手动添加缺失的图片HTML代码

---

#### 问题：Google Scholar链接缺失
**错误信息**：`Google Scholar链接 ❌ FAIL | 25/30条`

**解决方案**：
```python
# 手动生成缺失的链接
import urllib.parse

def generate_scholar_link(title):
    query = urllib.parse.quote(title)
    return f"https://scholar.google.com/scholar?q={query}"

# 示例
link = generate_scholar_link("Ferroptosis cell death")
print(link)
```

---

### 7. 性能问题

#### 问题：整个流程耗时过长（>15分钟）

**优化建议**：
1. **选择快速模式**：跳过MCP验证，仅用Google Scholar
2. **减少图片URL验证**：跳过可访问性检查
3. **检查MCP响应速度**：测试单次查询耗时

```bash
# 测试PubMed MCP响应时间
time python scripts/verify_links.py --test-pubmed 12345678
```

---

### 8. 文件路径问题

#### 问题：输出目录不存在
**错误信息**：`输出文件夹已创建 ❌ FAIL`

**解决方案**：
```bash
# 手动创建默认输出目录
mkdir -p ~/Documents/期刊排版/

# 或指定自定义输出路径（需修改skill配置）
export JOURNAL_OUTPUT_DIR="/path/to/custom/dir"
```

---

## 获取帮助

如果以上方案都无法解决问题，请：

1. **查看详细日志**：skill执行过程中的所有输出
2. **收集错误信息**：完整的错误堆栈
3. **提供示例文件**：最小可复现案例

**报告问题**：
- GitHub Issues: [提交问题](https://github.com/yourusername/journal-typesetting/issues)
- 包含信息：系统版本、Claude Code版本、错误日志、Word文档样本（脱敏）

---

## 快速诊断命令

```bash
# 一键检查所有依赖
echo "=== 依赖检查 ==="
echo "1. docx skill:"
opencode skill list | grep -q docx && echo "✅ 已安装" || echo "❌ 未安装"

echo "2. PubMed MCP:"
claude mcp list | grep -q pubmed && echo "✅ 已配置" || echo "❌ 未配置"

echo "3. Crossref MCP:"
claude mcp list | grep -q crossref && echo "✅ 已配置" || echo "❌ 未配置"

echo "4. 输出目录:"
[ -d ~/Documents/期刊排版 ] && echo "✅ 存在" || echo "❌ 不存在"

echo "5. 磁盘空间:"
df -h ~/ | awk 'NR==2 {print $4 " 可用"}'
```

运行这个脚本可以快速诊断环境问题。
