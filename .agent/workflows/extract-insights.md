---
description: 从processing提取精华内容生成投资笔记
---

# 提取洞察 /extract-insights

此工作流用于从 `processing` 文件夹提取高价值内容，生成精选笔记保存到 `output` 文件夹。

## 使用方法

```
/extract-insights [重要性过滤]
```

### 参数
- `重要性过滤`：可选，可选值为 high/medium/low/all，默认为 high

### 示例
```
/extract-insights high   # 只提取高重要性内容
/extract-insights all    # 提取所有内容
/extract-insights        # 默认提取高重要性内容
```

## 执行步骤

1. 查看 processing 中待提取的文件
```bash
// turbo
ls /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/processing/
```

2. 运行洞察提取脚本
```bash
cd /Users/mac/Desktop/my-ccm-projects/ai-analysis-system && python -c "from skills import extract_insights; print(extract_insights())"
```

3. 查看生成的笔记
```bash
// turbo
ls /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/output/notes/
```

## 输出

- 在 `output/notes/` 文件夹生成 `YYYY-MM-DD-投资笔记.md` 文件
- 包含洞察概览、详细洞察和行动建议

## 工作流意义

这是三层文件夹流水线的最后一步：
1. `input/` → AI分析 → `processing/`
2. `processing/` → 人工筛选 + AI提取 → `output/`
3. `output/` 中的内容成为可复用的知识库
