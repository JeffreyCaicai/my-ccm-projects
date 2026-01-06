---
description: 分析财经新闻，生成分析报告
---

# 分析财经新闻 /analyze-news

此工作流用于分析 `input` 文件夹中的财经新闻，生成分析报告保存到 `processing` 文件夹。

## 使用方法

```
/analyze-news [日期]
```

### 参数
- `日期`：可选，格式为 YYYY-MM-DD，默认为今天

### 示例
```
/analyze-news 2026-01-05
/analyze-news  # 分析今日新闻
```

## 执行步骤

1. 扫描 `ai-analysis-system/input/` 文件夹中的待处理文件
```bash
// turbo
ls /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/input/
```

2. 运行新闻分析脚本
```bash
cd /Users/mac/Desktop/my-ccm-projects/ai-analysis-system && python -c "from skills import analyze_news; print(analyze_news())"
```

3. 查看生成的报告
```bash
// turbo
ls /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/processing/
```

## 输出

- 在 `processing/` 文件夹生成 `YYYY-MM-DD-新闻分析.md` 文件
- 包含新闻摘要、市场情绪、重点股票和投资建议
