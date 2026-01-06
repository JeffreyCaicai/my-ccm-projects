---
description: 生成每周投资分析周报
---

# 生成周报 /generate-weekly-report

此工作流用于汇总一周的财经新闻分析，生成周报。

## 使用方法

```
/generate-weekly-report [开始日期] [结束日期]
```

### 参数
- `开始日期`：可选，格式为 YYYY-MM-DD，默认为本周一
- `结束日期`：可选，格式为 YYYY-MM-DD，默认为今天

### 示例
```
/generate-weekly-report 2025-12-30 2026-01-05
/generate-weekly-report  # 生成本周周报
```

## 执行步骤

1. 获取日期范围内的所有分析文件
```bash
// turbo
ls /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/processing/
```

2. 运行周报生成脚本
```bash
cd /Users/mac/Desktop/my-ccm-projects/ai-analysis-system && python -c "from skills import generate_weekly_report; print(generate_weekly_report())"
```

3. 查看生成的周报
```bash
// turbo
cat /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/processing/*周报.md 2>/dev/null | head -50
```

## 输出

- 在 `processing/` 文件夹生成 `YYYY-WXX-周报.md` 文件
- 包含本周热点、行业表现、推荐股票列表、周总结和下周展望
